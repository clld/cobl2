% if ctx.example_context:
    <b>Example context: </b>${ctx.example_context}
% endif
% if ctx.wiki:
    ${u.markdown(ctx.wiki)|n}
% endif