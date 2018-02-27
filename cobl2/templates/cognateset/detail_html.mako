<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "cognatesets" %>
<%block name="title">${_('Cognateset')} ${ctx.name}</%block>

<%def name="sidebar()">
    <div class="well">
        <dl>
            <dt>Meaning:</dt>
            <dd>${h.link(req, ctx.meaning)}</dd>
            % if ctx.root_form:
                <dt>Root form</dt>
                <dd><i>${ctx.root_form}</i></dd>
            % endif
            % if ctx.root_gloss:
                <dt>Root gloss</dt>
                <dd>${ctx.root_gloss}</dd>
            % endif
            % if ctx.root_language:
                <dt>Root languoid</dt>
                <dd>${ctx.root_language}</dd>
            % endif
            % if ctx.loan_source:
                <dt>Loan from</dt>
                <dd>${h.link(req, ctx.loan_source)}</dd>
            % endif
        </dl>
    </div>
</%def>


<h2>${_('Cognateset')} ${ctx.name}</h2>

% if ctx.description:
<p>${ctx.description}</p>
% endif

% if map_ or request.map:
${(map_ or request.map).render()}
% endif

<%util:table args="item" items="${ctx.cognates}">
    <%def name="head()">
        <th>Form</th>
        <th>Language</th>
    </%def>
    <td>${h.link(request, item.counterpart)|n}</td>
    <td>
        ${h.map_marker_img(req, item.counterpart.valueset.language)}
        ${h.link(request, item.counterpart.valueset.language)}
    </td>
</%util:table>
