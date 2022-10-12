# Copyright (c) 2022 FSM Solutions.
from rdflib import Graph, Namespace

graph = Graph()
graph.parse("./HandsOn/Group27/rdf/consumo-energia-edificios-updated.ttl", format="ttl")

# Used namespaces
SSN = Namespace("http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#")
TIME = Namespace("http://www.w3.org/TR/owl-time#")
WD = Namespace("http://www.wikidata.org/wiki/")
EC = Namespace("http://www.semanticweb_g27.org/ontology/EnergyCons#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
SCHEMA = Namespace("http://schema.org/")

graph.namespace_manager.bind('ssn', SSN, override=False)
graph.namespace_manager.bind('time', TIME, override=False)
graph.namespace_manager.bind('wd', WD, override=False)
graph.namespace_manager.bind('schema', SCHEMA, override=False)
graph.namespace_manager.bind('ec', EC, override=False)

# graph loaded.