from pathlib import Path


def __load_snippet():
    out = {}
    js_dir = Path(__file__).with_name('javascript')
    for path in js_dir.glob('*.js'):
        with path.open() as f:
            out[path.stem] = ''.join(f)
    return out


snippet = __load_snippet()
