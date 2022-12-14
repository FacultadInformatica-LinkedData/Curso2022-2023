# -*- coding: utf-8 -*-
"""Task09.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aA_7cDJnS46kKnLS5uuCGN5_s3QANqk-

**Task 09: Data linking**
"""

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4/"

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import OWL

g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"resources/data03.rdf", format="xml")
g2.parse(github_storage+"resources/data04.rdf", format="xml")

"""
    Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, 
    inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el 
    mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales 
    para un mismo individuo en los dos grafos.
"""

# Propiedades supuestas:
# apodo -> http://www.w3.org/2001/vcard-rdf/3.0#Given
# nombre de familia -> http://www.w3.org/2001/vcard-rdf/3.0#Family

VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

q1 = prepareQuery("""
    SELECT ?subject ?apodo ?familia 
    WHERE 
    {
        ?subject vcard:Given ?apodo ;
            vcard:Family ?familia . 
    }
    """, 
        initNs={"vcard": VCARD}
    )

for entry in g1.query(q1):
    
    apodo_match = g2.value(None, VCARD.Given, entry.apodo) 
    familia_match = g2.value(None, VCARD.Family, entry.familia) 

    if apodo_match == familia_match:
        g3.add((entry.subject, OWL.sameAs, apodo_match))


for t in g3:
    print(t)