import sys
import docx


def dump(p):
    d = docx.Document(p)
    out = []
    body = d.element.body
    for el in body.iter():
        tag = el.tag.split('}')[-1]
        if tag == 'p':
            t = ''.join(n.text or '' for n in el.iter() if n.tag.split('}')[-1] == 't')
            if t.strip():
                out.append(t)
    for ti, t in enumerate(d.tables):
        out.append('--- TABLE %d ---' % ti)
        for r in t.rows:
            out.append(' | '.join(c.text.strip().replace('\n', ' / ') for c in r.cells))
    return '\n'.join(out)


for a in sys.argv[1:]:
    print('######## ' + a)
    print(dump(a))
