
import os
import re
import mistune
root = os.path.dirname(__file__)

known = []

features = [
    'table', 'fenced_code', 'footnotes',
    'autolink', 'strikethrough',
]
m = mistune.Markdown(features=features)


def render(folder, name):
    filepath = os.path.join(folder, name + '.text')
    with open(filepath) as f:
        content = f.read()

    html = m.parse(content)

    filepath = os.path.join(folder, name + '.html')
    with open(filepath) as f:
        result = f.read()

    html = re.sub(r'\s', '', html)
    result = re.sub(r'\s', '', result)
    for i, s in enumerate(html):
        if s != result[i]:
            begin = max(i - 30, 0)
            msg = '\n\n%s\n------Not Equal(%d)------\n%s' % (
                html[begin:i+30], i, result[begin:i+30]
            )
            raise ValueError(msg)


def listdir(folder):
    folder = os.path.join(root, folder)
    files = os.listdir(folder)
    files = filter(lambda o: o.endswith('.text'), files)
    names = map(lambda o: o[:-5], files)
    return folder, names


def test_extra():
    folder, names = listdir('extra')
    for key in names:
        yield render, folder, key


def test_normal():
    folder, names = listdir('cases')
    for key in names:
        yield render, folder, key


def test_no_table():
    filepath = os.path.join(root, 'extra', 'gfm_tables.text')
    with open(filepath) as f:
        content = f.read()

    assert '</table>' not in mistune.markdown(content)


def test_escape():
    ret = mistune.markdown('<div>**foo**</div>', escape=True)
    assert '&gt;' in ret
