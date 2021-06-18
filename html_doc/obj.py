from typing import Iterable

from .templates import document
from .html_format_utils import smart_conditional_tab_in

class HtmlDoc():
    def __init__(self, title=None, css=None, include_default_styles=True):
        self.head = []
        self.stack = [[]]
        self.poppers = []
        self.title = title
        self.provided_css = css
        self.include_default_styles = include_default_styles
        self._tag_joiner = lambda x: '\n'.join(x)
        self.custom_header=None
        self.custom_footer=None
    
    
    ### Tags
    from .tags import h1, h2, h3, h4
    from .tags import p, ital, underline, bold
    from .tags import div, raw, a
    from .tags import ul, li, ol
    from .tags import img, svg
    from .tags import br, page_break, hline, anchor
    from .tags import table_el, thead, tbody, tfoot, td, tr, th

    from .table import easy_table
    from .figure import easy_plot

    ### Clever bits
    def remove_element_from_top(self, tag):
        "Removes the tag from the top of the top stack if the tag matches"
        cur_stack = self.stack[-1]
        if len(cur_stack) > 0 and tag is cur_stack[-1]:
            inner = cur_stack.pop()
            return True
        return False

    def append(self, tag):
        if not hasattr(tag, 'render'):
            raise NotImplementedError(f"This tag cannot be added to the stack as it cannot have render called on it {type(tag)}")
        cur_stack = self.stack[-1]
        self.remove_element_from_top(tag.inner)
        cur_stack.append(tag)
        return tag

    def extend(self, other):
        if isinstance(other, HtmlDoc):
            flat = other.flattened()
            self.stack[-1].extend(flat)
        elif isinstance(other, Iterable):
            self.stack[-1].extend(other)
        else:
            raise NotImplementedError("Can only extend with another document or an iterable")

    def push(self, wrapper):
        self.poppers.append(wrapper)
        self.stack.append([])

    def pop(self):
        latest = self.stack.pop()
        wrapper = self.poppers.pop()
        self.stack[-1].append(wrapper(latest))

    def virtual_pop(self, stack, poppers):
        if len(poppers) > 0:
            stack[-2].append(poppers[-1](stack[-1]))
            return stack, poppers
        return None
    

    ### Rendering bits    
    def flattened(self):
        stack, poppers = list(self.stack), list(self.poppers)
        while len(poppers) > 0:
            r = self.virtual_pop(stack, poppers)
            if r is not None:
                stack, poppers = r
        return stack[0]

    def get_default_css(self):
        from os.path import join, dirname
        contents = open(join(dirname(__file__), 'static/default.css')).read()
        return [contents]

    def get_styles(self):
        styles = self.provided_css or []
        if not isinstance(styles, list):
            styles = [styles]
        if self.include_default_styles:
            styles = self.get_default_css() + styles
        return styles

    def get_body_internals(self):
        flattened = self.flattened()
        body = self._tag_joiner([tag.render(self._tag_joiner) for tag in flattened])
        return body


    def render(self):
        body = self.get_body_internals()
        styles_elements = '\n'.join([f'<style>\n{css}\n</style>' for css in self.get_styles()])
        head = f"""<title>{self.title}</title>
          <meta name="description" content="">
          <meta name="author" content="">
          {styles_elements}
        """
        return document.format(body=smart_conditional_tab_in(body), head=head)


    def to_pdf(self, path):
        from .pdf import export_pdf_to
        export_pdf_to(self, path)

    def to_html(self, path):
        r = self.render()
        with open('tests/outputs/test_document.html', 'w') as f:
            f.write(r)