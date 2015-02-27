"""Retrieve arXiv abstracts with the OAI-PMH protocol
The parser is messed up: it returns empty lists for the metadata tags;
Do not use it"""


from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

URL = 'http://export.arxiv.org/oai2'

registry = MetadataRegistry()
registry.registerReader('arXiv', oai_dc_reader)
client = Client(URL, registry)

counter = 0
for record in client.listRecords(metadataPrefix='arXiv', set='physics:hep-ex'):
    if counter == 150:
        break
    # print record[0].datestamp()
    # print record[0].identifier()
    # print record[1].getField(name='title')
    print(vars(record[1]))
    counter += 1

# for a_set in client.listSets():
#     # if counter == 50:
#     #     break
#     print a_set
#     counter += 1
