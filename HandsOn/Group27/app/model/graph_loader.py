# Copyright (c) 2022 FSM Solutions.
from rdflib import Graph, Namespace, RDFS, OWL
import pathlib

graph = Graph()
graph.parse(pathlib.Path(__file__).parents[2].resolve().as_posix() + "/rdf/consumo-energia-edificios-updated-linked.ttl", format="ttl")

# Used namespaces
SSN = Namespace("http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#")
TIME = Namespace("http://www.w3.org/TR/owl-time#")
WD = Namespace("http://www.wikidata.org/wiki/")
EC = Namespace("http://www.semanticweb_g27.org/ontology/EnergyCons#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
SCHEMA = Namespace("http://schema.org/")
