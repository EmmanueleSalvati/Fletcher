"""Functions to connect to the MongoDB on DigitalOcean cloud"""

from pymongo import MongoClient
from textblob import TextBlob
from collections import Counter
import socket


def str_to_datetime(datestr):
    """Takes a string like 7/31/92 and returns a datetime object"""

    from dateutil.parser import parse

    date = parse(datestr)
    return date


def particles_in_abstract(words):
    """Returns a list of particles in this abstract"""

    particles_in_abs = [word for word in words if word in KEYWORDS]
    return particles_in_abs


def get_cursor(coll='hepex', from_date=None, to_date=None):
    """Returns the cursor in the given date range"""

    if coll == 'hepph':
        collection = client.arXivpapers.hepph
    else:
        collection = client.arXivpapers.hepex

    cursor = collection.find()
    return cursor


def loop_events(cursor=None):
    """Dumps all the particle names into a dictionary, whose keys are dates"""

    assert cursor, "there is no cursor!"
    abs_dict = {}

    counter = Counter()
    for record in cursor:
        date = str_to_datetime(record['date'])
        ABSTRACT = record['abstract']
        abstract = TextBlob(ABSTRACT)
        blob = list(abstract.words.singularize())
        if 'higg' in blob:
            blob.remove('higg')
            blob.append('higgs')
        particles = particles_in_abstract(blob)
        abs_dict[date] = particles
        for word in particles:
            counter[word] += 1

    return (abs_dict, counter)


if __name__ == '__main__':
    # URI instructions are here:
    # http://docs.mongodb.org/manual/reference/connection-string/
    # import urllib
    # password = urllib.quote_plus(mypassword)

    if socket.gethostname() == 'mcnulty-emmanuele':
        client = MongoClient()
    else:
        URI = 'mongodb://104.236.210.21'
        client = MongoClient(host=URI)

    KEYWORDS = ['electron', 'photon', 'muon', 'higgs', 'tau', 'proton',
                'neutron', 'quark', 'top', 'strange', 'bottom', 'quark',
                'lepton', 'meson', 'jet', 'BaBar', 'ATLAS', 'CMS']

    hepex = client.arXivpapers.hepex
    hepph = client.arXivpapers.hepph

    # Create a dictionary with [datetime]: [particles]
    # and a simple Counter to quickly see how many particles are in total
    cursor = get_cursor()
    (abs_dict, counter) = loop_events(cursor)
