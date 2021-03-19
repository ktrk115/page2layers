import bs4
from lib.element import Element, PseudoElement

SKIP_KEYS = ['html > head', 'style', 'script', 'svg >', 'video > source']


def get_inner_html(source):
    inner_html = ''
    soup = bs4.BeautifulSoup(source, 'html.parser')
    for child in soup.html.children:
        inner_html += str(child)
    return inner_html


def elem2selector(elem):
    def _elem2selector(elem, out):
        if elem.name != '[document]':
            prev_siblings = elem.find_previous_siblings(elem.name)
            next_siblings = elem.find_next_siblings(elem.name)
            if len(prev_siblings) + len(next_siblings) > 0:
                name = elem.name + f':nth-of-type({len(prev_siblings) + 1})'
                out.append(name)
            else:
                out.append(elem.name)
            _elem2selector(elem.parent, out)
        return ' > '.join(out[::-1])
    return _elem2selector(elem, list())


def get_text(elem):
    strings = []
    for child in elem.children:
        if type(child) == bs4.element.NavigableString:
            string = child.strip()
            if len(string) > 0:
                strings.append(string)
    return ' '.join(strings)


def build_element_tree(source):
    def _build_element_tree(element, e_par, e_ctx):
        if isinstance(element, bs4.element.Tag):
            selector = elem2selector(element)
            for key in SKIP_KEYS:
                if key in selector:
                    return

            e = Element(selector, get_text(element),
                        element.attrs, e_par, e_ctx)

            if e.find().is_displayed():
                e_ctx = e if e.is_context else e_ctx

                if e.has_before:
                    PseudoElement(e, e_ctx, 'before')

                for child in element.children:
                    _build_element_tree(child, e, e_ctx)

                if e.has_after:
                    PseudoElement(e, e_ctx, 'after')

            else:
                e.parent.children.remove(e)

    soup = bs4.BeautifulSoup(source, 'html.parser')

    root = soup.html
    e_root = Element('html', get_text(root), root.attrs)

    if not e_root.has_background:
        root = soup.html.body
        e_root = Element('html > body', get_text(root), root.attrs)

    for child in root.children:
        _build_element_tree(child, e_root, e_root)

    return e_root


def get_ordered_elements(root):
    def get_elements(element):
        out = []

        element.ctx_children.sort(key=lambda e: e.z_value)
        elements = element.ctx_children

        if not element.has_background and len(elements) > 0:
            i = 0
            for e in elements:
                if e.z_value < 0:
                    i += 1
                else:
                    break
            elements = elements[:i] + [element] + elements[i:]
        else:
            elements = [element] + elements

        for e in elements:
            if e != element and e.is_context:
                out.append(get_elements(e))
            else:
                out.append(e)

        return out

    def flatten(l):
        for e in l:
            if isinstance(e, list):
                yield from flatten(e)
            else:
                yield e

    return flatten(get_elements(root))
