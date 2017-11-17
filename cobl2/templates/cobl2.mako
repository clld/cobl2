<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}"
       style="padding-top: 7px; padding-bottom: 2px;">
        <img src="${request.static_url('cobl2:static/cognac_32px.png')}"/>
        CoBL
    </a>
</%block>

${next.body()}
