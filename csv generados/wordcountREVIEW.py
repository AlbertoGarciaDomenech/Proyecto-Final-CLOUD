import sys
import re

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
# from wordcloud import WordCloud, STOPWORDS
import csv

spark = SparkSession.builder.appName('StockSummary').getOrCreate() 
df = spark.read.options(inferSchema='True', delimiter=',', header='True', multiline = 'True',escape = '\"').csv(sys.argv[1])
# stopwords = set(STOPWORDS)
# filtramos al ingles y filtramos a recomendado/no recomendado
dfPos = df.filter( (col('language') == "english") & (col('recommended') == "True"))
dfNeg = df.filter( (col('language') == "english") & (col('recommended') == "False"))
dfPos = dfPos.withColumn('word', explode(split(dfPos.review, ' '))).groupBy('word').count()
dfPos = dfPos.filter(col('count') > 10)# & ~(col('word').isin(stopwords)))
dfNeg = dfNeg.withColumn('word', explode(split(dfNeg.review, ' '))).groupBy('word').count()
dfNeg = dfNeg.filter(col('count') > 10)# & ~(col('word').isin(stopwords)))

# guardamos en csv para generar wordcloud con palabras y freq

dfPos = dfPos.select('word','count')
dfPos.coalesce(1).write.option("header",True).csv(sys.argv[2])

dfNeg = dfNeg.select('word','count')
dfNeg.coalesce(1).write.option("header",True).csv(sys.argv[3])
