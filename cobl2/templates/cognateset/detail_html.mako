<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "cognatesets" %>
<%block name="title">${_('Cognateset')} ${ctx.name}</%block>

<%def name="sidebar()">
    <div class="well">
        <h4>${_('Meaning')}: ${h.link(req, ctx.meaning)}</h4>
        <dl>
            % if ctx.root_form:
                <dt>${_('Root form')}</dt>
                <dd><i>${ctx.root_form}</i></dd>
            % endif
            % if ctx.root_gloss:
                <dt>${_('Root gloss')}</dt>
                <dd>${ctx.root_gloss}</dd>
            % endif
            % if ctx.root_language:
                <dt>${_('Root languoid')}</dt>
                <dd>${ctx.root_language}</dd>
            % endif
        </dl>
    % if ctx.parallel_loan_event or ctx.loan_source or ctx.loan_source_form or ctx.loan_source_languoid or ctx.loan_notes:
        % if ctx.parallel_loan_event:
          <h4>${_('Parallel loan event:')}</h4>
        % else:
          <h4>${_('Loan event:')}</h4>
        % endif
        <dl>
          % if ctx.loan_source:
              <dt>${_('Loan from')}</dt>
              <dd>${h.link(req, ctx.loan_source)}</dd>
          % endif
          % if ctx.loan_source_languoid:
              <dt>${_('Loan source')}</dt>
              <dd>${ctx.loan_source_languoid}</dd>
          % endif
          % if ctx.loan_source_form:
              <dt>${_('Loan source form')}</dt>
              <dd>${ctx.loan_source_form}</dd>
          % endif
          % if ctx.loan_notes:
              <dt>${_('Loan notes')}</dt>
              <dd>${ctx.loan_notes}</dd>
          % endif
        </dl>
     % endif
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
        <th>Language</th>
        <th>Lexeme</th>
        <th>Native script</th>
        <th>Phonetic</th>
        <th>Phonemic</th>
    </%def>
    <td>
        ${h.map_marker_img(req, item.counterpart.valueset.language)}
        ${h.link(request, item.counterpart.valueset.language)}
    </td>
    <td>${h.link(request, item.counterpart)|n}</td>
    <td>${item.counterpart.native_script or ''}</td>
    <td>${item.counterpart.phonetic or ''}</td>
    <td>${item.counterpart.phonemic or ''}</td>
</%util:table>
