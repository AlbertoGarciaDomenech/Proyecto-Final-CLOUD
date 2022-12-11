#!/usr/bin/python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import csv
from collections import OrderedDict 



import sys
import re

spark = SparkSession.builder.appName('StockSummary').getOrCreate()

# sys.argv[1] = steam_games.csv
dataJuegosOriginal = spark.read.options(inferSchema='True', delimiter=',', header='true').csv(sys.argv[1])
# sys.argv[2] = steam_reviews.csv
dataReviews =  spark.read.options(inferSchema='True', delimiter=',', header='True', multiline = 'True',escape = '\"').csv(sys.argv[2])

# lista de id de juegos que aparecen en dataset de reviews 
titles = dataReviews.rdd.map(lambda x: x.app_id).collect()
titlesList = (list(dict.fromkeys(titles)))


# convertir columna url a id en dataset juegos -> id entre app/ ID /
dataJuegos = dataJuegosOriginal.withColumn('Id', regexp_extract(col('url'), '(app\/)(\\d+)(\/)', 2))

# filtrar los juegos que aparezcan en dataset reviews
dataJuegos = dataJuegos.filter(col('Id').isin(titlesList))


# print("Ids en juegos:" , dataJuegos.select('Id').collect())
# print("Ids en reviews:" , titlesList)

# guardar en csv nuevo dataset Juegos en sys.argv[3]=datasetReduced.csv
dataJuegos.coalesce(1).write.option("header",True).csv(sys.argv[3])

