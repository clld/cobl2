% if ctx.description:
    <p><b>Disambiguation: </b>${ctx.description}</p>
% endif
% if ctx.wiki:
    ${u.markdown_remove_links(ctx.wiki)|n}
% endif