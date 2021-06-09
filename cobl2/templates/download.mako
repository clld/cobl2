<%inherit file="${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="clldmpgutil" file="clldmpg_util.mako"/>
<%namespace name="util" file="util.mako"/>

<h3>Downloads</h3>

<div class="alert alert-info">
    <p>
        This IE-CoR web application serves the latest
        ${h.external_link('https://github.com/lexibank/iecor/releases', label='released version')}
        of data curated at
        ${h.external_link('https://github.com/lexibank/iecor', label='cldf-datasets/iecor')}.
    </p>
</div>
