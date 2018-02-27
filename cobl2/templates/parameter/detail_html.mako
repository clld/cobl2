<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>
<%! from clld_phylogeny_plugin.tree import Tree %>

<%block name="head">
    ${Tree.head(req)|n}
</%block>

<ul class="nav nav-pills" style="float: right">
    <li class="">
        <a href="#map-container">
            <img src="${req.static_url('cobl2:static/Map_Icon.png')}"
                 width="35">
            Map
        </a>
    </li>
    <li class="">
        <a href="#table-container">
            <img src="${req.static_url('cobl2:static/Table_Icon.png')}"
                 width="35">
            Table
        </a>
    </li>
    <li class="">
        <a href="#tree-container">
            <img src="${req.static_url('cobl2:static/Tree_Icon.png')}"
                 width="35">
            Tree
        </a>
    </li>
</ul>

<h2>${_('Parameter')} ${ctx.name}</h2>

% if ctx.description:
    <p>${ctx.description}</p>
% endif

${(map_ or request.map).render()}

<%util:section title="Lexemes" id="table-container" prefix="">
    ${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
</%util:section>

<%util:section title="Phylogeny" id="tree-container" prefix="">
    ${tree.render()}
</%util:section>
