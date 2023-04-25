#! /usr/bin/env python3
__doc__ = """Run a local HTTP web service to view the web site for development
"""

import http.server, argparse, os, sys

serverDirectory = None
cgiDirectories = ['/cgi-bin', '/htbin', '/downloads', '/forms']

class myCGIHTTPRequestHandler(http.server.CGIHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, directory=serverDirectory or '.', **kwargs)
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'port', type=int, nargs='?', default=8888,
        help='Local port for web service')
    parser.add_argument(
        '-H', '--host', default='localhost',
        help='Normally, the local host, but could be a particular network '
        'address on the the local host that will accept network connections.')
    parser.add_argument(
        '-r', '--root', default='public_html',
        help='Directory where root of the HTML documents are. '
        'Can either be relative to this executable or a full path.')
    parser.add_argument(
        '-c', '--CGI', metavar='DIR', nargs='*', default=cgiDirectories,
        help='Directory where CGI scripts are found under the HTML root.')
    args = parser.parse_args()

    # Find the web server root directory
    serverDirectory = None
    myCGIHTTPRequestHandler.cgi_directories = args.CGI
    dirs = set([os.path.dirname(sys.argv[0])])
    try:
        dirs.add(os.path.dirname(__file__))
    except:
        pass
    
    for dir in dirs:
        for trial in (os.path.join(dir, args.root), args.root):
            if os.path.exists(trial) and os.path.isdir(trial):
                serverDirectory = trial
                break

    serverDirectory = serverDirectory or '.'
    os.environ['DOCUMENT_ROOT'] = serverDirectory
    httpd = http.server.HTTPServer(
        (args.host, args.port), myCGIHTTPRequestHandler)
    print('Serving files from {} at http://{}:{} .'.format(
        serverDirectory, args.host, args.port))
    print(' with CGI scripts in {}'.format(
        myCGIHTTPRequestHandler.cgi_directories))
    print('Type Control-C to quit.')
    httpd.serve_forever()
