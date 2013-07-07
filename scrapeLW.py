import lxml.etree as lxml
from urlparse import urlparse
import simplejson as json
import re
import os

PARSER = lxml.HTMLParser(encoding='utf8')

DOMAIN = 'wiki.lesswrong.com'
outdir = 'out'
try:
    os.mkdir(outdir)
except:
    pass

def parse_article(url):
    tree = lxml.parse(url, parser=PARSER)
    head = tree.xpath('//h1')[0]
    title = head[0].text.strip()
    body = tree.xpath('//div[starts-with(@id,"entry")]/div/div/div')[0]
    children = body.getchildren()

    #remove nav headers
    for p in reversed(children):
        if p.text and (p.text.startswith('Next post:') or
                p.text.startswith('Previous post:') or
                p.text.startswith('Part of the sequence')):
            body.remove(p)
        elif p.text == u'\xa0':
            break

    #strip out images because we don't handle them yet..
    imgs = body.xpath('.//img')
    for i in imgs:
        p = i.getparent()
        while 1:
            if p.tag == 'p':
                p.remove(i)
                break
            i=p
            p=i.getparent()

    html = lxml.tostring(body)
    return title, html

hotstart = None#'How_To_Actually_Change_Your_Mind' #only works on top level at the moment
def get_links_from_toc(url, section, path):
    if not url.startswith('http'):
        url = 'http://' + DOMAIN + url
    print url
    global hotstart
    tree = lxml.parse(url, parser=PARSER)
    ul = tree.xpath('//table[@id="toc"]/tr/td/ul/li[%d]/ul' % (section,))[0]
    titles = [li[0].get('href') for li in ul.getchildren()]
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
            if not urlparse(newurl).netloc:
                fpath = os.path.join(path, '%02d'%i)
                with open(os.path.join(path, 'titles.txt'), 'a') as f:
                    f.write(title + '\n')
                os.mkdir(fpath)
                print 'Exploring', title
                try:
                    url = 'http://' + urlparse(url).netloc + newurl
                    get_links_from_toc(url, 1, fpath)
                except Exception as e:
                    print 'Failed on3', newurl
                    print e
            else: # assumed to be 'lesswrong.com'
                #try:
                if 1:
                    title, html = parse_article(newurl)
                    #fname = "".join(x for x in title if x.isalnum())
                    with open(os.path.join(path, '%02d.html'%i), 'w') as f:
                        f.write(html)
                    with open(os.path.join(path, 'titles.txt'), 'a') as f:
                        f.write(title + '\n')
                    print 'Stored', title
                #except:
                #    print 'Failed on2', newurl
    #except:
    #    print "failed on", url

get_links_from_toc('http://'+DOMAIN + '/wiki/Sequences', 4, outdir)
print 'Complete.'
