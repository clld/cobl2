import sys
import re
import os
from collections import OrderedDict
from itertools import groupby

from sqlalchemy.orm import joinedload
from sqlalchemy import func, and_
from clld.cliutil import Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType
from clld.web.util.helpers import data_uri
from clldutils.color import qualitative_colors, rgb_as_hex
from clldutils.path import Path
from clldutils.misc import slug
from pycldf import Wordlist
from clld_phylogeny_plugin.models import Phylogeny, TreeLabel, LanguageTreeLabel
from clld_cognacy_plugin.models import Cognate, Cognateset
from csvw.dsv import reader


import cobl2
from cobl2 import models
import clld_cognacy_plugin.models


data_file_path = Path(cobl2.__file__).parent / '../..' / 'iecor'

ds = Wordlist.from_metadata(data_file_path / 'cldf' / 'cldf-metadata.json')

photos = {
    p.stem: p.as_posix() for p in
    (Path(cobl2.__file__).parent / '../..' / 'CoBL-public' / 'cobl' / 'static' / 'contributors').iterdir()
    if p.suffix == '.jpg'}
for k, v in {
    'Kümmel': 'Kuemmel',
    'de Vaan': 'deVaan',
    'Dewey-Findell': 'Dewey',
}.items():
    photos[k] = photos[v]


