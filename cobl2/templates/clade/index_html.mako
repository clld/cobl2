<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "clades" %>

<%block name="title">${_('Clades Reference')}</%block>
<h2>${_('Clades Reference')}</h2>
<div>
    ${ctx.render()}
</div>
