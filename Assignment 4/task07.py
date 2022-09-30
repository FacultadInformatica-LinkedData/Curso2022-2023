# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1intEnSBIPPLwrx5SFx0awfgXM506M0rv

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
# Visualize the results

#for r in g.query(q1):
#  print(r)
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None,RDFS.subClassOf,ns.Person)):
  print(s)
from rdflib.plugins.sparql import prepareQuery
q1= prepareQuery(
    '''
    SELECT ?s
    WHERE{
      ?s rdfs:subClassOf ns:Person
    }
    ''', initNs={"rdfs": RDFS, "ns":ns}
)
for r in g.query(q1):
  print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
# Visualize the results
q2 = prepareQuery('''
  SELECT 
    ?s
  WHERE { 
    {
      ?s rdf:type ns:Person.
    } UNION{
      ?subClass rdfs:subClassOf ns:Person.
      ?s rdf:type ?subClass   
    }  
  }
  ''',
  initNs = { "rdfs":RDFS, "ns":ns, "rdf":RDF}
)
for r in g.query(q2):
  print(r)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

# TO DO
# Visualize the results


q2 = prepareQuery('''
SELECT ?s ?p ?o
  WHERE {
   {
    ?s rdf:type ns:Person.
    ?s ?p ?o1

  }UNION{ 
     ?s rdf:type ?s1.
     ?s ?p ?o1.
     ?s1 rdfs:subClassOf ns:Person
   }
  }
  ''',
  initNs = { "ns": ns, "rdf": RDF, "rdfs": RDFS}
)


for r in g.query(q2):
  print(r)