import lxml.etree as lxml
from urlparse import urlparse
import simplejson as json
import re
import os

def parse_article(url):
    tree = lxml.parse(url, parser=lxml.HTMLParser())
    head = tree.xpath('//h1')[0]
    title = head[0].text.strip()
    body = tree.xpath('//div[starts-with(@id,"entry")]')[0]
    children = body.getchildren()
    for child in children[-3:]:
        body.remove(child)
    html = lxml.tostring(body)
    return title, html

domain = 'http://wiki.lesswrong.com'
outdir = 'out'
os.mkdir(outdir)

def get_links_from_toc(url, section, path):
    urltup = urlparse(url)
    if not urltup.netloc:
        url = domain + url
    tree = lxml.parse(url, parser=lxml.HTMLParser())
    ul = tree.xpath('//table[@id="toc"]/tr/td/ul/li[%d]/ul' % (section,))[0]
    titles = [li[0].get('href') for li in ul.getchildren()]
    try:
        for i, t in enumerate(titles): 
            title = t[1:]
            a = tree.xpath('//span[@id="'+title+'"]/a')[0]
            newurl = a.get('href')
            if urltup.path == '/wiki/Sequences':
                fpath = os.path.join(path, title)
                os.mkdir(fpath)
                print 'Exploring', title
                get_links_from_toc(newurl, 1, fpath)
            else: # assumed to be 'lesswrong.com'
                try:
                    title, html = parse_article(newurl)
                    #fname = "".join(x for x in title if x.isalnum())
                    with open(os.path.join(path, '%02d.html'%i), 'w') as f:
                        f.write(title + '\n')
                        f.write(html)
                    print 'Stored', title
                except:
                    print 'Failed on2', newurl
    except:
        print "failed on", url, newurl

get_links_from_toc('/wiki/Sequences', 4, outdir)
print 'Complete.'
