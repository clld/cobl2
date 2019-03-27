<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.codes()}
    <div style="clear: right;"> </div>
    <div class="well well-small">
        Contributed by ${h.linked_contributors(request, ctx.contribution)}
        ${h.cite_button(request, ctx.contribution)}
    </div>
    <div class="well well-small">
    <dl>
        <dt>Clade</dt>
        <dd>${ctx.clade}</dd>
      % if ctx.historical:
        <dt>Historical</dt>
        <dd>yes</dd>
      % endif
      % if ctx.variety:
        <dt>Variety</dt>
        <dd>${ctx.variety}</dd>
      % endif
      % if ctx.lang_description:
        <dt>Description</dt>
        <dd>${ctx.lang_description}</dd>
      % endif
      % if ctx.earliest_time_depth_bound:
        <dt>Earliest time depth bound</dt>
        <dd>${ctx.earliest_time_depth_bound}</dd>
      % endif
      % if ctx.latest_time_depth_bound:
        <dt>Latest time depth bound</dt>
        <dd>${ctx.latest_time_depth_bound}</dd>
      % endif
    </dl>
    </div>

    ${util.language_meta()}
</%def>
