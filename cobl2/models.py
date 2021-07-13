import sqlalchemy as sa
import sqlalchemy.orm

from clld.db.meta import CustomModelMixin, Base
from clld.db.models.common import (
    Parameter, Language, Contribution,
    Contributor, Value, Identifier,
    IdentifierType, IdNameDescriptionMixin)
from clldutils.color import is_bright
from clld_cognacy_plugin.models import MeaningMixin, Cognateset
from zope.interface import implementer
from cobl2 import interfaces as cobl2_interfaces


SUPERSET_COLORS = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8',
                   '#f58231', '#911eb4', '#46f0f0', '#f032e6',
                   '#bcf60c', '#fabebe']


@implementer(cobl2_interfaces.IClade)
class Clade(Base, IdNameDescriptionMixin):
    pk = sa.Column(sa.Integer, primary_key=True)
    level0_name = sa.Column(sa.Unicode)
    level1_name = sa.Column(sa.Unicode)
    level2_name = sa.Column(sa.Unicode)
    level3_name = sa.Column(sa.Unicode)
    clade_name = sa.Column(sa.Unicode)
    color = sa.Column(sa.Unicode)
    clade_level0 = sa.Column(sa.Integer)
    clade_level1 = sa.Column(sa.Integer)
    clade_level2 = sa.Column(sa.Integer)
    clade_level3 = sa.Column(sa.Integer)
    short_name = sa.Column(sa.Unicode)


class Lexeme(CustomModelMixin, Value):
    pk = sa.Column(sa.Integer, sa.ForeignKey('value.pk'), primary_key=True)
    native_script = sa.Column(sa.Unicode)
    phonetic = sa.Column(sa.Unicode)
    phonemic = sa.Column(sa.Unicode)
    comment = sa.Column(sa.Unicode)
    gloss = sa.Column(sa.Unicode)
    url = sa.Column(sa.Unicode)


class Meaning(CustomModelMixin, Parameter, MeaningMixin):
    pk = sa.Column(sa.Integer, sa.ForeignKey('parameter.pk'), primary_key=True)
    description_md = sa.Column(sa.Unicode)
    count_languages = sa.Column(sa.Integer)
    count_cognateclasses = sa.Column(sa.Integer)
    count_loan_cognateclasses = sa.Column(sa.Integer)
    count_lexemes = sa.Column(sa.Integer)


class ProposedCognates(Base):
    cc1_pk = sa.Column(sa.Integer, sa.ForeignKey('cognateclass.pk'))
    cc2_pk = sa.Column(sa.Integer, sa.ForeignKey('cognateclass.pk'))
    scale = sa.Column(sa.Integer)
    proposedAsCognateTo_rel = sa.orm.relationship(
        'CognateClass',
        foreign_keys=[cc1_pk],
        backref=sa.orm.backref('proposedAsCognateTo'))


class CognateClass(CustomModelMixin, Cognateset):
    pk = sa.Column(sa.Integer, sa.ForeignKey('cognateset.pk'), primary_key=True)
    root_form = sa.Column(sa.Unicode)
    root_form_calc = sa.Column(sa.Unicode)
    root_gloss = sa.Column(sa.Unicode)
    root_language = sa.Column(sa.Unicode)
    root_language_calc = sa.Column(sa.Unicode)
    meaning_pk = sa.Column(sa.Integer, sa.ForeignKey('meaning.pk'))
    meaning = sa.orm.relationship(Meaning, backref='cognateclasses')
    color = sa.Column(sa.Unicode)
    clades = sa.Column(sa.Unicode)
    superset_id = sa.Column(sa.Integer)

    proposedAsCognateTo_rel = sa.orm.relationship(
        'ProposedCognates',
        foreign_keys=[pk],
        primaryjoin=pk == ProposedCognates.cc2_pk,
        backref=sa.orm.backref('cognateclass'))

    loan_source_pk = sa.Column(sa.Integer, sa.ForeignKey('cognateclass.pk'))
    loan_notes = sa.Column(sa.Unicode)
    loan_source_form = sa.Column(sa.Unicode)
    loan_source_languoid = sa.Column(sa.Unicode)
    parallel_loan_event = sa.Column(sa.Boolean, default=False)
    parallel_derivation = sa.Column(sa.Boolean, default=False)
    ideophonic = sa.Column(sa.Boolean, default=False)
    is_loan = sa.Column(sa.Boolean, default=False)
    comment = sa.Column(sa.Unicode)
    justification = sa.Column(sa.Unicode)
    revised_by = sa.Column(sa.Unicode)
    count_lexemes = sa.Column(sa.Integer)
    count_clades = sa.Column(sa.Integer)
    involved_clade_colors = sa.Column(sa.Unicode)
    loans = sa.orm.relationship(
        'CognateClass',
        foreign_keys=[loan_source_pk],
        backref=sa.orm.backref('loan_source', remote_side=[pk]))

    meaning_rel = sa.orm.relationship('Meaning', viewonly=True)

    def __str__(self):
        res = self.root_form if self.root_form else ''
        if self.root_language:
            res += ' [{0}]'.format(self.root_language)
        if len(res) > 0:
            return res
        return Cognateset.__str__(self)

    def get_superset_color(self):
        return SUPERSET_COLORS[self.superset_id % 10]


class Variety(CustomModelMixin, Language):
    pk = sa.Column(sa.Integer, sa.ForeignKey('language.pk'), primary_key=True)
    contribution_pk = sa.Column(sa.Integer, sa.ForeignKey('contribution.pk'))
    contribution = sa.orm.relationship(
        Contribution, backref=sa.orm.backref('variety', uselist=False))
    color = sa.Column(sa.Unicode)
    clade = sa.Column(sa.Unicode)
    clade_name = sa.Column(sa.Unicode)
    fossil = sa.Column(sa.Boolean, default=False)
    historical = sa.Column(sa.Boolean, default=False)
    distribution = sa.Column(sa.Unicode)
    logNormalMean = sa.Column(sa.Integer)
    logNormalOffset = sa.Column(sa.Integer)
    logNormalStDev = sa.Column(sa.Float)
    normalMean = sa.Column(sa.Integer)
    normalStDev = sa.Column(sa.Integer)
    glottocode = sa.Column(sa.Unicode)
    ascii_name = sa.Column(sa.Unicode)
    iso = sa.Column(sa.Unicode)
    lang_description = sa.Column(sa.Unicode)
    variety = sa.Column(sa.Unicode)
    sort_order = sa.Column(sa.Integer)
    loc_justification = sa.Column(sa.Unicode)
    count_meanings = sa.Column(sa.Integer)
    count_lexemes = sa.Column(sa.Integer)

    @property
    def fontcolor(self):
        return '#000' if is_bright(self.color) else '#eee'

    def get_identifier_objs(self, type_):
        o = Identifier()
        if getattr(type_, 'value', type_) == str(IdentifierType.glottolog):
            if not self.glottocode:
                return []
            o.name = self.glottocode
            o.type = str(IdentifierType.glottolog)
            return [o]
        if getattr(type_, 'value', type_) == str(IdentifierType.iso):
            if not self.iso:
                return []
            o.name = self.iso
            o.type = str(IdentifierType.iso)
            return [o]
        return []


class Author(CustomModelMixin, Contributor):
    pk = sa.Column(sa.Integer, sa.ForeignKey('contributor.pk'), primary_key=True)
    photo = sa.Column(sa.String)
