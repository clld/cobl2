<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "policies" %>

<%block name="title">${_('Policies')}</%block>

<h3>IE-CoR Policy Pages</h3>

<%def name="sidebar()">
    ${table_of_policies|n}
</%def>

