# -*- coding: utf-8 -*-
#"""Task07.ipynb
#
#Automatically generated by Colaboratory.

#Original file is located at
    #https://colab.research.google.com/drive/1ofNbNk0ik7d0P2i-FJlOLgl1Qg-hClZB

#**Task 07: Querying RDF(s)**
#"""

!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

#"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

#"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s, "Subclass of Person")

from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?subclass
  WHERE { 
    ?subclass rdfs:subClassOf ns:Person. 
  }
  ''',
  initNs = {"rdfs":RDFS, "ns":ns}
)

for i in g.query(q1):
  print(s, ("Subclass of Person"))

#"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

#"""

for s,p,o in g.triples((None, RDF.type, ns.Person)) :
  print(s)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for r,d,a in g.triples((None, RDF.type, s)):
    print(r)


#SPARQL
q2 = prepareQuery('''
  SELECT ?x
  WHERE { 
    {
      ?x rdf:type ns:Person. 
    }
    UNION {
      ?y (rdfs:subClassOf/rdfs:subClassOf*) ns:Person.
      ?x rdf:type ?y
    }
  }
  
  ''',
  initNs = {"rdfs":RDFS, "rdf":RDF, "ns":ns}
)

for x in g.query(q2):
  print(x)

#"""#**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

#"""

for s,p,o in g.triples((None, RDF.type, ns.Person)) :
  for s2, p2, o2 in g.triples((s, None, None)):
    print(s2, p2, o2)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2,p2,o2 in g.triples((None, RDF.type, s)):
    for s3, p3, o3 in g.triples((s2, None, None)):
      print(s3, p3, o3)

#SPARQL
q3 = prepareQuery('''
  SELECT ?s ?p ?z
  WHERE { 
    {
      ?s rdf:type ns:Person. 
      ?s ?p ?z
    }
    UNION {
      ?ss (rdfs:subClassOf/rdfs:subClassOf*) ns:Person.
      ?s rdf:type ?ss.
      ?s ?p ?z
    }
  }
  
  ''',
  initNs = {"rdfs":RDFS, "rdf":RDF, "ns":ns}
)

for s in g.query(q3):
  print(s)