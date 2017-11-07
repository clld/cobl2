from clld.web.assets import environment
from clldutils.path import Path

import cobl2


environment.append_path(
    Path(cobl2.__file__).parent.joinpath('static').as_posix(),
    url='/cobl2:static/')
environment.load_path = list(reversed(environment.load_path))
