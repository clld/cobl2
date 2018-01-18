"""script to create the default set of map marker icons distributed with clld."""
import os
import sys

from csvw.dsv import reader
import pyx
from pyx import bbox, unit, style, path, color, canvas, deco
# set the scale to 1/20th of an inch
unit.set(uscale=0.05, wscale=0.02, defaultunit="inch")

linewidth = style.linewidth(1.2)


def pyxColor(string):
    """Return a pyxColor instance.

    :param string: RGB color name like 'ffffff'
    :return: pyx color.

    >>> assert pyxColor('ffffff')
    """
    assert len(string) == 6
    colorTuple = tuple(
        int('0x' + c, 16) for c in [string[i:i + 2] for i in range(0, 6, 2)])
    return color.rgb(*[i / 255.0 for i in colorTuple])


if __name__ == '__main__':  # pragma: no cover
    out = sys.argv[1]
    if not pyx:
        sys.exit(1)
    for icon in set(d['Color'] for d in reader('../cobl-data/cldf/languages.csv', dicts=True)):
        assert len(icon) == 6
        c = canvas.canvas()
        c.draw(
            path.circle(20, 20, 13.6),
            [deco.stroked([linewidth]), deco.filled([pyxColor(icon)])])
        stream = c.pipeGS("pngalpha", resolution=20, bbox=bbox.bbox(0, 0, 40, 40))
        with open(os.path.join(out, 'c{0}.png'.format(icon)), 'wb') as fp:
            fp.write(stream.read())
    sys.exit(0)

