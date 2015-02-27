"""This is just a testing module without the pyoai package:
it is incomplete and do not use it."""

import urllib2
import urllib
from datetime import datetime
from xml.dom.minidom import parse, parseString
import requests
import time
import sys


# function for return dom response after parsting oai-pmh URL
def oaipmh_response(URL):

    print URL
    # file = urllib2.urlopen(URL)
    file = requests.get(URL)
    # data = file.read()
    data = file.text
    print data
    file.close()

    dom = parseString(data)
    return dom


# function for getting value of resumptionToken after parsting oai-pmh URL
def oaipmh_resumptionToken(URL):
    file = requests.get(URL)
    data = file.text
    file.close()

    dom = parseString(data)
    print dom
    print "START: "+str(datetime.now())
    return dom.getElementsByTagName('resumptionToken')[0].firstChild.nodeValue


# function for writing to output files
def write_xml_file(inputData, outputFile):
    oaipmhResponse = open(outputFile, mode="w")
    oaipmhResponse.write(inputData)
    oaipmhResponse.close()
    print "END: "+str(datetime.now())


# main code
baseURL = 'http://export.arxiv.org/oai2'
getRecordsURL = str(baseURL+'?verb=ListRecords&metadataPrefix=arXiv')

# initial parse phase
resumptionToken = oaipmh_resumptionToken(getRecordsURL)  # get initial resumptionToken
print "Resumption Token: "+resumptionToken
outputFile = 'page-0.xml'  # define initial file to use for writing response

wtf = oaipmh_response(getRecordsURL).toxml()

sys.exit(1)

write_xml_file(oaipmh_response(getRecordsURL).toxml(), outputFile)
time.sleep(20)

# loop parse phase
pageCounter = 1
while resumptionToken != "":
    print "URL ECONDED TOKEN: "+resumptionToken
    resumptionToken = urllib.urlencode({'resumptionToken': resumptionToken})  # create resumptionToken URL parameter
    print "Resumption Token: "+resumptionToken
    getRecordsURLLoop = str(baseURL+'?verb=ListRecords&'+resumptionToken)
    oaipmhXML = oaipmh_response(getRecordsURLLoop).toxml()
    outputFile = 'page-'+str(pageCounter)  # create file name to use for writing response
    write_xml_file(oaipmhXML, outputFile)  # write response to output file

    resumptionToken = oaipmh_resumptionToken(getRecordsURLLoop)
    pageCounter += 1  # increament page counter
    time.sleep(20)
