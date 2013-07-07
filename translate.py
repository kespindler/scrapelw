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

def appendWalk(apath, depth):
    if os.path.isdir(apath):
        titles_fpath = os.path.join(apath, 'titles.txt')
        if not os.path.exists(titles_fpath):
            return
        with open(titles_fpath) as f:
            titles = [title.strip().replace('_', ' ') 
                    for title in f.readlines()]
        files = os.listdir(apath)
        files.remove('titles.txt')
        for l in files:
            num = os.path.splitext(l)[0]
            title = titles[int(num)]
            outf.write(title + '\n' +
                    mktitlebar(depth, title) + 
                    '\n\n')
            appendWalk(os.path.join(apath, l), depth+1)
    elif apath.endswith('html'):
        outrst = apath + '.rst'
        sub.call(['pandoc', '-o', outrst, apath])
        with open(outrst) as f:
            text = f.read()
        outf.write(text)
        os.remove(outrst)

appendWalk(indir, 0)
