% if ctx.example_context:
    <p><b>Example context: </b>${ctx.example_context}</p>
% endif
% if ctx.description:
    <p><b>Disambiguation: </b>${ctx.description}</p>
% endif
% if ctx.wiki:
    ${u.markdown_remove_links(ctx.wiki)|n}
% endif