import subprocess as sub
import os
import lxml.etree as lxml

outfile = 'LessWrong Sequences.rst'

DEPTH_CHAR = '=-:"~^_*'
outf = open(outfile, 'w')
outf.write('.. contents::\n\n')

indir = 'out'
def mktitlebar(depth, title):
    return DEPTH_CHAR[depth]*len(title)

def appendWalk(adir, depth):
    for l in os.listdir(adir):
        path = os.path.join(adir, l)
        if os.path.isdir(path):
            title = l[2:]
            titlebar = mktitlebar(depth, title)
            outf.write(title +'\n' + titlebar + '\n\n')
            appendWalk(path, depth+1)
        elif l.endswith('html'):
            outrst = l + '.rst'
            sub.call(['pandoc', '-o', outrst, path])
            with open(outrst) as f:
                text = f.read()
            titleindex = text.find('\n')
            title = text[:titleindex]
            body = text[titleindex:]
            tree = lxml.fromstring(body, parser=lxml.HTMLParser())
            imgs = tree.xpath('//img')
            for i in imgs:
                p = i.getparent()
                while 1:
                    if p.tag == 'p':
                        p.remove(i)
                        break
                    i=p
                    p=i.getparent()
            body = lxml.tostring(tree)
            newtext = (title + '\n' +
                    mktitlebar(depth, title) + '\n' +
                    body)
            outf.write(newtext)
            os.remove(outrst)

appendWalk(indir, 0)
