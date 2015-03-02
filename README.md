# Project Fletcher
### Particle name statistics in arXiv abstracts. Natural Language Processing exercise.

The goal of this project is to collect all hep-ex abstracts on the arXiv and provide some fun visualization about the history of particles over time. As an obvious example, how many papers were about the Higgs boson in the last decade?

I understand that it might not have a commercial value per se (this is my personal project, who cares about its commercial value, anyways), but it might answer a little scientific question that a physicist might have (you know...).

Tools used: a little class which I have wrote to retrieve data from the arXiv API (which uses the OAI-PMH protocol), mongoDB to store all the abstracts on the cloud, D3 to create the visualization.