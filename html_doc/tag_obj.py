from html import escape
from .html_format_utils import smart_conditional_tab_in, get_element_style_string


class BaseTagTemplate():
    pass

class BaseTagInstance:
    def __init__(self, outer, inner, escape=True, parent=None):
        self.outer = outer
        self.inner = inner
        self.escape = escape
        self.parent = parent
    
    # These context manager functions exist so one can envoke a tag with some settings like
    # with d.p(classes=['test']):
    #     d.ital("Text")
    # and have this work
    def __enter__(self):
        self.parent.remove_element_from_top(self)
        return self.parent.push(self)

    def __exit__(self, type, value, traceback):
        return self.parent.pop()

    def __call__(self, inner):
        self.inner = inner
        return self

    def combine_inner_outer(self, rendered_inner):
        rendered_inner = smart_conditional_tab_in(rendered_inner)
        if '{}' in self.outer:
            return self.outer.format(rendered_inner)
        else:
            return self.outer

    def render(self, tag_joiner):
        inner = self.inner
        if not isinstance(inner, list):
            inner = [inner]
        semi_rendered_inner = []
        for bit in inner:
            if isinstance(bit, BaseTagInstance):
                semi_rendered_inner.append(bit.render(tag_joiner))
            else:
                bit_ = str(bit)
                if self.escape:
                    bit_ = escape(bit_)
                semi_rendered_inner.append(bit_)
        rendered_inner = tag_joiner(semi_rendered_inner)
        return self.combine_inner_outer(rendered_inner)

    def __str__(self):
        return self.outer.format(str(self.inner))

class BasicTagTemplate(BaseTagTemplate):
    def __init__(self, tag, initial_classes = None, initial_id=None, initial_styles=None, escape=True):
        self.tag = tag
        self.initial_classes = initial_classes or []
        self.initial_id = initial_id
        self.initial_styles = initial_styles or {}
        self.escape = escape

    def get_templ(self, classes, id_, styles):
        classesf = ''
        if len(classes) > 0:
            classesf = ' class="{}"'.format(' '.join(classes))
        idf = ''
        if id_ is not None:
            idf = ' id="{}"'.format(id_)
        outer = f"<{self.tag}{idf}{classesf}{get_element_style_string(styles)}>{{}}</{self.tag}>"
        return outer

    def instance(self, inner='', classes=None, id_=None, styles=None, escape=None, parent=None):
        classes = classes or []
        classes += self.initial_classes
        escape = escape or self.escape
        styles_ = dict(self.initial_styles)
        styles_.update(styles or {})
        id_ = id_ or self.initial_id
        outer = self.get_templ(classes, id_, styles_)
        return BaseTagInstance(outer, inner, escape=escape, parent=parent)

    def __str__(self):
        return self.get_templ(self.initial_classes, self.initial_id, self.initial_styles)


class FunctionTagTemplate(BaseTagTemplate):
    def __init__(self, function):
        self.function = function

    def instance(self, *args, parent=None, **kwargs):
        result = self.function(*args, **kwargs)
        if isinstance(result, tuple):
            return BaseTagInstance(*result, escape=False, parent=parent)
        return BaseTagInstance(result, '', escape=False, parent=parent)


class TagDispatcher:
    def __init__(self, parent, tag_template):
        self.parent = parent
        self.tag_template = tag_template

    def __call__(self, *args, **kwargs):
        return self.parent.append(self.tag_template.instance(*args, **kwargs, parent=self.parent))

    def __enter__(self):
        return self.parent.push(self.tag_template.instance)

    def __exit__(self, type, value, traceback):
        return self.parent.pop()


def tag_magic(tag_template):
    # Tags work by being properties on the class, meaning they can be called without adding brackets
    # This is only done to make the aesthetics of context managers make more sense
    # The property, when accessed, gives the parent document via the self argument, which the TagDispatcher uses
    # To know how to manipulate its parent via the append, push and pop methods.
    # When TagDispatcher itself is called it acts like a function on the parent that appends that tag
    return property(lambda doc: TagDispatcher(doc, tag_template))