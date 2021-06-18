
# This workaround courtesy of https://docs.python-guide.org/writing/structure/
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from html_doc import HtmlDoc

def make_standard_doc():
    d = HtmlDoc(title="This is a document")

    d.h1("This is a title")
    d.anchor("title")
    with d.div:
        d.p("test line")
        d.p("test line")
        d.p("test line")
    d.h1("Title")
    d.h2("Subtitle")
    d.h3("Subsubtitle")
    d.h4("Subsubsubtitle")
    with d.p:
        d.raw('Should have a line break now:')
        d.br()
        d.br()
        d.raw('See above, ')
        d.ital("italics, ")
        d.bold("bold, ")
        d.underline("underlined!")

    with d.p(classes=['test']):
        d.raw("Text")

    d.hline()
    with d.ul:
        d.li(d.p("Item1"))
        d.li(d.p("Item2"))
        d.li(d.p("Item3"))
        d.li(d.p("Item4"))
    d.hline()
    with d.ol:
        d.li(d.p("Item1"))
        d.li(d.p("Item2"))
        d.li(d.p("Item3"))
        d.li(d.p("Item4"))
    #
    d.raw("<div><p>Some HTML</p></div>")
    d.h1("PNGs:")
    d.img(png=open('tests/example.png', 'rb').read())
    d.img(path='tests/example.png')
    d.h1("Jpegs:")
    d.img(jpg=open('tests/example.jpg', 'rb').read())
    d.img(path='tests/example.jpg')
    d.h1("SVGs:")
    d.img(svg=open('tests/example.svg').read())
    d.img(path='tests/example.svg', width="2in")
    d.img(path='tests/example.svg', height="25mm")
    d.svg(open('tests/example.svg').read())
    with d.a(href="#title"):
        d.raw("A link 1")

    easy_table(d)
    pandas_table(d)
    basic_plot(d)
    d.a(href="#title", content='A link 2')
    return d

def basic_table(d:HtmlDoc):
    with d.table_el:
        with d.thead:
            with d.tr:
                d.td("Col 1")
                d.td("Col 2")
        for i in range(3):
            with d.tr:
                d.td(f"{i}-1")
                d.td(f"{i}-2")


def easy_table(d: HtmlDoc):
    d.easy_table([[f"{i}-{j}" for i in range(2)] for j in range(3)], columns=[f"Col {i}" for i in range(2)])
    d.easy_table([[f"{i}-{j}" for i in range(2)] for j in range(3)], columns=[f"Col {i}" for i in range(2)], clear_rows=True)
    d.easy_table([[f"{i}-{j}" for i in range(2)] for j in range(3)], columns=[f"Col {i}" for i in range(2)], clear_columns=True)
    d.easy_table([[f"{i}-{j}" for i in range(2)] for j in range(3)], columns=[f"Col {i}" for i in range(2)], clear_rows=True, clear_columns=True)

def pandas_table(d: HtmlDoc):
    import pandas as pd
    df = pd.DataFrame([[1,2,3],[3,4,5]], columns=('first', 'second', 'third'), index=('alpha', 'beta'))
    d.easy_table(df)
    d.easy_table(df, show_index=True)
    d.easy_table(df['first'])

def basic_plot(d: HtmlDoc):
    import matplotlib.pyplot as plt
    import numpy as np

    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    plt.plot(t, s)

    plt.gca().set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    plt.grid()
    d.easy_plot()
    d.easy_plot(render_as='raster')
    d.easy_plot(plt.gcf())


def test_document():
    d = make_standard_doc()
    r = d.render()
    with open('tests/outputs/test_document.html', 'w') as f:
        f.write(r)
    return d

def test_pdf():
    d = make_standard_doc()
    d.to_pdf("tests/outputs/test_document.pdf")

def test_extend():
    d = HtmlDoc()
    d.h1("First doc")
    d2 = HtmlDoc()
    d2.h1("Second doc")
    with d.div:
        d.extend(d2)
    result = d.get_body_internals()
    expected_result = "<h1>First doc</h1>\n<div><h1>Second doc</h1></div>"
    assert result == expected_result, result

if __name__ == '__main__':
    test_pdf()
    test_document()
    test_extend()