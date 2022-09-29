# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hLS7IorY1ZXFRPbq9_a7fiPmY-lWHjr-

**Task 07: Querying RDF(s)**
"""

!pip install rdflib 
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
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#") 
q1 = prepareQuery('''
  SELECT DISTINCT ?person WHERE {
      ?person rdfs:subClassOf <http://somewhere#Person>.
  }
  ''',
   initNs = { "rdfs": RDFS}
)

# Visualize the results

for r in g.query(q1):
  print(r.person)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
q2 = prepareQuery('''
  SELECT DISTINCT ?subj ?subj2 WHERE {
      ?subj rdf:type <http://somewhere#Person>.
      ?subclass rdfs:subClassOf <http://somewhere#Person>.
      ?subj2 rdf:type ?subclass.
  }
  ''',
  initNs = { "rdfs": RDFS, "rdf": RDF}
)
# Visualize the results
for r in g.query(q2):
     print(r)
# Visualize the results

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

q3 = prepareQuery('''
  SELECT ?subj ?property ?class WHERE {
      ?subj rdf:type <http://somewhere#Person>.
      ?subj ?prop ?obj.
      ?prop rdf:type ?class.
  }
  ''',
  initNs = {"rdf": RDF}
)
# Visualize the results
for r in g.query(q3):
    print(r)