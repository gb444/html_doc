from typing import Iterable, Any, Optional, Union

def easy_table(self:'HtmlDoc',
               contents: Optional[Union[Iterable[Iterable[Any]],'DataFrame', 'Series']] = None,
               columns:Optional[Iterable] = None,
               footer:Optional[Iterable] = None,
               clear_rows=False,
               clear_columns=False,
               show_index=False):
    doc = self
    classes = []
    if clear_rows:
        classes.append('clear-rows')
    if clear_columns:
        classes.append('clear-columns')
    is_df = any([t.__name__ in ['DataFrame'] for t in type(contents).__mro__])
    is_series = any([t.__name__ in ['Series'] for t in type(contents).__mro__])
    if is_df or is_series:
        frame = contents
        if is_df:
            columns = list(frame.columns)
            contents = frame.values.tolist()
        else:
            columns = [frame.name]
            contents = [[row] for row in frame.values.tolist()]
        if show_index:
            index = frame.index.tolist()
            columns = ['Index'] + columns
            contents = [[index_]+row for index_,row in zip(index, contents)]

    with doc.table_el(classes=classes):
        if columns is not None:
            with doc.thead:
                with doc.tr:
                    for column in columns:
                        doc.td(str(column))
        if contents is not None:
            with doc.tbody:
                for row in contents:
                    with doc.tr:
                        for cell in row:
                            doc.td(str(cell))
        if footer is not None:
            with doc.tfoot:
                with doc.tr:
                    for column in footer:
                        doc.td(str(column))

