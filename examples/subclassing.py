# This workaround courtesy of https://docs.python-guide.org/writing/structure/
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from html_doc import HtmlDoc, easy_tag_maker

class CustomHtmlDoc(HtmlDoc):
    def get_default_css(self):
        from os.path import join, dirname
        contents = open(join(dirname(__file__), 'subclassed.css')).read()
        return [contents]

    outlined = easy_tag_maker('div', initial_classes=['outlined'])


if __name__ == '__main__':
    d = CustomHtmlDoc()
    d.h1("An example subclassed custom html doc")
    with d.outlined:
        d.p("Some text in an outline")
        d.p("Some text in an outline")
        d.p("Some text in an outline")

    d.to_html('examples/outputs/subclassed.html')