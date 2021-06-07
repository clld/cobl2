<%inherit file="${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="clldmpgutil" file="clldmpg_util.mako"/>
<%namespace name="util" file="util.mako"/>

<h3>Downloads</h3>
<p>
  Please find here the underlying dataset ${h.external_link('https://github.com/lexibank/iecor', label='https://github.com/lexibank/iecor')}.
</p>
