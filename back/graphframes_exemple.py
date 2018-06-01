# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:36:19 2018

@author: aduhamel
"""

###############################################################################
#LIBRAIRIES
###############################################################################
from pyspark.sql.session import SparkSession
from pyspark.sql import SQLContext
import pyspark

import os
os.environ["PYSPARK_SUBMIT_ARGS"] = (
    "--packages graphframes:graphframes:0.5.0-spark2.1-s_2.11"
)
###############################################################################


###############################################################################
#Création du spark context
###############################################################################
sc = pyspark.SparkContext.getOrCreate()
conf = pyspark.SparkConf()
conf.setAppName('GraphFrame')
conf.setMaster('local[*]')
conf.set('spark.executor.memory', '16g')
conf.set('spark.executor.cores', '5')
conf.set('spark.cores.max', '5')
conf.set('spark.logConf', True)
sc.stop()
sc = pyspark.SparkContext(conf=conf)
spark = SparkSession(sc)
sqlContext = SQLContext(sc)
###############################################################################

# Create a Vertex DataFrame with unique ID column "id"
v = sqlContext.createDataFrame([
  ("a", "Alice", 34),
  ("b", "Bob", 36),
  ("c", "Charlie", 30),
  ("d", "David", 29),
  ("e", "Esther", 32),
  ("f", "Fanny", 36),
  ("g", "Gabby", 60)
], ["id", "name", "age"])
# Create an Edge DataFrame with "src" and "dst" columns
e = sqlContext.createDataFrame([
  ("a", "b", "friend"),
  ("b", "c", "follow"),
  ("c", "b", "follow"),
  ("f", "c", "follow"),
  ("e", "f", "follow"),
  ("e", "d", "friend"),
  ("d", "a", "friend"),
  ("a", "e", "friend")
], ["src", "dst", "relationship"])
#v.show()
#e.show()

# Create a GraphFrame
from graphframes import *
g = GraphFrame(v, e)

# Query: Get in-degree of each vertex.
#g.inDegrees.show()

# Query: Count the number of "follow" connections in the graph.
#g.edges.filter("relationship = 'follow'").count()
#g.edges.filter("relationship = 'follow'").show()
#g.vertices.filter("age > 30").show()

#motifs = g.find("(a)-[e]->(b); (b)-[e2]->(a)")
#motifs.show()

paths = g.bfs("name = 'Esther'", "age < 32)
paths.show()

#♦results = g.shortestPaths(landmarks=["a", "d"])
#results.show()
#results.select("id", "distances").show()
# Run PageRank algorithm, and show results.
#results = g.pageRank(resetProbability=0.01, maxIter=20)
#results.vertices.select("id", "pagerank").show()
