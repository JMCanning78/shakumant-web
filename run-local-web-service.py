#! /usr/bin/env python3
__doc__ = """Run a local HTTP web service to view the web site for development
"""

import http.server, argparse, os, sys

serverDirectory = None

class simpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, directory=serverDirectory or '.', **kwargs)
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'port', type=int, nargs='?', default=8888,
        help='Local port for web service')
    args = parser.parse_args()

    # Find the public_html subdirectory
    dirs = set([os.path.dirname(sys.argv[0])])
    try:
       dirs.add(os.path.dirname(__file__))
    except:
       pass
    for dir in dirs:
       if os.path.exists(os.path.isdir(os.path.join(dir, 'public_html'))):
          serverDirectory = os.path.join(dir, 'public_html')
          break

    httpd = http.server.HTTPServer(('', args.port),
                                   simpleHTTPRequestHandler)
    print('Serving files from {} at http://localhost:{} .'.format(
       serverDirectory or '.', args.port))
    print('Type Control-C to quit.')
    httpd.serve_forever()
    
