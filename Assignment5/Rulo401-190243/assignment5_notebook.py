# -*- coding: utf-8 -*-
"""Assignment5-Notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AwuH8upnHLhCdWiF3f2n7TihnkUQA3u5
"""
"""
!pip install kgtk==1.0.1

!echo "deb http://downloads.skewed.de/apt bionic main" >> /etc/apt/sources.list
!apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
!apt-get update
!apt-get install python3-graph-tool python3-cairo python3-matplotlib
!apt-get install libcairo2-dev
"""
"""## Preamble: set up the environment and files used in the assignment (remember to restart runtime)"""

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
       --match '()-[r]->()'
       --return 'count(distinct r.label)'
 """)

"""Now, let's count the frequency of those properties. That is, how many instances we can find with each property"""

# Commented out IPython magic to ensure Python compatibility.

kgtk("""
     query -i all 
       --match '()-[r]->()'
       --return 'r.label, count(r)' 
 """)

"""## Simple queries
Some of these queries are simple and will run in the Wikidata endpoint. 
Try both of them using SPARQL and Kypher
"""

# Which actors has Schwarzenegger worked with throughout his career? (Print also the movie)

# (in SPARQL)
"""
SELECT ?acName (GROUP_CONCAT(?fName; SEPARATOR=", ") as ?films) WHERE{
  ?film wdt:P31 wd:Q11424 .
  ?film wdt:P161 wd:Q2685 .
  ?film rdfs:label ?fName FILTER (lang(?fName) = "es").
  ?film wdt:P161 ?ac FILTER(?ac != wd:Q2685).
  ?ac rdfs:label ?acName FILTER (lang(?acName) = "es").
}GROUP BY ?ac ?acName
"""

# In Kypher:
kgtk("""
    query -i all
    --match '(:Q11424)<-[:P31]-(f)-[:P161]->(:Q2685), (fName)<-[:label]-(f)-[:P161]->(ac)-[:label]->(acName)'
    --where 'ac != "Q2685"'
    --return 'acName as Name, fName as Film'
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
SELECT ?partName WHERE{
  wd:Q2685 wdt:P102 ?pParty.
  ?partner wdt:P102 ?pParty .
  ?partner wdt:P31 wd:Q5 FILTER (?partner != wd:Q2685) FILTER NOT EXISTS { ?partner wdt:P570 []}.
  ?partner rdfs:label ?partName FILTER (lang(?partName) = "es").
}LIMIT 5
"""

# Kypher:
kgtk("""
    query -i all
    --match '(:Q2685)-[:P102]->(pparty)<-[:P102]-(partner)-[:P31]->(:Q5), (partner)-[:label]->(partname)'
    --limit 2
    --return 'partname'
""")

# What are the properties that describe an artist?

# In theory this one is heavy on Wikidata

# SPARQL: 
"""
SELECT DISTINCT ?property WHERE{
  ?class wdt:P279* wd:Q483501 .
  ?artist wdt:P106 ?class .
  ?artist ?property ?value .
}
"""


# In Kypher:
kgtk("""
    query -i all
    --match '((:Q483501)<-[:P279star]-()<-[:P106]-(artist)-[r]->())'
    --return 'distinct r.label'
""")

# And a film director?
# SPARQL: 
"""
SELECT DISTINCT ?property WHERE{
  ?class wdt:P279* wd:Q2526255 .
  ?fdirector wdt:P106 ?class .
  ?fdirector ?property ?value .
}
"""


# In Kypher:
kgtk("""
    query -i all
    --match '((:Q2526255)<-[:P279star]-()<-[:P106]-(fdirector)-[r]->())'
    --return 'distinct r.label'
""")

# Embeddings. Run the noebook https://colab.research.google.com/drive/1A55l10voA4jnjoju3fojJWY3buLfaR4i?usp=sharing. 
# Which are the top 10 similar entities to Schwarzenegger? (list below) 
"""
index,node1,node2,label,node1;label,node1;description
0,Q2685,1.0,similarity,'Arnold Schwarzenegger'@en,"'Austrian-American actor, businessman, bodybuilder and politician'@en"
1,Q220918,0.8411656022071838,similarity,'Emilio Estevez'@en,"'American actor, director, and writer'@en"
2,Q94715,0.83599853515625,similarity,'Dagmar Koller'@en,'Austrian actor and singer'@en
3,Q352010,0.8334155082702637,similarity,'David S. Goyer'@en,"'American screenwriter, film director, novelist, and comic book writer'@en"
4,Q345325,0.830280601978302,similarity,'Harry Shearer'@en,'American actor'@en
5,Q212518,0.8279862999916077,similarity,'Patrick Dempsey'@en,'American actor'@en
6,Q181490,0.8246354460716248,similarity,'Teri Hatcher'@en,"'American actress, presenter, writer'@en"
7,Q315763,0.8222377896308899,similarity,'Bill Pullman'@en,'American actor'@en
8,Q38196234,0.8187390565872192,similarity,'Meinhard Schwarzenegger'@en,'Arnold Schwarzenegger\'s brother'@en
9,Q1135627,0.8186355829238892,similarity,'Cortney Palm'@en,'American actress'@en
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
  paths --max_hops 3 
   --path-file paths.tsv 
   --path-mode NONE 
   --path-source source --path-target target 
   -i all --statistics-only
""")

# Retrieve all the family of Schwarzenegger (child/father/mother/sibling/spouse relationships)
  
kgtk("""
    reachable-nodes -i all
        --root Q2685
        --props P40 P22 P25 P3373 P26
        --label Arnold_family
""")

# What are the 10 most relevant actors (pagerank) in the graph? (Use graph-statistics command to calculate page rank, and then filter only actors)
# TO DO  
kgtk("""
  graph-statistics -i all -o $OUT/pagerank.tsv.gz 
    --compute-pagerank True
    --compute-hits False
    --page-rank-property Pdirected_pagerank
    --vertex-in-degree-property Pindegree
    --vertex-out-degree-property Poutdegree
    --output-degrees True
    --output-pagerank True
    --output-hits False \
    --output-statistics-only
    --undirected True
""")

# TO DO: Hint: do the query after calculating the pagerank. See https://github.com/usc-isi-i2/kgtk-notebooks/blob/main/tutorial/06-kg-network-analysis.ipynb for inspiration
kgtk("""
    query -i all -i $OUT/pagerank.tsv.gz 
        --match '
            all: (actor)-[:P106]->(:Q33999),
            pagerank: (actor)-[:Pdirected_pagerank]->(pagerank),
            all: (actor)-[:label]->(acName)'
        --return 'actor as node1, pagerank as node2, acName'
        --order-by 'cast(pagerank, float) desc'
        --limit 10
""")
