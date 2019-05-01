<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}"
       style="padding-top: 7px; padding-bottom: 2px;">
        <img src="${request.static_url('cobl2:static/IE-CoR.png')}" width="71px"/>
    </a>
</%block>

${next.body()}
