<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "policies" %>
<%block name="title">${ctx.name}</%block>

<h2>${ctx.name}</h2>
% if ctx.markup_description:
    ${u.markdown_policies(ctx.markup_description)|n}
% endif

<%def name="sidebar()">
    ${table_of_policies|n}
</%def>