def main(args):
    data = Data()

    dataset = common.Dataset(
        id=cobl2.__name__,
        name="IE-CoR",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="https://www.eva.mpg.de",
        license="https://creativecommons.org/licenses/by/4.0/",
        domain='iecor.clld.org',
        contact='iecorproject@gmail.com',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})

    DBSession.add(dataset)

    editors = OrderedDict([('Heggarty', None), ('Anderson', None), ('Scarborough', None)])
    for row in sorted(ds['authors.csv'], key=lambda x: [
            x['Last_Name'].lower(), x['First_Name'].lower()]):
        if row['Last_Name'] in editors:
            editors[row['Last_Name']] = row['ID']
        data.add(
            models.Author,
            row['ID'],
            id=row['ID'],
            name='{0} {1}'.format(row['First_Name'], row['Last_Name']),
            url=row['URL'],
            photo=data_uri(photos[row['Last_Name']], 'image/jpg') if row['Last_Name'] in photos else None)

    for i, cid in enumerate(editors.values()):
        common.Editor(dataset=dataset, contributor=data['Author'][cid], ord=i + 1)

    for src in ds.sources.items():
        for invalid in ['isbn', 'part', 'institution']:
            if invalid in src:
                del src[invalid]
        data.add(
            common.Source,
            src.id,
            id=src.id,
            name=src.get('author', src.get('editor')),
            description=src.get('title', src.get('booktitle')),
            bibtex_type=getattr(EntryType, src.genre, EntryType.misc),
            **src)

    re_links = re.compile(r'\[(?P<label>[^\]]+?)\]\((?P<type>.+?)-(?P<id>\d+)\)')
    link_map = {
        'cog': '/cognatesets/',
        'lex': '/values/',
        'src': '/sources/',
    }

    def parse_links(m):
        try:
            return '<a href="%s%s">%s</a>' % (
                link_map[m.group('type')], m.group('id'), m.group('label'))
        except KeyError:
            print("parse_links: type error in '%s'" % (":".join(m.groups())))
            return '[%s](%s-%s)' % (m.group('label'), m.group('type'), m.group('id'))

    for param in ds['ParameterTable']:
        data.add(
            models.Meaning,
            param['ID'],
            id=slug(param['Name']),
            name=param['Name'],
            description_md=param['Description_md'],
            concepticon_id=int(param['Concepticon_ID']) if param['Concepticon_ID'] != '0' else None,
        )

    for row in ds['clades.csv']:
        data.add(
            models.Clade,
            row['ID'],
            id=row['ID'],
            level0_name=row['level0_name'],
            level1_name=row['level1_name'],
            level2_name=row['level2_name'],
            level3_name=row['level3_name'],
            clade_level0=row['clade_level0'],
            clade_level1=row['clade_level1'],
            clade_level2=row['clade_level2'],
            clade_level3=row['clade_level3'],
            clade_name=row['clade_name'],
            short_name=row['short_name'],
            color=row['color'],
        )

    for row in ds['LanguageTable']:
        c = data.add(
            common.Contribution,
            row['ID'],
            id=row['ID'],
            name=row['Name'],
        )
        for i, cid in enumerate(row['Author_ID']):
            DBSession.add(common.ContributionContributor(
                contribution=c, contributor=data['Author'][cid], ord=i + 1))
        data.add(
            models.Variety,
            row['ID'],
            id=slug(row['Name']),
            name=row['Name'],
            latitude=float(row['Latitude']) if row['Latitude'] is not None else None,
            longitude=float(row['Longitude']) if row['Longitude'] is not None else None,
            contribution=c,
            color=rgb_as_hex(row['Color']),
            clade=', '.join(filter(None, row['Clade'])),
            clade_name=row['clade_name'],
            glottocode=row['Glottocode'],
            historical=row['historical'],
            distribution=row['distribution'],
            logNormalMean=row['logNormalMean'],
            logNormalOffset=row['logNormalOffset'],
            logNormalStDev=row['logNormalStDev'],
            normalMean=row['normalMean'],
            normalStDev=row['normalStDev'],
            ascii_name=row['ascii_name'],
            iso=row['ISO639P3code'],
            lang_description=row['Description'],
            variety=row['Variety'],
            loc_justification=row['loc_justification'] or None,
            sort_order=row['sort_order']
        )

    vsrs = set()
    for row in ds['FormTable']:
        vs = data['ValueSet'].get((row['Language_ID'], row['Parameter_ID']))
        if not vs:
            vs = data.add(
                common.ValueSet,
                (row['Language_ID'], row['Parameter_ID']),
                id='{0}-{1}'.format(row['Language_ID'], row['Parameter_ID']),
                language=data['Variety'][row['Language_ID']],
                parameter=data['Meaning'][row['Parameter_ID']],
                contribution=data['Contribution'][row['Language_ID']],
            )
        v = data.add(
            models.Lexeme,
            row['ID'],
            id=row['ID'],
            name=row['Form'],
            native_script=row['native_script'],
            phonetic=row['phon_form'],
            phonemic=row['Phonemic'],
            comment=re_links.sub(parse_links, row['Comment'] or ''),
            url=row['url'],
            gloss=row['Gloss'],
            valueset=vs
        )
        for src in row['Source']:
            sid, pages = ds.sources.parse(src)
            key = (vs.id, sid, pages)
            if pages:
                pages = pages.replace('|', ';')
            if key not in vsrs:
                DBSession.add(common.ValueSetReference(
                    valueset=vs, source=data['Source'][sid], description=pages))
                vsrs.add(key)

    for row in ds['CognatesetTable']:
        cc = data.add(
            models.CognateClass,
            row['ID'],
            id=row['ID'],
            name=row['ID'],
            root_form=row['Root_Form'] or None,
            root_form_calc=row['Root_Form_calc'] or None,
            root_gloss=row['Root_Gloss'] or None,
            root_language=row['Root_Language'] or None,
            root_language_calc=row['Root_Language_calc'] or None,
            comment=re_links.sub(parse_links, row['Comment'] or ''),
            justification=re_links.sub(parse_links, row['Justification'] or ''),
            ideophonic=row['Ideophonic'] or None,
            parallel_derivation=row['parallelDerivation'] or None,
            revised_by=','.join(row['revised_by']) or None,
            superset_id=int(row['supersetid']) if row['supersetid'] else None,
        )
        for src in row['Source']:
            sid, pages = ds.sources.parse(src)
            if pages:
                pages = pages.replace('|', ';')
            DBSession.add(clld_cognacy_plugin.models.CognatesetReference(
                cognateset=cc, source=data['Source'][sid], description=pages))

    DBSession.flush()

    cc_id_pk_map = {str(ccid): cc.pk for ccid, cc in data['CognateClass'].items()}
    for row in ds['CognatesetTable']:
        if row['proposedAsCognateTo_pk']:
            DBSession.add(models.ProposedCognates(
                cc1_pk=data['CognateClass'][row['ID']].pk,
                cc2_pk=cc_id_pk_map[str(row['proposedAsCognateTo_pk'])],
                scale=row['proposedAsCognateToScale']
            ))
    DBSession.flush()

    loans = {ln['Cognateset_ID']: ln for ln in ds['loans.csv']}
    for ccid, cc in data['CognateClass'].items():
        if ccid in loans:
            le = loans[ccid]
            if le['SourceCognateset_ID']:
                cc.loan_source_pk = data['CognateClass'][le['SourceCognateset_ID']].pk
            else:
                cc.loan_source_pk = None
            cc.loan_notes = le['Comment']
            cc.loan_source_languoid = le['Source_languoid']
            cc.loan_source_form = le['Source_form']
            cc.parallel_loan_event = le['Parallel_loan_event']
            cc.is_loan = True

    for row in ds['CognateTable']:
        cc = data['CognateClass'][row['Cognateset_ID']]
        if cc.meaning_pk is None:
            cc.meaning_pk = data['Lexeme'][row['Form_ID']].valueset.parameter_pk
        else:
            assert data['Lexeme'][row['Form_ID']].valueset.parameter_pk == cc.meaning_pk
        data.add(
            clld_cognacy_plugin.models.Cognate,
            row['ID'],
            cognateset=data['CognateClass'][row['Cognateset_ID']],
            counterpart=data['Lexeme'][row['Form_ID']],
            doubt=row['Doubt'],
        )

    l_by_gc = {}
    for s in DBSession.query(models.Variety):
        l_by_gc[s.glottocode] = s.pk

    tree = Phylogeny(
        id='1',
        name='Bouckaert et al.',
        description='',
        newick=Path.read_text(data_file_path / 'raw' / 'bouckaert_et_al2012' / 'newick.txt'),
    )
    for k, taxon in enumerate(reader(data_file_path / 'raw' / 'bouckaert_et_al2012' / 'taxa.csv', namedtuples=True)):
        label = TreeLabel(
            id='{0}-{1}-{2}'.format(tree.id, slug(taxon.taxon), k + 1),
            name=taxon.taxon,
            phylogeny=tree,
            description=taxon.glottocode)
        if taxon.glottocode in l_by_gc:
            LanguageTreeLabel(language_pk=l_by_gc[taxon.glottocode], treelabel=label)
    DBSession.add(tree)

    l_by_ascii = {}
    for s in DBSession.query(models.Variety):
        l_by_ascii[s.ascii_name] = s.pk

    tree = Phylogeny(
        id='2',
        name='CoBL consensu',
        description='',
        newick=Path.read_text(data_file_path / 'raw' / 'ie122' / 'newick.txt'),
    )
    for k, taxon in enumerate(reader(data_file_path / 'raw' / 'ie122' / 'taxa.csv', namedtuples=True)):
        label = TreeLabel(
            id='{0}-{1}-{2}'.format(tree.id, slug(taxon.taxon), k + 1),
            name=taxon.taxon,
            phylogeny=tree)
        if taxon.taxon in l_by_ascii:
            LanguageTreeLabel(language_pk=l_by_ascii[taxon.taxon], treelabel=label)
    DBSession.add(tree)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    ordered_clade_colors = {k: v for k, v in DBSession.query(models.Clade.clade_name, models.Clade.color)
                            .filter(models.Clade.short_name != '')
                            .order_by(models.Clade.clade_level0).all()}
    for _, cc in groupby(
            DBSession.query(models.CognateClass, models.Variety.clade_name)
            .join(clld_cognacy_plugin.models.Cognate,
                  and_(models.CognateClass.pk == clld_cognacy_plugin.models.Cognate.cognateset_pk))
            .join(models.Value,
                  and_(clld_cognacy_plugin.models.Cognate.counterpart_pk == models.Value.pk))
            .join(common.ValueSet,
                  and_(models.Value.valueset_pk == common.ValueSet.pk))
            .join(models.Variety,
                  and_(common.ValueSet.language_pk == models.Variety.pk))
            .distinct().order_by(models.CognateClass.pk), lambda c: c[0].pk):
        cc = sorted(list(cc))
        cc[0][0].count_clades = len(cc)
        involved_clades = [c[1] for c in cc]
        r = []
        for cl, col in ordered_clade_colors.items():
            if cl in involved_clades:
                r.append(col)
            else:
                r.append('0')
        cc[0][0].involved_clade_colors = ' '.join(r)
        cc[0][0].clades = ', '.join(involved_clades)

    for c in DBSession.query(models.CognateClass, func.count(models.CognateClass.id)) \
            .join(clld_cognacy_plugin.models.Cognate) \
            .group_by(models.CognateClass.pk, models.Cognateset.pk, models.CognateClass.id):
        c[0].count_lexemes = c[1]

    for _, ccs in groupby(
        DBSession.query(models.CognateClass).order_by(models.CognateClass.meaning_pk),
        lambda c: c.meaning_pk
    ):
        ccs = list(ccs)
        colors = qualitative_colors(len(ccs))
        for i, cc in enumerate(ccs):
            cc.color = colors[i]

    for meaning in DBSession.query(models.Meaning).options(
        joinedload(models.Meaning.cognateclasses),
        joinedload(common.Parameter.valuesets, common.ValueSet.language)
    ):
        meaning.count_cognateclasses = len(meaning.cognateclasses)
        meaning.count_languages = len([vs.language for vs in meaning.valuesets])
        meaning.count_loan_cognateclasses = len([cc for cc in meaning.cognateclasses
                                                 if cc.is_loan])

    for meaning in DBSession.query(
        models.Meaning, func.count(common.Parameter.pk))\
            .join(common.Parameter).join(common.ValueSet).join(common.Value).group_by(
                models.Meaning.pk, common.Parameter.pk):
        meaning[0].count_lexemes = meaning[1]

    for language in DBSession.query(common.Language).options(
        joinedload(common.Language.valuesets, common.ValueSet.references)
    ):
        language.count_meanings = len(language.valuesets)
        language.count_lexemes = len(DBSession.query(common.Value.id)
                                     .filter(common.ValueSet.language_pk == language.pk)
                                     .join(common.ValueSet).all())
        spks = set()
        for vs in language.valuesets:
            for ref in vs.references:
                spks.add(ref.source_pk)
        for spk in spks:
            DBSession.add(common.LanguageSource(language_pk=language.pk, source_pk=spk))


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
