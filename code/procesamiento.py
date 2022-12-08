from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import csv
import sys

spark = SparkSession.builder.appName('StockSummary').getOrCreate()

#steam_reviews.csv
dataset = spark.read.options(inferSchema='true', delimiter = ',', header='true', multiLine = 'true', escape = '\"').csv(sys.argv[1])

#get languages most used
dataset.groupBy('language').count().orderBy(col('count').desc(), col('language')).show(10)

#videogames
videogames = dataset.groupBy('app_name').count()

#get videogames most used
videogames.orderBy(col('count').desc(), col('app_name')).show(10)

#get videogames least used
videogames.orderBy(col('count').asc(), col('app_name')).show(10)

#get possitive reviews
dataset.filter(col('recommended') == 'True').groupBy('app_id').count().show()

#get negative reviews
dataset.filter(col('recommended') == 'False').groupBy('app_id').count().show()
