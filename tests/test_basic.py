
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

    d.a(href="#title", content='A link 2')
    return d

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
    #test_extend()