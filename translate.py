import subprocess as sub
import os

outfile = 'LessWrong Sequences.rst'

DEPTH_CHAR = '=-:"~^_*'
outf = open(outfile, 'w')

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
            newtext = (title + '\n' +
                    mktitlebar(depth, title) + '\n' +
                    text[titleindex:])
            outf.write(newtext)
            os.remove(outrst)

appendWalk(indir, 0)
