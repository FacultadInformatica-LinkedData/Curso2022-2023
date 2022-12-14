# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x0Y5N7m9k6VZSE7I25L_VZ09nL-VnZxY

**Task 08: Completing missing data**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""

vcard=Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
print("\n listamos los elementos de la clase Person del primer grafo en RDFLib")
for s, p, o in g1.triples((None,None,RDFS.Class)):
  for s1, p1, o1 in g1.triples((None,RDF.type,s)):
    print(s1)
   
#rellenamos los campos que faltan en el g1
    if not (s1,vcard.Given,None) in g1:
     tripletas_Given = g2.triples((s1, vcard.Given, None))
     for s2, p2, o2 in tripletas_Given:
      g1.add((s1, vcard.Given,o2))
    
    if not (s1,vcard.Family,None) in g1:
      tripletas_Family = g2.triples((s1, vcard.Family, None))
      for s2, p2, o2 in tripletas_Family:
       g1.add((s1, vcard.Family,o2))
    
    if not (s1,vcard.EMAIL,None) in g1:
      tripletas_EMAIL = g2.triples((s1, vcard.EMAIL, None))
      for s2, p2, o2 in tripletas_EMAIL:
       g1.add((s1, vcard.EMAIL,o2))



print("\n listamos los elementos de la clase Person del primer grafo con los datos completos en RDFLib")
for s, p, o in g1:
  print(s,p,o)