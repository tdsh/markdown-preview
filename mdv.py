#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
from datetime import datetime
import markdown2
import webbrowser
import re


def check_strikethrough(line, index):
    if '~~' in line:
        if index % 2:
            line = line.replace('~~', '<del>', 1)
        else:
            line = line.replace('~~', '</del>', 1)
        index += 1
        (line, index) = check_strikethrough(line, index)
    return (line, index)


# translate to GitHub Flavored Markdown
# Only covers Strikethrough, Fenced code blocks.
#
# https://help.github.com/articles/github-flavored-markdown
def convert_gfm(content):
    # Fenced code blocks
    code_block = re.findall('^(```.*)\n.*\n(```)$', content, re.MULTILINE)
    num = len(code_block) * 2
    res = ''
    index = 1
    for line in content.split('\n'):
        if '```' in line:
            if index > num:
                res += line
            elif index % 2:
                res += line.replace('```', '<pre><code>')
            else:
                res += line.replace('```', '</code></pre>')
            index += 1
        else:
            res += line
        res += '\n'
    # Strikethrough
    strikethrough = re.findall('(~~).*(~~)', res, re.MULTILINE)
    num = len(strikethrough) * 2
    print num
    final = ''
    index = 1
    res = res.split('\n')
    for line in res:
        if '~~' in line:
            if index > num:
                final += line
            else:
                (line, index) = check_strikethrough(line, index)
                final += line
        else:
            final += line
        final += '\n'
    return final


def main(markdown_file):
    infile = file(markdown_file, 'r')
    outfile = '/tmp/md-' + str(int(time.mktime(datetime.now().timetuple()))) +\
              '.html'
    md = markdown2.Markdown()
    out = file(outfile, 'w')
    content = convert_gfm(infile.read())
    content = '<html><head><meta charset="UTF-8" /></head><body>' +\
              md.convert(content) + '</body></html>'
    content = content.encode('utf-8')
    out.write(content)
    infile.close()
    out.close()
    w3m = webbrowser.get('w3m')
    w3m.open('file:///' + outfile)
    os.remove(outfile)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'tyes'
        print 'Usage: %s <Markdown file>\n' % sys.argv[0]
        sys.exit(1)
    main(sys.argv[1])