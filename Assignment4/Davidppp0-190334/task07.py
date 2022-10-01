# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
#!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

# %% [markdown]
# Leemos el fichero RDF de la forma que lo hemos venido haciendo

# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# %% [markdown]
# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

# %%
# TO DO
ns = Namespace("http://somewhere#")

# RDFLib
print("List RDFLib:")
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    print(s)

# SPARQL
print("------\nList SPARQL:")
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?s
  WHERE { 
    ?s rdfs:subClassOf ns:Person. 
  }
  ''',
  initNs = { "rdfs": RDFS, "ns" : ns}
)

# Visualize the results
for r in g.query(q1):
  print(r)

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %%
# TO DO
ns = Namespace("http://somewhere#")

# RDFLib
print("RDFLib:")
for s,p,o in g.triples((None, RDF.type, ns.Person)):
    print(s)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for ss,pp,oo in g.triples((None, RDF.type, s)):
        print(ss)

# SPARQL
print("------\nList SPARQL:")
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?s
  WHERE { 
    {
      ?s rdf:type ns:Person.
    } 
    UNION {
      ?s rdf:type ?x.
      ?x rdfs:subClassOf* ns:Person.
    }
  }
  ''',
  initNs = { "rdf": RDF, "rdfs": RDFS, "ns" : ns}
)
# Visualize the results
for r in g.query(q1):
  print(r)

# %% [markdown]
# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
# 

# %%
# TO DO
ns = Namespace("http://somewhere#")

# RDFLib
print("RDFLib:")
for s,p,o in g.triples((None, RDF.type, ns.Person)):
    for ss,pp,oo in g.triples((s, None, None)):
        print(ss,pp,oo)
        
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for ss,pp,oo in g.triples((None, RDF.type, s)):
            for sss,ppp,ooo in g.triples((ss, None, None)):
                print(sss,ppp,ooo)

# SPARQL
print("-----\nSPARQL:")
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?s ?p
  WHERE { 
    {
      ?s rdf:type ns:Person.
      ?s ?p ?x.
    } 
    UNION {
      ?s rdf:type ?y.
      ?y rdfs:subClassOf* ns:Person.
      ?s ?p ?x.
    }
  }
  ''',
  initNs = { "rdf": RDF, "rdfs": RDFS, "ns" : ns}
)

# Visualize the results
for r in g.query(q1):
  print(r)


