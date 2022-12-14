# -*- coding: utf-8 -*-
"""Copy of Assignment-Notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zIM8LBhKovxvkRjA6bIhI8KKSYTvnNAl


!pip install kgtk==1.0.1

!echo "deb http://downloads.skewed.de/apt bionic main" >> /etc/apt/sources.list
!apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
!apt-get update
!apt-get install python3-graph-tool python3-cairo python3-matplotlib
!apt-get install libcairo2-dev

## Preamble: set up the environment and files used in the assignment (remember to restart runtime)"""

import io
import os
import subprocess
import sys

import math
import numpy as np
import pandas as pd
from graph_tool.all import *
from IPython.display import display, HTML

from kgtk.configure_kgtk_notebooks import ConfigureKGTK
from kgtk.functions import kgtk, kypher

# Parameters

# Folder on local machine where to create the output and temporary folders
input_path = None
output_path = "/tmp/projects"
project_name = "assignment"

"""The following command will download all the files you  need for the assignment:"""

files = [
    "all",
    "label",
    "alias",
    "description",
    "external_id",
    "monolingualtext",
    "quantity",
    "string",
    "time",
    "item",
    "wikibase_property",
    "qualifiers",
    "datatypes",
    "p279",
    "p279star",
    "p31",
    "in_degree",
    "out_degree",
    "pagerank_directed",
    "pagerank_undirected"
]
ck = ConfigureKGTK(files)
ck.configure_kgtk(input_graph_path=input_path,
                  output_path=output_path,
                  project_name=project_name)

"""The KGTK setup command defines environment variables for all the files so that you can reuse the Jupyter notebook when you install it on your local machine."""

ck.print_env_variables()

# Commented out IPython magic to ensure Python compatibility.
# %%time
ck.load_files_into_cache()

"""# About this assignment.
This assignment is based on https://github.com/usc-isi-i2/kgtk-notebooks/tree/main/tutorial. If you have any questions or doubts, it is encouraged to look how the tutorial performs the different operations.

Additional information can be found in https://kgtk.readthedocs.io/

## Simple graph statistics

Let's calculate first some statistics about the KG. Count the number of instances:
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
kgtk("""
    query -i all
      --match '()-[]->()'
      --return 'count()'
""")

"""Now, count the number of distinct properties: 

"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
kgtk("""
    query -i all
      --match '()-[p]->()'
      --return 'count(distinct p.label)'
""")

"""Now, let's count the frequency of those properties. That is, how many instances we can find with each property"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
kgtk("""
    query -i all
      --match '()-[p]->()'
      --return 'p.label, count(p)'
""")

"""## Simple queries
Some of these queries are simple and will run in the Wikidata endpoint. 
Try both of them using SPARQL and Kypher
"""

# Which actors has Schwarzenegger worked with throughout his career? (Print also the movie)

# (in SPARQL)
"""
SELECT ?acName (GROUP_CONCAT(?mName; SEPARATOR=", ") as ?movie) WHERE{
  ?movie wdt:P31 wd:Q11424 .
  ?movie wdt:P161 wd:Q2685 .
  ?movie rdfs:label ?fName FILTER (lang(?mName) = "es") .
  ?movie wdt:P161 ?ac FILTER (?actor != wd:Q2685) .
  ?actor rdfs:lavel ?acName FILTER (lang(?acName) = "es") . 
}GROUP BY ?actor ?acName
"""

# In Kypher:
kgtk("""
    query -i all
      --match '(:Q11424)<-[:P31]-(m)-[:P161]->(:Q2685), (mName)<-[:label]-(m)-[:P161]->(actor)-[:label]->(acName)'
      --where 'actor != "Q2685"'
      --return 'acName as Name, mName as Movie'
""")

# How many awards does Schwarzenegger have?

# SPARQL:
"""
SELECT (count(?award) as ?nAwards) WHERE{
  wd:Q2685 wdt:P166 ?award
}
"""

# Kypher:
kgtk("""
    query -i all
    --match '(:Q2685)-[:P166]->()'
    --return 'count()'
""")

# Retrieve at least two members of Schwarzenegger's political party. Make sure only persons are returned
# SPARQL:
"""
SELECT ?partyName WHERE{
  wd:Q2685 wdt:P102 ?poliParty .
  ?member wdt:P102 ?poliParty .
  ?member wdt:P31 wd:Q5 FILTER (?member != wd:Q2685) FILTER NOT EXISTS {?member wdt:P570 []} .
  ?member rdfs:label ?partyName FILTER (lang(?partyName) = "es") .
} LIMIT 3
"""

# Kypher:
kgtk("""
    query -i all
    --match '(:Q2685)-[:P102]->(poliparty)<-[:P102]-(member)-[:P31]->(:Q5),(member)-[:label]->(partyMemberName)'
    --limit 3
    --return 'partyMemberName'
