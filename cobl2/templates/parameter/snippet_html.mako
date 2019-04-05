% if ctx.example_context:
    <b>Example context: </b>${ctx.example_context}
% endif
% if ctx.wiki:
    ${u.markdown_remove_links(ctx.wiki)|n}
% endif