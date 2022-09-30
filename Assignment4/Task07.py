#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# Leemos el fichero RDF de la forma que lo hemos venido haciendo

# In[2]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

# In[7]:


# TO DO
# Visualize the results
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
# Visualize the results
for r in g.triples((None,RDFS.subClassOf,ns.Person)):
  print(r)
############################ SPARQL ###################################3
q1 = prepareQuery('''
  SELECT ?Subject ?Class WHERE { 
    ?Subject rdfs:subClassOf ns:Person.
  } 
  ''', initNs = { "ns": ns})
# Visualize the results
for r in g.query(q1):
  print(r.Subject)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[8]:


# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
# Visualize the results
for s in g.triples((None,RDF.type,ns.Person)):
  print(s)

################################# SPARQL ################################################################
q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdf:type ns:Person.
  } 
  ''', initNs = { "ns": ns})
# Visualize the results
for r in g.query(q1):
  print(r.Subject)


# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
# 

# In[9]:


# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
for s,p,o in g.triples((None,RDF.type,ns.Person)):
# Visualize the results  
  for r in g.triples((s,vcard,None)):
    print(r)

################################## SPARQL ###############################################################
q1 = prepareQuery('''
  SELECT ?Subject ?property WHERE { 
    ?Subject ?property vcard:Person.
  } 
  ''', initNs = { "vcard": vcard,"ns":ns})
# Visualize the results
for r in g.query(q1):
  print(r.Subject)

