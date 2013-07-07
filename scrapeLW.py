import lxml.etree as lxml
from urlparse import urlparse
import simplejson as json
import re
import os

def parse_article(url):
    tree = lxml.parse(url, parser=lxml.HTMLParser())
    head = tree.xpath('//h1')[0]
    title = head[0].text.strip()
    body = tree.xpath('//div[starts-with(@id,"entry")]/div/div/div')[0]
    children = body.getchildren()
    for p in reversed(children):
        if p.text and (p.text.startswith('Next post:') or
                p.text.startswith('Previous post:') or
                p.text.startswith('Part of the sequence')):
            body.remove(p)
        elif p.text == u'\xa0':
            break
    html = lxml.tostring(body)
    return title, html

domain = 'wiki.lesswrong.com'
outdir = 'out'
try:
    os.mkdir(outdir)
except:
    pass

hotstart = 'A_Human.27s_Guide_to_Words' #only works on top level at the moment
def get_links_from_toc(url, section, path):
    if not url.startswith('http'):
        url = 'http://' + domain + url
    global hotstart
    tree = lxml.parse(url, parser=lxml.HTMLParser())
    ul = tree.xpath('//table[@id="toc"]/tr/td/ul/li[%d]/ul' % (section,))[0]
    titles = [li[0].get('href') for li in ul.getchildren()]
    #try:
    if 1:
        for i, t in enumerate(titles): 
            title = t[1:]
            if hotstart:
                if title != hotstart:
                    continue
                else:
                    hotstart = None
            a = tree.xpath('//span[@id="'+title+'"]/a')[0]
            newurl = a.get('href')
            if urlparse(newurl).netloc == domain:
                fpath = os.path.join(path, '%02dtitle'%i)
                os.mkdir(fpath)
                print 'Exploring', title
                try:
                    get_links_from_toc(newurl, 1, fpath)
                except:
                    print 'Failed on3', newurl
            else: # assumed to be 'lesswrong.com'
                #try:
                if 1:
                    title, html = parse_article(newurl)
                    #fname = "".join(x for x in title if x.isalnum())
                    with open(os.path.join(path, '%02d.html'%i), 'w') as f:
                        f.write(title + '\n')
                        f.write(html)
                    print 'Stored', title
                #except:
                #    print 'Failed on2', newurl
    #except:
    #    print "failed on", url

get_links_from_toc('http://'+domain + '/wiki/Sequences', 4, outdir)
print 'Complete.'
