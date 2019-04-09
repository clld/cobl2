<%inherit file="../snippet.mako"/>
<%namespace name="util" file="../util.mako"/>
% if ctx.valueset.references:
    <dt>${_('Lexeme Source')}</dt>
    <dd>${u.cobl_linked_references(request, ctx.valueset, False)|n}</dd>
% endif
