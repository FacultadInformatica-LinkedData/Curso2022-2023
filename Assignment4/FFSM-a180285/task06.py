from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib import XSD

VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")

ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

# **TASK 6.1: Create a new class named "University"**
g.add((ns.University, RDF.type, RDFS.Class))

print("\n\n 6.1 Check new Class (University)")
for s, p, o in g.triples((None, RDF.type, RDFS.Class)):
  print(s,p,o)

# **TASK 6.2: Add "Researcher" as a subclass of "Person"**
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))

print("\n\n 6.2 Check new subClassOf Person (Researcher)")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s,p,o)

# **TASK 6.3: Create a new individual of Researcher named "Jane Smith"**
g.add((ns.JaneSmith, RDF.type, ns.Researcher))

print("\n\n 6.3 Check that JaneSmith Data")
for s, p, o in g.triples((ns.JaneSmith, None, None)):
  print(s,p,o)

# **TASK 6.4: Add to the individual JaneSmith the fullName, given and family names**
g.add((ns.JaneSmith, VCARD.FN, Literal("Jane Smith", datatype=XSD.string)))
g.add((ns.JaneSmith, VCARD.Given, Literal("Jane", datatype=XSD.string)))
g.add((ns.JaneSmith, VCARD.Family, Literal("Smith", datatype=XSD.string)))

print("\n\n 6.4 Check that JaneSmith Data")
for s, p, o in g.triples((ns.JaneSmith, None, None)):
  print(s,p,o)

# **TASK 6.5: Add UPM as the university where John Smith works**
g.add((ns.UPM, RDF.type, ns.University))

# Create a new property. (I'm not that creative naming properties... Sorry)
g.add((ns.worksIn, RDF.type, ns.Property))
g.add((ns.worksIn, RDFS.domain, ns.Person))
g.add((ns.worksIn, RDFS.range, ns.University))

# Create the relationship 
g.add((ns.JonhSmith, ns.worksIn, ns.UPM))

print("\n\n 6.5 Check that JonhSmith worksIn UPM")
for s, p, o in g.triples((ns.JonhSmith, ns.worksIn, ns.UPM)):
  print(s,p,o)