""")

# What are the properties that describe an artist?

# In theory this one is heavy on Wikidata

# SPARQL: 
"""
SELECT DISTINCT ?properties WHERE{
  ?class wdt:P279* wd:Q483501 .
  ?artist wdt:P106 ?class .
  ?artist ?properties ?val .
}
"""

# In Kypher:
kgtk("""
    query -i all
    --match '((:Q483501)<-[:P279star]-()<-[:P106]-(artist)-[p]->())'
    --return 'distinct p.label'
""")

# And a film director?
# SPARQL: 
"""
SELECT DISTINCT ?properties WHERE{
  ?class wdt:P279* wd:Q2526255 .
  ?director wdt:P106 ?class .
  ?dircetor ?properties ?val .
}
"""

# In Kypher:
kgtk("""
    query -i all
    --match '((:Q2526255)<-[:P279star]-()<-[:P106]-(director)-[p]->())'
    --return 'distinct p.label'
""")

# Embeddings. Run the noebook https://colab.research.google.com/drive/1A55l10voA4jnjoju3fojJWY3buLfaR4i?usp=sharing. 
# Which are the top 10 similar entities to Schwarzenegger? (list below) 
"""
0	Q2685	1.0	similarity	'Arnold Schwarzenegger'@en	'Austrian-American actor, businessman, bodybuilder and politician'@en
1	Q2263	0.8721055388450623	similarity	'Tom Hanks'@en	'American actor and producer'@en
2	Q193048	0.8692933320999146	similarity	'Laurence Fishburne'@en	'Award-winning American film, theatre, and television actor, film director, film producer, and playwright'@en
3	Q1371229	0.8644353747367859	similarity	'Norm Macdonald'@en	'Canadian comedian'@en
4	Q3128023	0.8484771847724915	similarity	'Harvey Bernhard'@en	'American film producer (1924-2014)'@en
5	Q710169	0.8452587127685547	similarity	'Courtney B. Vance'@en	'American actor'@en
6	Q363666	0.845219075679779	similarity	'Jerry Zucker'@en	'American film director'@en
7	Q455279	0.8450338840484619	similarity	'Joe Dante'@en	'American Filmmaker'@en
8	Q482907	0.8416696786880493	similarity	'Bryan Adams'@en	'Canadian guitarist, singer, composer, record producer, photographer, philanthropist, and activist'@en
9	Q192165	0.8397883772850037	similarity	'Danny Glover'@en	'American actor, film director and political activist'@en
"""

"""## Network analysis
Print all the paths between Schwarzenegger and Trump

## Note that **you have to create a file `paths.tsv` with the node pairs you want to find the paths for. Upload it in the "content" folder**

"""

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# cat <<EOF >$TEMP/path-query.tsv
# node1	node2	label
# Q2685	Q22686	path

kgtk("""
    add-labels -i $TEMP/path-query.tsv
""")

# Calculate all the paths between Trump and Schwarzenegger (max hops: 3)  
kgtk("""
    paths --max-hops 3 
      --path-file paths.tsv
      --path-mode NONE
      --path-source source
      --path-target target
      -i all --statistics-only
""")

# Retrieve all the family of Schwarzenegger (child/father/mother/sibling/spouse relationships)
kgtk("""
    reachable-nodes -i all
      --root Q2685
      --props P40 P22 P25 P3373 P26
      --label Schwarzenegger_family
""")

# What are the 10 most relevant actors (pagerank) in the graph? (Use graph-statistics command to calculate page rank, and then filter only actors)
kgtk("""
    graph-statistics -i all -o $OUT/pagerank.tsv.gz
      --compute-pagerank True
      --compute-hits False
      --page-rank-property Pdirected_pagerank
      --vertex-in-degree-property Pindegree
      --vertex-ouyt-degree-property Poutdegree
      --output-degrees True
      --output-pagerank True
      --output-hits False \
      --output-statistics-only
      --undirected True
""")

#Hint: do the query after calculating the pagerank. See https://github.com/usc-isi-i2/kgtk-notebooks/blob/main/tutorial/06-kg-network-analysis.ipynb for inspiration
kgtk("""
  query -i all -i $OUT/pagerank.tsv.gz
    --match 'all: (actor)-[:P106]->(:Q33999),
            pagerank: (actor)-[:Pdirected_pagerank]->(pagerank),
            all: (actor)-[:label]->(acName)'
    --return 'actor as node1, pagerank as node2, acName'
    --order-by 'cast(pagerank, float) desc'
    --limit 10
""")