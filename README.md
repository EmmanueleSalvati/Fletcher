# Project Fletcher
### Particle name statistics in arXiv abstracts. Natural Language Processing exercise.

The goal of this project is to collect all hep-ex abstracts on the arXiv and provide a visualization about the history of particles over time. As an obvious example, how many papers were about the Higgs boson in the last decade?

Tools used: a little class which I have written to retrieve data from the arXiv API (which uses the OAI-PMH protocol), mongoDB to store all the abstracts on the cloud, D3 to create the visualization.