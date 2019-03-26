<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! from clld.web.util.glottolog import link %>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    <div class="well well-small">
        Contributed by ${h.linked_contributors(request, ctx.contribution)}
        ${h.cite_button(request, ctx.contribution)}
    </div>
    <div class="well well-small">
    <dl>
      % if ctx.glottocode:
        <dt>Glottolog code</dt>
        <dd>${link(request, id=ctx.glottocode, label=ctx.glottocode)}</dd>
      % endif
        <dt>Clade</dt>
        <dd>${ctx.clade}</dd>
      % if ctx.historical:
        <dt>Historical</dt>
        <dd>yes</dd>
      % endif
    </dl>
    </div>

    ${util.language_meta()}
</%def>
