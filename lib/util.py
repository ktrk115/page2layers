import json
import requests
import tempfile
import imagehash
from PIL import Image
from anytree.exporter import UniqueDotExporter, DictExporter

requests.urllib3.disable_warnings()


class BrokenLinkError(Exception):
    pass


def check_broken_link(url, headers=None, return_content=False):
    with requests.get(url, headers=headers,
                      verify=False, timeout=(3.05, 27)) as res:
        if res.status_code != 200:
            msg = f'[{res.status_code}] {url}'
            raise BrokenLinkError(msg)

        if return_content:
            return res.content


def get_image_hash(img):
    if isinstance(img, imagehash.ImageHash):
        return img
    else:
        img = img.convert('RGB')
        return imagehash.phash(img, hash_size=16)


def detach(element):
    # tree
    children = list(element.children)
    parent = element.parent
    p_children = list(parent.children)
    i = p_children.index(element)
    parent.children = p_children[:i] + children + p_children[i + 1:]

    # context tree
    if hasattr(element, 'ctx_children'):
        children = element.ctx_children
        parent = element.ctx_parent
        for c in children:
            c.ctx_parent = parent

        p_children = parent.ctx_children
        i = p_children.index(element)
        parent.ctx_children = p_children[:i] + children + p_children[i + 1:]


def remove_redundant_elements(root, visible_elements):
    elements = root.descendants

    visual_contributors = set(visible_elements)
    for e in visible_elements:
        for ancestor in e.ancestors:
            visual_contributors.add(ancestor)

    for e in elements:
        if e not in visual_contributors:
            detach(e)

    return root


def get_reconstruct_image(root, window_size):
    recon = Image.new('RGB', window_size, color=(255, 255, 255))
    elements = [root] + list(root.descendants)
    visible_elements = [e for e in elements if e.is_visible]
    visible_elements.sort(key=lambda e: e.z_order)
    for element in visible_elements:
        img, box = element.img, element.box
        x, y = int(round(box[0])), int(round(box[1]))
        recon.paste(img, (x, y), mask=img)
    return recon


def get_tree_image(root):
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = tmpdir + '/tree.png'
        UniqueDotExporter(root,
                          nodeattrfunc=lambda e:
                          f'label="[{e.index}] {e.name}"'
                          ).to_picture(out_path)
        with open(out_path, 'rb') as f:
            img = Image.open(f).copy()
    return img


def save_metadata(root, out_path):
    skip_attrs = set(['ctx_parent', 'ctx_children', 'base_element',
                      'img', 'color_style'])
    exporter = DictExporter(attriter=lambda attrs:
                            [(k, v) for k, v in attrs if k not in skip_attrs])
    with open(out_path, 'w') as f:
        json.dump(exporter.export(root), f, indent=2)
