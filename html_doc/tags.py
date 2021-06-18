from os.path import splitext

from .html_format_utils import base64_encode, get_element_style_string, get_classes_string, get_id_string
from .tag_obj import TagDispatcher, BasicTagTemplate, tag_magic, FunctionTagTemplate

def easy_tag_maker(tag, initial_classes=None, initial_id=None):
    return tag_magic(BasicTagTemplate(tag, initial_classes, initial_id))

def easy_function_tag(function):
    return tag_magic(FunctionTagTemplate(function))

h1 = easy_tag_maker('h1')
h2 = easy_tag_maker('h2')
h3 = easy_tag_maker('h3')
h4 = easy_tag_maker('h4')

p = easy_tag_maker('p')
ital = easy_tag_maker('i')
bold = easy_tag_maker('b')
underline = easy_tag_maker('u')

div = easy_tag_maker('div')

ul = easy_tag_maker('ul')
ol = easy_tag_maker('ol')
li = easy_tag_maker('li')


page_break = easy_tag_maker('div', initial_classes=['page_break'])

table_el = easy_tag_maker('table', initial_classes=['default-style'])
thead = easy_tag_maker('thead')
tbody = easy_tag_maker('tbody')
tfoot = easy_tag_maker('tfoot')
tr = easy_tag_maker('tr')
td = easy_tag_maker('td')
th = easy_tag_maker('th')


@easy_function_tag
def raw(content):
    return content

@easy_function_tag
def br():
    return '<br/>'

@easy_function_tag
def hline():
    return '<hr/>'

def get_content_uri(type_, content):
    data_uri_templ = 'data:image/{};base64,{}'
    return data_uri_templ.format(type_, base64_encode(content))

@easy_function_tag
def img(png=None, jpg=None, svg=None, path=None, alt=None, width=None, height=None, classes=None, id_=None):
    if png is not None:
        content = get_content_uri('png', png)
    elif jpg is not None:
        content = get_content_uri('jpg', jpg)
    elif svg is not None:
        content = get_content_uri('svg+xml', svg)
    elif path is not None:
        filename, file_extension = splitext(path)
        extension_map = {
            'png': 'png',
            'jpg': 'jpg',
            'jpeg': 'jpg',
            'svg': 'svg+xml'
        }
        file_content = open(path, 'rb').read()
        content = get_content_uri(extension_map[file_extension.lower().replace('.','')], file_content)
    else:
        raise TypeError("One of png, jpg or svg should be specified")
    altf = '' if alt is None else f' alt="{alt}"'
    styles = get_element_style_string({'width':width, 'height':height})
    return f'<img {get_classes_string(classes)}{get_id_string(id_)} src="{content}"{altf}{styles}/>'

@easy_function_tag
def anchor(id_):
    return f"<div id=\"{id_}\" class=\"empty\"></div>"

@easy_function_tag
def svg(content: str):
    return content

@easy_function_tag
def a(href, content=''):
    return f'<a href="{href}">{{}}</a>', content

