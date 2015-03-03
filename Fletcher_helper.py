"""Functions to connect to the MongoDB on DigitalOcean cloud"""

# import urllib
from pymongo import MongoClient
from textblob import TextBlob
from collections import Counter
import nltk


def count_particles(abstract):
    """Adds counts to the global Counter() of particles"""

    words = abstract.words.singularize()
    for particle in particles:
        if particle in words:
            counter[particle] += 1


def get_cursor(collection=hepex, from_date=None, to_date=None):
    """Returns the cursor in the given date range"""

    collection.find()

if __name__ == '__main__':
    # URI instructions are here:
    # http://docs.mongodb.org/manual/reference/connection-string/

    # password = urllib.quote_plus('p0rcaccioInf@me')
    # URI = 'mongodb://JerkFace:' + password + '@104.236.210.21'
    # client = MongoClient(URI)

    raw_particles = ['electron', 'photon', 'muon', 'higgs', 'tau']
    stemmer = nltk.stem.porter.PorterStemmer()
    particles = []
    for particle in raw_particles:
        particles.append(stemmer.stem(particle))

    client = MongoClient()
    hepex = client.arXivpapers.hepex

    counter = Counter()
    cursor = hepex.find()
    for record in cursor:
        ABSTRACT = record['abstract']
        abstract = TextBlob(ABSTRACT)
        count_particles(abstract)
