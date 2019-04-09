<%inherit file="../snippet.mako"/>
<%namespace name="util" file="../util.mako"/>

% if ctx.root_gloss:
    <h5>${_('Gloss')}</h5>
    <p style="margin-top:-4px;">${ctx.root_gloss}</p>
% endif
% if ctx.references:
    <h5>${_('Cognate Set Source')}</h5>
    <p style="margin-top:-4px;">${u.cobl_linked_references(request, ctx)}</p>
% endif
