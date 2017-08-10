"""
Fetches the reference docs for a specified revision

Usage:
    fetch_references -h | --help
    fetch_references <host> <title>
                     [--debug]

Options:
    -h --help   Prints this documentation
    <host>      The host of a MediaWiki instance to query, e.g.
                en.wikipedia.org
    <title>     The article title to get text for
    --debug     Prints debug logging
"""
import json
import logging
import sys

import docopt
import mwapi

from ..references import extract


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    logging.basicConfig(
        level=logging.WARNING if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )
    run(args['<host>'], args['<title>'])


def run(host, title):
    session = mwapi.Session("https://" + host)
    doc = session.get(action='query', prop='revisions', titles=title,
                      rvprop='content', formatversion=2)
    content = doc['query']['pages'][0]['revisions'][0]['content']
    for reference_doc in extract(content):
        json.dump(reference_doc, sys.stdout)
        sys.stdout.write("\n")
