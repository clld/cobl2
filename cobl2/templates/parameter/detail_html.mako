<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')}: ${ctx.name}</%block>

<h2>${_('Parameter')}: ${ctx.name}</h2>
${(map_ or request.map).render()}

<div class="alert alert-info">
    Represented in ${ctx.count_languages} language${langs_suf} with ${ctx.count_cognateclasses} cognate set${cogclasses_suf}.
</div>
% if ctx.description_md or ctx.description:
    <div id="meaning-more">
    <%util:accordion_group eid="acc-a" parent="meaning-more" title="${_('IE-CoR Definition')}">
        % if ctx.description_md:
            <p>${u.markdown_handle_links(request, ctx.description_md)|n}</p>
        % endif
        % if ctx.description:
            <h4>Disambiguation</h4>${ctx.description}
        % endif
    </%util:accordion_group>
</div>
% endif


<h2>${'Cognate sets for meaning: %s' % (ctx.name)}</h2>
${request.get_datatable('cognatesets', u.CognateClass, parameter=ctx).render()}
<h2>Lexeme Details</h2>
${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
