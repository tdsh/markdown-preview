#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from future.builtins import str

import os
import argparse
import time
from datetime import datetime
import markdown2
import webbrowser
import re
import yaml

CONFIG_FILE = '/etc/mdv.yaml'


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
    print(num)
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


def main():
    parser = argparse.ArgumentParser(description=u'preview markdown file via \
                                     terminal.')
    parser.add_argument('file', type=str,
                        help='markdown file')
    parser.add_argument('-d', '--default', help='use default directory',
                        action='store_true')
    args = parser.parse_args()

    # load mdv config
    try:
        config_file = open(CONFIG_FILE, 'r')
    except Exception as msg:
        print('Failed to open mdv config file {0}: {1}'.
              format(CONFIG_FILE, msg))

    else:
        config_data = yaml.safe_load(config_file)
        config_file.close()

    default_directory = ''
    if args.default:
        try:
            default_directory = config_data['config']['default_directory']
        except KeyError:
            # No entry fo default directory.
            pass
        else:
            if default_directory is None:
                default_directory = ''
            elif default_directory[-1] != '/':
                default_directory += '/'

    try:
        infile = file(default_directory + args.file, 'r')
    except Exception as msg:
        print('Failed to open file: {0}'.format(msg))
        return
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
    main()
