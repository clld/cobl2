<%inherit file="../snippet.mako"/>
<%namespace name="util" file="../util.mako"/>

% if request.params.get('parameter'):
    ## called for the info windows on parameter and cognateset maps
    % if request.params.get('is_cognateset_map'):
      <% valueset = u.get_valueset_via_cognate(request, ctx) %>
    % else:
      <% valueset = h.get_valueset(request, ctx) %>
    % endif
    <h4>${h.link(request, ctx)}</h4>
    % if valueset:
        <h5>${_('Value')}</h5>
        <ul class='unstyled'>
            % for value in valueset.values:
            <li>
                ${h.map_marker_img(request, value)}
                ${h.link(request, value, label=value.__str__())}
                ${h.format_frequency(request, value)}
            </li>
            % endfor
        </ul>
        % if valueset.references:
            <h5>${_('Source')}</h5>
            <p style="margin-top:-4px;">${u.cobl_linked_references(request, valueset)}</p>
        % endif
    % endif
% else:
<h4>${h.link(request, ctx)}</h4>
    % if ctx.description:
        <p>${ctx.description}</p>
    % endif
${h.format_coordinates(ctx)}
% endif