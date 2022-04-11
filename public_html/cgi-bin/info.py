#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os, urllib
from subprocess import *

try:
    a = check_output
except:
    def check_output(*popenargs, **kwargs):
        kwargs['stdout'] = PIPE
        p = Popen(*popenargs, **kwargs)
        (stdout, stderr) = p.communicate()
        if p.returncode != 0:
            raise CalledProcessError(
                "Error in check_output; stdout = '{0}', stderr = '{1}'".format(
                    stdout, stderr))
        return stdout.decode() if isinstance(stdout, bytes) else stdout

def response_header():
    print "Content-Type: text/html; charset=utf-8"
    print "Status: 200"
    print ""
    
def document_header(config={'title': 'info'}):
    print """<!doctype html>
<html>
<head>
  <title>{title}</title>
</head>
""".format(**config)

def document_footer():
    print "</html>"

def document_content():
    print "<body>"
    print "<p>Parts of URI:</p>"
    print "<ul>"
    request_URI = os.environ.get(
        'REQUEST_URI',
        os.environ.get('SCRIPT_NAME',
                       'REQUEST_URI and SCRIPT_NAME not set'))
    for arg in request_URI.split('/'):
        if arg:
            print "<li>{0}</li>".format(urllib.unquote(arg))
    print "</ul>"
    if '?' in request_URI:
        print "<p>Arguments in query:</p>"
        print "<ul>"
        query = os.environ.get('QUERY_STRING', 'QUERY_STRING not set')
        for parm in query.split('&'):
            if parm:
                key, val = parm.split('=', 1) if '=' in parm else (parm, '')
                print "<li>{0:15s}: {1}</li>".format(
                    urllib.unquote(key), urllib.unquote(val))
        print "</ul>"
    print """The four winds<br>
E S W N<br>
🀀 🀁 🀂 🀃<br>
<br>
The three dragons<br>
G R W<br>
🀅 🀄 🀆<br>
"""
    print "</body>"

logfile = None
def log(msg, newline=True):
    global logfile
    if logfile:
        logfile.write('{0}{1}'.format(msg, '\n' if newline else ''))
    
if __name__ == '__main__':
    executable = os.path.basename(sys.argv[0])
    logfile = open('/tmp/{0}.log'.format(executable), 'a')
    log('\n' + '=' * 78)
    log(check_output(['date']), newline=False)
    log('Called {0}'.format(
        ' '.join(["'{0}'".format(x) if ' ' in x or '"' in x else x
                  for x in sys.argv])))
    log('Environment:')
    for key in sorted(os.environ):
        log('{0:20s} = {1}'.format(key, os.environ[key]))
    log('{0:20s} = {1}'.format('working directory', os.getcwd()))

    response_header()
    request_method = os.environ.get('REQUEST_METHOD', '?')
    if request_method in ('GET', 'PUT'):
        document_header(config={'title': executable})
        document_content()
        document_footer()
    else:
        log('Request method {0} {1}'.format(
            request_method, 'unset' if request_method == '?' else 'unknown'))
        log('Ignoring request')
        
