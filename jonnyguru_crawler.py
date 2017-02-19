"""JonnyGuru PSU Crawler

Usage:
  jonnyguru_crawler.py crawl 
  jonnyguru_crawler.py sort <file_path>
  jonnyguru_crawler.py (-h | --help)
  jonnyguru_crawler.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import json

from docopt import docopt


def crawl():
    pass


def sort(file_path):
    all_results = []
    with open(file_path, 'r') as results:
        for line in results.readlines():
            all_results.append(json.loads(line))

    all_results.sort(key=sort_how, reverse=True)
    print(all_results[:10])


def sort_how(elem):
    try:
        return float(elem['scores']['total_score'] or '0.0')
    except ValueError:
        return 0.0


if __name__ == '__main__':
    arguments = docopt(__doc__, version='JonnyGuru PSU Crawler v0.0.1')

    if arguments['crawl']:
        crawl()

    if arguments['sort']:
        file_path = arguments['<file_path>']
        sort(file_path)
