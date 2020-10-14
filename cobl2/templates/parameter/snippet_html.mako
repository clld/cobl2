% if ctx.description_md:
    ${u.markdown_handle_links(request, ctx.description_md)|n}
% endif