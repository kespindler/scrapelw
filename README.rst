Download Links
==============

The books can be found in this `Dropbox Folder <https://www.dropbox.com/sh/y3uv8bvyhf9eu5h/8N-V_wf4w6>`_. ``epub``, ``mobi``, ``html``, and ``rst`` are available there.

Prequisites
===========

#. A few python libraries. ``lxml`` provides most of the heavy-lifting.
#. `pandoc <http://johnmacfarlane.net/pandoc/>`_
#. `kindlegen <http://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211>`_, if you want to read on your kindle. Install: go to the link, unzip the download, and just drag it somewhere into your path.

Instructions
============

#. Run ``python -u scrapeLW.py | tee result.log``. This does the crawling, (``-u`` makes python unbuffered) and allows you to see stdout while it runs and simultaneously pipe it to ``result.log``.
#. This creates a large directory structure rooted at ``out/``, which represents what it found while crawling.
#. Run ``python translate.py``. This will create a very large rst file.

#. *(Optional)* Trying to run ``rst2html.py`` on it gives me a few errors. Fix these manually, I haven't figured out how to do it automatically yet. This step allows you to preview the result in the browser.

Using pandoc, this rst file can be converted into pretty much anything. I like reading on my Kindle:

#. Run ``pandoc -o lesswrong.html lesswrong.rst``.
#. Run ``kindlegen lesswrong.html``. Note there is a major bug right now - I can't figure out how to get the rst table of contents to be active within the mobi. If anyone has the solution to this I'd love to hear about it!

Known Issues
============

This works really well on some of the sequences, but only sort of well at other times. Working on this. And pull-requests are welcome.
