import base64

def smart_conditional_tab_in(rendered):
    if rendered.count('<') > 2:
        NL = '\n'
        sp = rendered.split(NL)
        TAB = '\t'
        return f"\n{NL.join([TAB + bit for bit in sp])}\n"
    return rendered


def base64_encode(blurb):
    if not isinstance(blurb, bytes):
        blurb = blurb.encode('utf-8')
    return base64.b64encode(blurb).decode('ascii')


def get_element_style_string(styles):
    final_styles = [(key, value.replace('"', '\\"')) for key, value in styles.items() if value is not None]
    if len(final_styles) > 0:
        return ' style="{}"'.format(' '.join([f'{key}:{value};' for key, value in final_styles]))
    else:
        return ""


def get_classes_string(classes):
    if classes is None or len(classes) == 0:
        return ''
    else:
        return ' class="{}"'.format(' '.join(classes))


def get_id_string(id_):
    if id_ is not None:
        return ' id="{}"'.format(id_)
    else:
        return ''


def get_attributes_string(attrs):
    r = ' '.join([f'{key}="{value}"' for key, value in attrs.items() if value is not None])
    if len(r) > 0:
        return ' '+r
    else:
        return ''
