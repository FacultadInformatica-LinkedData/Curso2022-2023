# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18P0xTS31q1P7nR4efg0Yy3QrClOxqMAe

**Task 08: Completing missing data**
"""

#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4/"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"resources/data01.rdf", format="xml")
g2.parse(github_storage+"resources/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""

from rdflib import XSD
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

print("Graph 1 triples:")

for subj, pred, obj in g1:
  print(subj,pred,obj)

print("\n")
q1 = prepareQuery('''
        SELECT DISTINCT ?Person ?Given ?Family ?Email WHERE{
          ?Person rdf:type <http://data.org#Person>
          OPTIONAL{?Person vcard:Given ?Given}.
          OPTIONAL{?Person vcard:Family ?Family}.
          OPTIONAL{?Person vcard:EMAIL ?Email}
        }
    ''',
    initNs={"vcard":VCARD, "rdf":RDF}
    )

q2 = prepareQuery('''
        SELECT DISTINCT ?Person ?Given ?Family ?Email WHERE{
          OPTIONAL{?Person vcard:Given ?Given}.
          OPTIONAL{?Person vcard:Family ?Family}.
          OPTIONAL{?Person vcard:EMAIL ?Email}
        }
    ''',
    initNs={"vcard":VCARD, "rdf":RDF}
    )

for r in g1.query(q1):
  for rTemp in g2.query(q2, initBindings={"?Person":r.Person}):
    if(r.Given == None and rTemp.Given != None): g1.add((r.Person, VCARD.Given, Literal(rTemp.Given, datatype=XSD.string)))
    if(r.Family == None and rTemp.Family != None): g1.add((r.Person, VCARD.Family, Literal(rTemp.Family, datatype=XSD.string)))
    if(r.Email == None and rTemp.Email != None): g1.add((r.Person, VCARD.EMAIL, Literal(rTemp.Email, datatype=XSD.string)))

print("Graph 1 triples after completing data:")
for subj, pred, obj in g1:
  print(subj,pred,obj)