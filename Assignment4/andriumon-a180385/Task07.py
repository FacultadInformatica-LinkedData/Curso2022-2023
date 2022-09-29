#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[22]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# Leemos el fichero RDF de la forma que lo hemos venido haciendo

# In[23]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

# In[24]:


# TO DO
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?subject WHERE {
      ?subject rdfs:subClassOf <http://somewhere#Person>.
  }
  ''',
  initNs = { "rdfs": RDFS}
)
# Visualize the results
for r in g.query(q1):
    print(r)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[32]:


# TO DO
q2 = prepareQuery('''
  SELECT ?subject ?subject2 WHERE {
      ?subject rdf:type <http://somewhere#Person>.
      ?subclass rdfs:subClassOf <http://somewhere#Person>.
      ?subject2 rdf:type ?subclass.
  }
  ''',
  initNs = { "rdfs": RDFS, "rdf": RDF}
)
# Visualize the results
for r in g.query(q2):
    print(r)


# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
# 

# In[34]:


# TO DO
q3 = prepareQuery('''
  SELECT ?subject ?property ?class WHERE {
      ?subject rdf:type <http://somewhere#Person>.
      ?subject ?property ?whatever.
      ?property rdf:type ?class.
  }
  ''',
  initNs = { "rdfs": RDFS, "rdf": RDF}
)
# Visualize the results
for r in g.query(q3):
    print(r)


# In[ ]:




