from typing import Literal
from enum import Enum
from io import BytesIO, StringIO


class RenderType(Enum):
    Vector='vector'
    Raster='raster'


def easy_plot(doc=None, figure=None,
              render_as: Literal['vector', 'raster'] = 'vector',
              fix_size=True, size_inches=None, size_cm=None):
    """Render the handed (matplotlib) figure, or the current matplotlib figure, in the document

    """
    plt = None
    if figure is None:
        import matplotlib.pyplot as plt
        figure = plt.gcf()

    if fix_size or size_inches is not None or size_cm is not None:
        target_size = None
        if size_inches is not None:
            target_size = size_inches
        elif size_cm is not None:
            target_size = tuple([size/2.54 for size in size_cm])
        else:
            target_size = (6, 4)

        figure.set_size_inches(target_size)


    if render_as == 'vector':
        i = StringIO()
        figure.savefig(i, format='svg')
        s = i.getvalue()
        return doc.img(svg=s, classes=['plot'])
    elif render_as == 'raster':
        i = BytesIO()
        figure.savefig(i, format='png')
        s = i.getvalue()
        return doc.img(png=s, classes=['plot'])
    else:
        raise NotImplementedError("Render_as must be either 'vector' or 'raster'")
