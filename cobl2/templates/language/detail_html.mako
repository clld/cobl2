<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
  <div style="float: right;width: 90%">
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
      % if ctx.loc_justification:
        <dt>Note on geographical location</dt>
        <dd>${ctx.loc_justification}</dd>
      % endif
      % if ctx.distribution:
        <br />
        <dt><i>Language Date Calibration</i></dt>
        <dt>Distribution</dt>
        <dd>${ctx.distribution}</dd>
        % if ctx.logNormalOffset:
        <dt>Offset <i>(years before 2000 AD)</i></dt>
        <dd>${ctx.logNormalOffset}</dd>
        % endif
        % if ctx.logNormalMean:
        <dt>Mean <i>(years additional to offset)</i></dt>
        <dd>${ctx.logNormalMean}</dd>
        % endif
        % if ctx.logNormalStDev:
        <dt>Standard deviation <i>(years)</i></dt>
        <dd>${ctx.logNormalStDev}</dd>
        % endif
        % if ctx.normalMean:
        <dt>Mean <i>(years before 2000 AD)</i></dt>
        <dd>${ctx.normalMean}</dd>
        % endif
        % if ctx.normalStDev:
        <dt>Standard deviation <i>(years)</i></dt>
        <dd>${ctx.normalStDev}</dd>
        % endif
      % endif
    </dl>
    </div>

    <div class="accordion" id="sidebar-accordion">
        % if getattr(request, 'map', False):
        <%util:accordion_group eid="acc-map" parent="sidebar-accordion" title="Map" open="${True}">
            ${request.map.render()}
            ${h.format_coordinates(ctx)}
        </%util:accordion_group>
        % endif
    % if ctx.identifiers:
        <%util:accordion_group eid="acc-names" parent="sidebar-accordion" title="${_('Alternative names')}">
            <dl>
            % for type_, identifiers in h.groupby(sorted(ctx.identifiers, key=lambda i: i.type), lambda j: j.type):
                <dt>${type_}:</dt>
                % for identifier in identifiers:
                <dd>${h.language_identifier(request, identifier)}</dd>
                % endfor
            % endfor
            </dl>
        </%util:accordion_group>
    % endif
    </div>
  </div
##    ${util.language_meta()}
</%def>
