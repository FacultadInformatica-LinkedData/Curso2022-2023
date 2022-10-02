# **Task 07: Querying RDF(s)**
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"
import pandas as pd
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

g = Graph()
NS = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
g.namespace_manager.bind('ns', NS, override=False)
g.namespace_manager.bind('vcard', VCARD, override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**
q1 = prepareQuery('''
  SELECT ?any 
  WHERE { 
    ?any rdfs:subClassOf ns:Person .
  }''',
  initNs = {"ns": NS, "rdfs":RDFS}
)

print("\n 7.1 Result Sparql:")
for r in g.query(q1):
  print(f"{r.any} is subClass of {NS.Person}")

print("\n 7.1 Result RDFLib:")
for subC,_,_ in g.triples((None, RDFS.subClassOf, NS.Person)):
  print(f"{subC} is subClass of {NS.Person}")

# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
q2 = prepareQuery('''
  SELECT ?person ?clss 
  WHERE { 
    {
      BIND(ns:Person as ?clss)
      ?person a ?clss.
    }
    UNION
    {
      ?clss rdfs:subClassOf ns:Person .
      ?person a ?clss .
    }
  }''',
  initNs = {"ns": NS, "rdf":RDF, "rdfs":RDFS}
)

print("\n 7.2 Result SparQL:")
for r in g.query(q2):
  print(f"{r.person} is a {r.clss}")

print("\n 7.2 Result RDFLib:")
for s,_,_ in g.triples((None, RDF.type, NS.Person)):
  print(f"{s} is a {NS.Person}")

for subC,_,_ in g.triples((None, RDFS.subClassOf, NS.Person)):
  for s,_,_ in g.triples((None, RDF.type, subC)):
    print(f"{s} is a {subC}")

# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

# Using SPARQL:
q3 = prepareQuery('''
  SELECT ?person ?prop ?value
  WHERE {
    {
      ?person a ns:Person ;
        ?prop ?value .
    }
    UNION
    {
      ?clss rdfs:subClassOf ns:Person .
      ?person a ?clss ;
        ?prop ?value .
    }
  }''',
  initNs = {"ns": NS, "rdf":RDF, "rdfs":RDFS}
)

q3a_result = []
for person, prop, value in g.query(q3):
  q3a_result.append((person, f"...{prop[-45:]}", value))

df = pd.DataFrame(q3a_result, columns =['Person', 'Property', 'Value'])

print("\n 7.3a result Sparql🚀")
print(df)

# Using RDFLib:
q3b_result = []
for person,_,_ in g.triples((None, RDF.type, NS.Person)):
  for _,prop,value in g.triples((person, None, None)):
    q3b_result.append((person, f"...{prop[-45:]}", value))

# Umm maybe it could be done differently I don't like this level of complexity..
for subclss,_,_ in g.triples((None, RDFS.subClassOf, NS.Person)):
  for person,_,_ in g.triples((None, RDF.type, subclss)):
    for _,prop,value in g.triples((person, None, None)):
      q3b_result.append((person, f"...{prop[-45:]}", value))

df = pd.DataFrame(q3b_result, columns =['Person', 'Property', 'Value'])

print("\n 7.3b result RDFLib🚀")
print(df)


