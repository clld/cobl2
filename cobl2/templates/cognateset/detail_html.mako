<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "cognatesets" %>
<%block name="title">${_('Cognateset')} ${ctx.name}</%block>

<h2>${_('Cognateset')} ${ctx.name}<span style="font-weight: normal;"> – ${_('Meaning')}: ${h.link(req, ctx.meaning)}</span></h2>
<div class="container-fluid">
    <div style="float: left;margin-right: 30px;">
        <dl>
          % if ctx.root_form_calc:
            <dt>${_('IE-CoR reference form')}:</dt>
            <dd><i>${ctx.root_form_calc}</i></dd>
          % elif ctx.root_form:
            <dt>${_('IE-CoR reference form')}:</dt>
            <dd>${ctx.root_form}</dd>
          % endif
          % if ctx.root_language_calc:
            <dt>${_('IE-CoR reference language')}:</dt>
            <dd><i>${ctx.root_language_calc}</i></dd>
          % elif ctx.root_language:
            <dt>${_('IE-CoR reference language')}:</dt>
            <dd>${ctx.root_language}</dd>
          % endif
          % if ctx.root_gloss:
            <dt>${_('Gloss in IE-CoR reference language')}:</dt>
            <dd>${ctx.root_gloss}</dd>
          % endif
            <dt>${_('Ideophonic')}:</dt>
            <dd>${_('yes') if ctx.ideophonic else _('no')}</dd>
            <dt>${_('Parallel derivation')}:</dt>
            <dd>${_('yes') if ctx.parallel_derivation else _('no')}</dd>
          % if ctx.cognates[0].doubt:
            <dt>${_('Dubious set')}:</dt>
            <dd>yes</dd>
          % endif
          % if ctx.proposedAsCognateTo:
            <dt>${_('Proposed as cognate to')}:</dt>
            <dd><a href="${request.route_url('cognatesets')}/${ctx.proposedAsCognateTo[0].cognateclass[0].id}">
                ${ctx.proposedAsCognateTo[0].cognateclass[0]}</a>
                <i>scale:</i> ${ctx.proposedAsCognateTo[0].scale}</dd>
          % endif
        </dl>
    </div>

% if ctx.is_loan:
    <div style="float: left;margin-right: 30px;">
        <dl>
            <dt>${_('Loan event')}:</dt>
            <dd>${_('yes')}</dd>
            <dt>${_('Parallel loan event')}:</dt>
            <dd>${_('yes') if ctx.parallel_loan_event else _('no')}</dd>
          % if ctx.loan_source_languoid:
            <dt>${_('Loan source language')}:</dt>
            <dd>${ctx.loan_source_languoid}</dd>
          % endif
          % if ctx.loan_source_form:
            <dt>${_('Source lexeme in loan source language')}:</dt>
            <dd>${ctx.loan_source_form}</dd>
          % endif
          % if ctx.loan_source:
            <dt>${_('Loan source lexeme belongs to cognate set')}:</dt>
            <dd>${h.link(req, ctx.loan_source)}</dd>
          % endif
          % if ctx.loan_notes:
            <dt>${_('Loan notes')}:</dt>
            <dd>${ctx.loan_notes}</dd>
          % endif
        </dl>
    </div>
% endif

    <div style="float: left;width:70%">
        <dl>
          % if ctx.justification:
            <dt>${_('Justification')}:</dt>
            <dd>${ctx.justification | n}</dd>
          % endif
          % if ctx.clades:
            <dt>${_('Found in clades')}:</dt>
            <dd>${ctx.clades}</dd>
          % endif
          % if revisors:
            <dt>${_('Revised by')}:</dt>
            <dd>${revisors|n}</dd>
          % endif
        </dl>
    </div>
</div>

% if ctx.description:
<p>${ctx.description}</p>
% endif

% if map_ or request.map:
<div style="margin-top:30px">
${(map_ or request.map).render()}
</div>
% endif

<%util:table args="item" items="${ctx.cognates}" options="${dict(aaSorting=[[0, 'asc']])}">
    <%def name="head()">
        <th></th>
        <th>Language</th>
        <th>Lexeme</th>
        <th>Native&nbsp;script</th>
        <th>Phonetic</th>
        <th>Phonemic</th>
        <th>Notes</th>
    </%def>
    <td><span class="hide">${item.counterpart.valueset.language.sort_order}</span></td>
    <td style="white-space: nowrap;">
        <span style="border-left:12px solid ${item.counterpart.valueset.language.color};padding-left:5px" 
            title="Clade: ${item.counterpart.valueset.language.clade}">&nbsp;</span>
        ${h.link(request, item.counterpart.valueset.language)}
    </td>
    <td>${h.link(request, item.counterpart)|n}</td>
    <td>${item.counterpart.native_script or ''}</td>
    <td>${item.counterpart.phonetic or ''}</td>
    <td>${item.counterpart.phonemic or ''}</td>
    <td>${item.counterpart.comment or '' | n}</td>
</%util:table>

% if ctx.references:
    <dl style="margin-top:30px">
        <dt>${_('References')}</dt>
        <dd>${u.cobl_linked_references(request, ctx, True)|n}</dd>
    </dl>
% endif

