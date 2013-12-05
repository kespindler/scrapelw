# Download Links

The books can be found in this [Dropbox Folder](https://www.dropbox.com/sh/y3uv8bvyhf9eu5h/8N-V_wf4w6>). `epub`, `mobi`, `html`, and `rst` are available there.

# Prequisites

1. A few python libraries. `lxml` provides most of the heavy-lifting.
2. [pandoc](http://johnmacfarlane.net/pandoc/)
3. [calibre](http://calibre-ebook.com/), to convert to mobi.

Instructions
============

1. Run `python -u scrapeLW.py | tee result.log`. This does the crawling, (`-u` makes python unbuffered) and allows you to see stdout while it runs and simultaneously pipe it to `result.log`.
2. This creates a large directory structure rooted at `out/`, which represents what it found while crawling.
3. Run `python translate.py`. This will create a very large rst file.

4. *(Optional)* Trying to run `rst2html.py` on it gives me a few errors. Fix these manually, I haven't figured out how to do it automatically yet. This step allows you to preview the result in the browser.

Using pandoc, this rst file can be converted into pretty much anything. I like reading on my Kindle:

5. Run `pandoc -t epub -o lesswrong.epub --smart --toc --epub-stylesheet=epub.css lesswrong.rst`.
6. Launch up calibre and import the epub. Use Calibre to convert it to mobi.

Known Issues
============

1. This works really well on some of the sequences, but only sort of well at other times. Working on this. And pull-requests are welcome.
