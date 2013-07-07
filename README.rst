Prequisites
===========

#. A few python libraries.
#. ``pandoc``
#. ```kindlegen`` <http://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211>_`, if you want to read on your kindle. Install: go to the link, unzip the download, and just drag it somewhere into your path. bbbb

Instructions
============

#. Run ``python -u scrapeLW.py | tee result.log``. This does the crawling, (``-u`` makes python unbuffered) and allows you to see stdout while it runs and simultaneously pipe it to ``result.log``.
#. This creates a large directory structure rooted at ``out/``, which represents what it found while crawling.
#. Run ``python translate.py``. This will create a very large rst file.

#. *(Optional)* Trying to run ``rst2html.py`` on it gives me a few errors. Fix these manually, I haven't figured out how to do it yet. You can preview it here if you'd like.

Using pandoc, this rst file can be converted into pretty much anything. I like reading on my Kindle:

#. Run ``pandoc -o lesswrong.epub lesswrong.rst``.
#.



