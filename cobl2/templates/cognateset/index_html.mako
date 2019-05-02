<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "cognatesets" %>
<%block name="title">${_('Cognatesets')}</%block>

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
</%block>

<div class="pull-right well well-large" style="padding: 8px 8px">
    <form>
        <fieldset>
                Select shared clades within a cognate set:<br />
                <small>
                    <i>To get the cognate sets which share these clades uniquely,<br />
                    enter the number of chosen clades into to the filter box </i><b># clades</b>
                </small>
            <br/>
            ${select.render()}
            <button class="btn btn-small" type="submit">Filter</button>
        </fieldset>
    </form>
</div>

<h2>${title()}</h2>

<div class="clearfix"> </div>
<div>
    ${ctx.render()}
</div>
