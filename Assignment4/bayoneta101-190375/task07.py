# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T8f-yHnc1yv5l4hKOlL2lC9DDM9j6lK1

**Task 07: Querying RDF(s)**
"""
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

# TO DO
# Visualize the results

#Rdflib
ns=Namespace("http://somewhere#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
# subject, predicate, object
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s)

#SPARQL
from rdflib.plugins.sparql import prepareQuery


q1 = prepareQuery('''
  SELECT 
    ?x
  WHERE { 
    ?x rdfs:subClassOf ns:Person
  }
  ''',
  initNs = {"ns": ns, "rdfs":rdfs }
)


for r in g.query(q1):
  print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
# Visualize the results
#Rdflib

for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s_, p_, o_ in g.triples((None, RDF.type, s)):
    print(s_, "subclase de:", s, "es de tipo Person")

for s, p, o in g.triples((None, RDF.type, ns.Person)):
  print(s)

# SPARQL
q2 = prepareQuery('''
  SELECT DISTINCT 
  ?s 
  WHERE { 
    ?subject rdfs:subClassOf* ns:Person .
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?subject
  } 
  ''',
  initNs = {"ns": ns,"rdfs":rdfs}
)

for r in g.query(q2):
  print(r)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

# TO DO
# Visualize the results

#rdflib


for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s_, p_, o_ in g.triples((None, RDF.type, s)):
    for s__, p__, o__ in g.triples((s_, None, None)):
      print(s__, p__, o__)

for s,p,o in g.triples((None, RDF.type, ns.Person)):
  for a,b,c in g.triples((s, None, None)):
    print(a,b,c)

#SPARQL:
q3 = prepareQuery('''
  SELECT DISTINCT ?s ?p ?o
  WHERE { 
    ?subject rdfs:subClassOf* ns:Person .
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?subject.
    ?s ?p ?o.
  } 
  ''',
  initNs = { "ns": ns,"rdfs":rdfs}
)
for r in g.query(q3):
  print(r)