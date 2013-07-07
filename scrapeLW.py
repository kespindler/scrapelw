import lxml.etree as lxml
from urlparse import urlparse
import simplejson as json
import re

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

def save_progress():
    with open('out.json', 'w') as f:
        f.write(json.dumps(STORAGE))
domain = 'http://wiki.lesswrong.com'
def get_links_from_toc(url, section, storage):
    urltup = urlparse(url)
    if not urltup.netloc:
        url = domain + url
    tree = lxml.parse(url, parser=lxml.HTMLParser())
    ul = tree.xpath('//table[@id="toc"]/tr/td/ul/li[%d]/ul' % (section,))[0]
    titles = [li[0].get('href') for li in ul.getchildren()]
    for t in titles: 
        a = tree.xpath('//span[@id="'+t[1:]+'"]/a')[0]
        url = a.get('href')
        if urltup.path == '/wiki/Sequences':
            storage[t] = {}
            print 'Exploring', t
            get_links_from_toc(url, 1, storage[t])
        else: # assumed to be 'lesswrong.com'
            title, html = parse_article(url)
            storage[title] = html
            print 'Stored', title
            save_progress()

STORAGE = {}
get_links_from_toc('/wiki/Sequences', 4, STORAGE)
print 'Complete.'
