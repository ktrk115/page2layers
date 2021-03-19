from pathlib import Path


def __load_snippet():
    out = {}
    js_dir = Path(__file__).with_name('javascript')
    for path in js_dir.glob('*.js'):
        script = ''
        with path.open() as f:
            for l in f:
                script += l.strip()
        out[path.stem] = script
    return out


snippet = __load_snippet()
