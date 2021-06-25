# pdfkit weasyprint
from enum import Enum, auto
import tempfile
from typing import Optional

try:
    import pdfkit
except:
    pdfkit = None

try:
    import weasyprint
except:
    weasyprint = None

class ExportLibraryPreference(Enum):
    PdfkitPreference = auto()
    WeasyprintPreference = auto()
    PdfkitOnly = auto()
    WeasyprintOnly = auto()

class PageSizes(Enum):
    A4 = 'A4'
    Letter = 'Letter'

class ExportSettings():
    def __init__(self, page_size=PageSizes.A4,
                 margin_top='0.78in', margin_bottom='0.78in', margin_left='0.78in', margin_right='0.78in',
                 footer_page_number=True, footer_title=False,
                 explicit_overrides = None):
        self.page_size = page_size or PageSizes.A4
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.footer_page_number = footer_page_number
        self.footer_title = footer_title

        self.explicit_overrides = explicit_overrides

def d_set(d, k, v):
    if v is not None:
        d[k] = v


"""
Headers And Footer Options:
      --footer-center <text>          Centered footer text
      --footer-font-name <name>       Set footer font name (default Arial)
      --footer-font-size <size>       Set footer font size (default 12)
      --footer-html <url>             Adds a html footer
      --footer-left <text>            Left aligned footer text
      --footer-line                   Display line above the footer
      --no-footer-line                Do not display line above the footer
                                      (default)
      --footer-right <text>           Right aligned footer text
      --footer-spacing <real>         Spacing between footer and content in mm
                                      (default 0)
      --header-center <text>          Centered header text
      --header-font-name <name>       Set header font name (default Arial)
      --header-font-size <size>       Set header font size (default 12)
      --header-html <url>             Adds a html header
      --header-left <text>            Left aligned header text
      --header-line                   Display line below the header
      --no-header-line                Do not display line below the header
                                      (default)
      --header-right <text>           Right aligned header text
      --header-spacing <real>         Spacing between header and content in mm
                                      (default 0)
      --replace <name> <value>        Replace [name] with value in header and
                                      footer (repeatable)
                                      
    Footers And Headers:
  Headers and footers can be added to the document by the --header-* and
  --footer* arguments respectively.  In header and footer text string supplied
  to e.g. --header-left, the following variables will be substituted.

   * [page]       Replaced by the number of the pages currently being printed
   * [frompage]   Replaced by the number of the first page to be printed
   * [topage]     Replaced by the number of the last page to be printed
   * [webpage]    Replaced by the URL of the page being printed
   * [section]    Replaced by the name of the current section
   * [subsection] Replaced by the name of the current subsection
   * [date]       Replaced by the current date in system local format
   * [isodate]    Replaced by the current date in ISO 8601 extended format
   * [time]       Replaced by the current time in system local format
   * [title]      Replaced by the title of the of the current page object
   * [doctitle]   Replaced by the title of the output document
   * [sitepage]   Replaced by the number of the page in the current site being converted
   * [sitepages]  Replaced by the number of pages in the current site being converted
                                      """

def export_with_pdfkit(doc, output_path, options:Optional[ExportSettings]=None):
    popts = {}#{'quiet':''}
    if options is None:
        options = ExportSettings()

    d_set(popts, 'page-size', options.page_size.value)
    d_set(popts, 'margin-top', options.margin_top)
    d_set(popts, 'margin-bottom', options.margin_bottom)
    d_set(popts, 'margin-left', options.margin_left)
    d_set(popts, 'margin-right', options.margin_right)
    if options.footer_page_number:
        popts['footer-right'] = "Page [page] of [topage]"
    if options.footer_title:
        popts['footer-left'] = "[title]"

    if options.explicit_overrides is not None:
        popts.update(options.explicit_overrides)


    pdfkit.from_string(doc.render(), output_path, options=popts)


def export_with_weasyprint(doc, output_path, options:Optional[ExportSettings]=None):
    if options is None:
        options = ExportSettings()
    footers = ""
    if options.footer_title:
        footers += f"""
            @bottom-left {{
                content: string(title);
            }}
"""
    if options.footer_page_number:
        footers += f"""
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
            }}
"""
    styles = f"""
    @page {{
        margin-left:{options.margin_left};
        margin-right:{options.margin_right};
        margin-top:{options.margin_top};
        margin-bottom:{options.margin_bottom};
        size: {options.page_size.value};
        {footers}
    }}
    """
    weasyprint.HTML(string=doc.render(with_styles=[styles])).write_pdf(output_path)

def export_pdf_to(doc, output_path,
                  options=None,
                  export_library_option=ExportLibraryPreference.WeasyprintPreference):
    if pdfkit is None and weasyprint is None:
        raise ModuleNotFoundError("Neither pdfkit nor weasyprint are available - export failed")
    if export_library_option == ExportLibraryPreference.PdfkitOnly:
        if pdfkit is None:
            raise ModuleNotFoundError("pdfkit not found - export failed with option PdfkitOnly")
        else:
            export_with_pdfkit(doc, output_path, options=options)
    elif export_library_option == ExportLibraryPreference.PdfkitPreference:
        if pdfkit is None:
            export_with_weasyprint(doc, output_path, options=options)
        else:
            export_with_pdfkit(doc, output_path)
    elif export_library_option == ExportLibraryPreference.WeasyprintPreference:
        if weasyprint is None:
            export_with_pdfkit(doc, output_path, options=options)
        else:
            export_with_weasyprint(doc, output_path, options=options)
    elif export_library_option == ExportLibraryPreference.WeasyprintOnly:
        if weasyprint is None:
            raise ModuleNotFoundError("weasyprint not found - export failed with option WeasyprintOnly")
        else:
            export_with_weasyprint(doc, output_path, options=options)
