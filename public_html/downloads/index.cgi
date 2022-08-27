#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, urllib, glob, time
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

def document_content(config, sections):
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
                       'Download {0}</li>').format(os.path.basename(f))
                      for f in section['downloads'])))
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
    log(check_output(['date']), newline=False)
    log('Called {0}'.format(
        ' '.join("{0!r}".format(x) if ' ' in x else x
                 for x in [executable] + sys.argv[1:])))
    log('Python version: {0}'.format(sys.version_info))
    if '-e' not in sys.argv[1:]:
        log('Environment:')
        for key in sorted(os.environ):
            log('{0:20s} = {1}'.format(key, os.environ[key]))
    dirs = [arg for arg in sys.argv[1:] +
            [os.path.join(
                os.getcwd(),
                os.path.dirname(
                    os.environ.get('SCRIPT_NAME',
                                   '/downloads/index.cgi').strip('/')))]
            if os.path.isdir(arg)]

    log('Current working directory:', os.getcwd())
    log('Script name:',
        os.environ.get('SCRIPT_NAME', '/downloads/index.cgi').strip('/'))
    log('Combined directory candidate:',
        os.path.join(
            os.getcwd(),
            os.path.dirname(
                os.environ.get('SCRIPT_NAME',
                               '/downloads/index.cgi').strip('/'))))
    if len(dirs) == 0:
        dirs = ['.']
    
    request_method = os.environ.get('REQUEST_METHOD', '?')
    if request_method in ('GET', 'PUT'):
        response_header()
        config={'title': 'Downloads Archive'}
        document_header(config=config)
        last = 'other'
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
        document_content(config, sections)
        document_footer()
    else:
        log('Request method {0} {1}'.format(
            request_method, 'unset' if request_method == '?' else 'unknown'))
        log('Ignoring request')
