"""JonnyGuru PSU Crawler

Usage:
  jonnyguru_crawler.py crawl 
  jonnyguru_crawler.py (-h | --help)
  jonnyguru_crawler.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt


def crawl():
    pass


if __name__ == '__main__':
    arguments = docopt(__doc__, version='JonnyGuru PSU Crawler v0.0.1')

    if arguments['crawl']:
        crawl()
