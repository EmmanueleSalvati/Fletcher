"""
Module taken from
python_arXiv_paging_example.py

Recommend that you wait 3 seconds between api calls.

Please see the documentation at
http://export.arxiv.org/api_help/docs/user-manual.html
for more information, or email the arXiv api
mailing list at arxiv-api@googlegroups.com.

feedparser can be downloaded from http://feedparser.org/ .
"""

import urllib
import time
import feedparser
from dateutil import parser


def change_date_format(published):
    """Utility function to change the date format into a datetime object"""

    return parser.parse(published).date()


if __name__ == '__main__':
    PARTICLES = ['electron', 'muon', 'tau']

    # Base api query url
    base_url = 'http://export.arxiv.org/api/query?'

    # Search parameters
    search_query = 'cat:hep-ph+AND+abs:electron'
    start = 0                       # start at the first result
    total_results = 5              # want 20 total results
    results_per_iteration = 5       # 5 results at a time
    wait_time = 3                   # number of seconds to wait beetween calls

    print 'Searching arXiv for %s' % search_query

    for i in range(start, total_results, results_per_iteration):
        print "Results %i - %i" % (i, i+results_per_iteration)

        query = 'search_query=%s&start=%i&max_results=%i' % (search_query, i,
                                                             results_per_iteration)

        # perform a GET request using the base_url and query
        response = urllib.urlopen(base_url+query).read()

        # parse the response using feedparser
        feed = feedparser.parse(response)

        # Run through each entry, and print out information
        for entry in feed.entries:
            # print 'arxiv-id: %s' % entry.id.split('/abs/')[-1]
            print 'Title:  %s' % entry.title
            # # feedparser v4.1 only grabs the first author
            # print 'First Author:  %s' % entry.author
            print 'Publication date %s' % change_date_format(entry.published)

        # Remember to play nice and sleep a bit before you call
        # the api again!
        print 'Sleeping for %i seconds' % wait_time
        time.sleep(wait_time)
