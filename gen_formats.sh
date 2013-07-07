#!/usr/bin/env bash
rst2html.py lesswrong.rst lesswrong.html # create html
kindlegen lesswrong.html -o lesswrong.mobi # create mobi
pandoc -o lesswrong.epub lesswrong.rst # create epub


