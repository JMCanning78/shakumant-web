#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, glob, time
from urllib.parse import *
from subprocess import *

# Definitions for different download sections:
sections = [
    {'title': 'Visualiztions bundle for macOS', 'id': 'macOS',
     'description': '',
     'pattern': 'DatastructureVisualizations*_[0-9][0-9].dmg'},
    {'title': 'Visualiztions bundle for Windows', 'id': 'windows',
     'description': '',
     'pattern': 'DatastructureVisualizations*_[0-9][0-9].zip'},
    {'title': 'Other downloads', 'id': 'other',
     'description': '',
     'pattern': '*.zip'},
]

output = print

def response_header():
    output("Content-Type: text/html; charset=utf-8")
    output("Status: 200")
    output("")
    
def document_header(config={'title': 'Visualization Downloads Archive'}):
    output("""<!doctype html>
<html>
<head>
  <title>{title}</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" >
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="/main-functions.js"></script>
  <link rel="stylesheet" type="text/css" href="/main-styles.css">
  <link rel="icon" type="img" href="/Shakumant-logo-favicon.png">
</head>
""".format(**config))

def document_headrow():
    output('''
  <div class="smallheader">
    <a href="/" class="homelink">
      <img class="homelinklogo"
	   src="/Shakumant-logo-and-text.svg" alt="Shakumant Software logo" />
    </a>
    <!-- <p class="centered">
      <i>Data Structures &amp; Algorithms in Python</i>
    </p> -->
  </div>
''')
    
def document_footrow():
    output('<div class="footer">')
    output('<p class="footer">Copyright © {0}</p>'.format(time.gmtime().tm_year))
    output('</div>')
    
def document_footer():
    output("</html>")

def document_content(config, sections, other_info=()):
    output("<body>")
    document_headrow()
    output("<H1>{title}</H1>".format(**config))
    for section in sections:
        if not section['downloads']:
            continue
        output(('<div class="columnmenu" id="{id}_downloads">\n'
                '<H2>{title}</H2>').format(**section))
        if section['description']:
            output('<p class="centered">{description}</p>'.format(**section))
        output('<ul class="menulist">\n{0}\n</ul></div>'.format(
            '\n'.join(('<li class="button" onclick="download_file({0!r})">\n'
                       'Download {0}</li>Updated: {1}').format(
                           os.path.basename(f),
                           time.ctime(os.stat(f).st_mtime))
                      for f in section['downloads'])))
    for i, info in enumerate(other_info):
        output('<div class="columnmenu" id="otherinfo_{}">\n<p>{}</p>\n</div>'
               .format(i + 1, info))
    document_footrow()
    output("</body>")

logfile = None
def log(*msgs, newline=True):
    global logfile
    if logfile:
        logfile.write('{0}{1}'.format(' '.join(str(m) for m in msgs),
                                      '\n' if newline else ''))
    
if __name__ == '__main__':
    executable = os.path.basename(sys.argv[0])
    logfile = open('/tmp/{0}.log'.format(executable), 'a')
    log('\n' + '=' * 78)
    server_datetime = check_output(['date']).decode().strip()
    log(server_datetime, '', newline=False)
    log('Called {0}'.format(
        ' '.join("{0!r}".format(x) if ' ' in x else x
                 for x in [executable] + sys.argv[1:])))
    python_info = 'Python version: {0}'.format(sys.version_info)
    log(python_info)
    if '-e' not in sys.argv[1:]:
        log('Environment:')
        for key in sorted(os.environ):
            log('{0:20s} = {1}'.format(key, os.environ[key]))
    script_name = os.environ.get(
        'SCRIPT_NAME', '/downloads/index.cgi').strip('/')
    cwd = os.getcwd()
    path_translated = os.environ.get('PATH_TRANSLATED', cwd)
    dirs = [arg
            for arg in sys.argv[1:] + [
                    os.path.dirname(os.path.join(cwd, script_name)),
                    os.path.dirname(os.path.join(path_translated, script_name)),
                    cwd]
            if os.path.isdir(arg)]

    log('Current working directory:', cwd)
    log('Script name:', script_name)
    log('Combined directory candidates:', '\n'.join(dirs))
    if len(dirs) == 0:
        dirs = ['.']

    request_URI = urlparse(os.environ.get('REQUEST_URI', ''))
    request_query = parse_qs(os.environ.get('QUERY_STRING', request_URI.query))
    
    request_method = os.environ.get('REQUEST_METHOD', '?')
    if request_method in ('GET', 'PUT'):
        response_header()
        config={'title': 'Downloads Archive'}
        document_header(config=config)
        done = set()
        for section in sections:
            downloads=[f for dir in dirs
                       for f in glob.glob(os.path.join(dir, section['pattern']))
                       if not os.path.islink(f) and f not in done]
            downloads.sort(key=os.path.basename, reverse=True)
            section['downloads'] = downloads
            done |= set(downloads)
        log('Found {0} among {1}'
            .format(', '.join('{0} {1}'.format(str(len(s['downloads'])),
                                               s['id'])
                              for s in sections),
                    dirs))
        document_content(
            config, sections,
            (python_info, server_datetime) if 'debug' in request_query else ())
        document_footer()
    else:
        log('Request method {0} {1}'.format(
            request_method, 'unset' if request_method == '?' else 'unknown'))
        log('Ignoring request')
