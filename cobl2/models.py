import sqlalchemy as sa
import sqlalchemy.orm

from clld.db.meta import CustomModelMixin
from clld.db.models.common import Parameter, Language, Contribution
from clld_cognacy_plugin.models import MeaningMixin, Cognateset


class Meaning(CustomModelMixin, Parameter, MeaningMixin):
    pk = sa.Column(sa.Integer, sa.ForeignKey('parameter.pk'), primary_key=True)
    example_context = sa.Column(sa.Unicode)
    wiki = sa.Column(sa.Unicode)


class CognateClass(CustomModelMixin, Cognateset):
    pk = sa.Column(sa.Integer, sa.ForeignKey('cognateset.pk'), primary_key=True)
    root_form = sa.Column(sa.Unicode)
    root_gloss = sa.Column(sa.Unicode)
    root_language = sa.Column(sa.Unicode)


class Variety(CustomModelMixin, Language):
    pk = sa.Column(sa.Integer, sa.ForeignKey('language.pk'), primary_key=True)
    contribution_pk = sa.Column(sa.Integer, sa.ForeignKey('contribution.pk'))
    contribution = sa.orm.relationship(
        Contribution, backref=sa.orm.backref('variety', uselist=False))
