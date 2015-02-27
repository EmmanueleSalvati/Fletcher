"""Module to make requests to the arXiv OAI-PMH and return them"""

from bs4 import BeautifulSoup
import re
from datetime import datetime
import requests
import time
import sys

"""Arguments for querying from OAI-PMH

*from* an optional argument with a UTCdatetime value, which specifies a
lower bound for datestamp-based selective harvesting.

*until* an optional argument with a UTCdatetime value, which specifies a
upper bound for datestamp-based selective harvesting.

*set* an optional argument with a setSpec value , which specifies set
criteria for selective harvesting.

*resumptionToken* an exclusive argument with a value that is the flow
control token returned by a previous ListRecords request that issued an
incomplete list.

*metadataPrefix* a required argument (unless the exclusive argument
resumptionToken is used) that specifies the metadataPrefix of the format
that should be included in the metadata part of the returned records.
Records should be included only for items from which the metadata format
"""


class OAIFetcher():
    """Fetch and return a batch of documents
        params:
            baseURL: 'http://export.arxiv.org/oai2'
            metadataPrefix='arXiv'
    """

    def __init__(self, baseURL='http://export.arxiv.org/oai2',
                 metadataPrefix='arXiv'):
        self._baseURL = baseURL

        self._params = {
            'verb': 'ListRecords',
            'metadataPrefix': metadataPrefix
        }

    def set_params(self, token=None):
        self._params = {
            'verb': 'ListRecords',
            'resumptionToken': token
        }

    def fetch(self, setSpec='physics:hep-ex', date_from=None, date_until=None):
        """Fetch data from the OAI.
        """

        self._params['set'] = setSpec

        if date_from:
            self._params['from'] = date_from

        if date_until:
            self._params['until'] = date_until

        xml = self.query(**self._params)
        soup = BeautifulSoup(xml)
        docs = [soup]
        token = ''
        if soup.find('resumptiontoken'):
            token = soup.find('resumptiontoken').text
        del soup

        while token:
            self.set_params(token=token)
            xml = self.query(**self._params)
            soup = BeautifulSoup(xml)
            docs.append(soup)
            if soup.find('resumptiontoken'):
                token = soup.find('resumptiontoken').text

        return docs

    def query(self, **kwargs):
        '''Get articles from OAI in XML format.
        '''

        print 'Querying OAI with params %s...' % (kwargs)

        # Build URL for request
        _url_params = '&'.join(['%s=%s' % (key, val) for key, val
                               in kwargs.iteritems()])
        url = '%s?%s' % (self._baseURL, _url_params)
        print 'Querying OAI with url %s' % (url)

        # Get and return XML from OAI
        time.sleep(20)
        req = requests.get(url)

        return req.text
