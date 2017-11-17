<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>


<h2>${ctx.name}</h2>

% if ctx.photo:
    <div style="float: left; margin-right: 20px; margin-bottom: 1em;">
        <img class="img-polaroid" src="${ctx.photo|n}"/>
    </div>
% endif

% if ctx.description:
<p>${ctx.description}</p>
% endif

<dl>
    % if ctx.address:
    <dt>${_('Address')}:</dt>
    <dd>
        <address>
            ${h.text2html(ctx.address)|n}
        </address>
    </dd>
    % endif
    % if ctx.url:
    <dt>${_('Web:')}</dt>
    <dd>${h.external_link(ctx.url)}</dd>
    % endif
    % if ctx.email:
    <dt>${_('Mail:')}</dt>
    <dd>${ctx.email.replace('@', '[at]')}</dd>
    % endif
    ${util.data(ctx, with_dl=False)}
</dl>

<h3 style="clear: left">${_('Contributions')}</h3>
<ul>b
    % for c in ctx.contribution_assocs:
    <li>${h.link(request, c.contribution)}</li>
    % endfor
</ul>
