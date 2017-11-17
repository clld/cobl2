<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    <div class="well well-small">
        Contributed by ${h.linked_contributors(request, ctx.contribution)}
        ${h.cite_button(request, ctx.contribution)}
    </div>

    ${util.language_meta()}
</%def>
