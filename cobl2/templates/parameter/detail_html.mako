<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<h2>${_('Parameter')} ${ctx.name}</h2>
% if ctx.wiki or ctx.description:
    <div id="meaning-more">
    <%util:accordion_group eid="acc-a" parent="meaning-more" title="${_('Description')}" open="True">
        % if ctx.wiki:
            <p>${u.markdown_remove_links(ctx.wiki)|n}</p>
        % endif
        % if ctx.description:
            <h4>Disambiguation</h4>${ctx.description}
        % endif
    </%util:accordion_group>
    </div>
% endif
<div class="alert alert-info">
    Represented in ${len([vs.language for vs in ctx.valuesets])} languages with ${len(ctx.cognateclasses)} cognate sets.
</div>

${(map_ or request.map).render()}

<%util:section title="Lexemes" id="table-container" prefix="">
    ${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
</%util:section>
