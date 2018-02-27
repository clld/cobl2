# coding: utf8
from __future__ import unicode_literals
import sys
from collections import OrderedDict
from itertools import groupby

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType
from clld.web.util.helpers import data_uri
from clldutils.path import Path, read_text
from clldutils.misc import slug
from pycldf import Wordlist
from clld_phylogeny_plugin.models import Phylogeny, TreeLabel, LanguageTreeLabel
from csvw.dsv import reader


import cobl2
from cobl2 import models
import clld_cognacy_plugin.models


CC_COLORS = [
    '#ff0000',
    '#e5bf73',
    '#003330',
    '#b1a3d9',
    '#bf0000',
    '#403610',
    '#bffffb',
    '#6930bf',
    '#4c0000',
    '#f2e200',
    '#00e2f2',
    '#a200f2',
    '#ff8080',
    '#a69b00',
    '#59adb3',
    '#81698c',
    '#8c4646',
    '#736d1d',
    '#0099bf',
    '#da79f2',
    '#331a1a',
    '#f2eeb6',
    '#002933',
    '#912699',
    '#e6acac',
    '#66644d',
    '#1a5766',
    '#40103d',
    '#735656',
    '#a3a67c',
    '#303d40',
    '#e639c3',
    '#f26d3d',
    '#334000',
    '#738c99',
    '#e6acda',
    '#4c2213',
    '#b8d936',
    '#001b33',
    '#332630',
    '#bf7960',
    '#7f994d',
    '#3d9df2',
    '#a6006f',
    '#7f3300',
    '#296600',
    '#406280',
    '#660044',
    '#b2622d',
    '#299900',
    '#bfe1ff',
    '#f20081',
    '#8c6246',
    '#bef2b6',
    '#4073ff',
    '#66334e',
    '#f2ceb6',
    '#1a331a',
    '#5369a6',
    '#8c0038',
    '#4c2900',
    '#00e61f',
    '#0000ff',
    '#40001a',
    '#d98d36',
    '#36d977',
    '#0000d9',
    '#d96c98',
    '#33210d',
    '#4d996b',
    '#2d2d59',
    '#997382',
    '#4c3b26',
    '#4d6657',
    '#070033',
    '#7f0011',
    '#332d26',
    '#004d33',
    '#31238c',
    '#cc3347',
    '#ffaa00',
    '#40ffd9',
    '#180059',
    '#664400',
    '#00736b',
    '#7159b3'
]

ds = Wordlist.from_metadata(
    Path(cobl2.__file__).parent / '../..' / 'cobl-data' / 'cldf' / 'Wordlist-metadata.json')
wiki = Path(cobl2.__file__).parent / '../..' / 'CoBL-public.wiki'
photos = {
    p.stem: p.as_posix() for p in
    (Path(cobl2.__file__).parent / '../..' / 'CoBL-public' / 'static' / 'contributors').iterdir()
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
        name="CoBL-IE",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='cobl2.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})

    DBSession.add(dataset)

    editors = OrderedDict([('Heggarty', None), ('Anderson', None)])
    for row in ds['authors.csv']:
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

    def clean_md(t):
        lines = []
        for line in t.splitlines():
            if line.startswith('#'):
                line = '##' + line
            lines.append(line)
        return '\n'.join(lines)

    for param in ds['ParameterTable']:
        wiki_page = wiki / '{0}.md'.format(param['Name'])
        data.add(
            models.Meaning,
            param['ID'],
            id=param['ID'],
            name=param['Name'],
            description=param['Description'],
            wiki=clean_md(read_text(wiki_page)) if wiki_page.exists() else None,
            example_context=param['Example_Context'],
            concepticon_id=int(param['Concepticon_ID']) if param['Concepticon_ID'] != '0' else None,
        )

    for row in ds['LanguageTable']:
        c = data.add(
            common.Contribution,
            row['ID'],
            id=row['ID'],
            name='{0} Dataset'.format(row['Name']),
        )
        for i, cid in enumerate(row['Author_ID']):
            DBSession.add(common.ContributionContributor(
                contribution=c, contributor=data['Author'][cid], ord=i + 1))
        data.add(
            models.Variety,
            row['ID'],
            id=row['ID'],
            name=row['Name'],
            latitude=float(row['Latitude']),
            longitude=float(row['Longitude']),
            contribution=c,
            color=row['Color'],
            clade=row['Clade'],
            glottocode=row['Glottocode'],
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
            common.Value,
            row['ID'],
            id=row['ID'],
            name=row['Romanised'],
            valueset=vs
        )
        for src in row['Source']:
            sid, pages = ds.sources.parse(src)
            key = (vs.id, sid, pages)
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
            root_gloss=row['Root_Gloss'] or None,
            root_language=row['Root_Language'] or None,
        )
        for src in row['Source']:
            sid, pages = ds.sources.parse(src)
            DBSession.add(clld_cognacy_plugin.models.CognatesetReference(
                cognateset=cc, source=data['Source'][sid], description=pages))

    DBSession.flush()
    loans = {l['Cognateset_ID']: l for l in ds['loans.csv']}
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

    for row in ds['CognateTable']:
        cc = data['CognateClass'][row['Cognateset_ID']]
        if cc.meaning_pk is None:
            cc.meaning_pk = data['Value'][row['Form_ID']].valueset.parameter_pk
        else:
            assert data['Value'][row['Form_ID']].valueset.parameter_pk == cc.meaning_pk
        data.add(
            clld_cognacy_plugin.models.Cognate,
            row['ID'],
            cognateset=data['CognateClass'][row['Cognateset_ID']],
            counterpart=data['Value'][row['Form_ID']],
        )

    l_by_gc = {}
    for s in DBSession.query(models.Variety):
        l_by_gc[s.glottocode] = s.pk

    tree = Phylogeny(
        id='1',
        name='phy',
        description='',
        newick=read_text(args.data_file('cldf', 'bouckaert_et_al2012', 'newick.txt')),
    )
    for k, taxon in enumerate(reader(args.data_file('cldf', 'bouckaert_et_al2012', 'taxa.csv'), namedtuples=True)):
        label = TreeLabel(
            id='{0}-{1}-{2}'.format(tree.id, slug(taxon.taxon), k + 1),
            name=taxon.taxon,
            phylogeny=tree,
            description=taxon.glottocode)
        if taxon.glottocode in l_by_gc:
            LanguageTreeLabel(language_pk=l_by_gc[taxon.glottocode], treelabel=label)
    DBSession.add(tree)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for _, ccs in groupby(
        DBSession.query(models.CognateClass).order_by(models.CognateClass.meaning_pk),
        lambda c: c.meaning_pk
    ):
        for i, cc in enumerate(ccs):
            cc.color = CC_COLORS[i]


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
