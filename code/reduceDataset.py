from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, avg
import csv

bucket =

spark = SparkSession.builder.appName('StockSummary').getOrCreate()

# dataJuegosOriginal = spark.read.options(inferSchema='True', delimiter=',', header='true').csv('steam_games.csv')
dataJuegosOriginal = spark.read.options(inferSchema='True', delimiter=',', header='true').csv(sys.argv[1])

# dataReviews =  spark.read.options(inferSchema='True', delimiter=',', header='True').csv('steam_reviews.csv')
dataReviews =  spark.read.options(inferSchema='True', delimiter=',', header='True').csv(sys.argv[2])

# app_name
titles = dataReviews.select('app_name').distinct().collect()
dataJuegos = dataJuegosOriginal.filter(col('name') in titles)
# header = dataJuegosOriginal.row()
dataJuegosEscribir = spark.createDataframe(dataJuegos,['url','types','name','desc_snippet','recent_reviews','all_reviews','release_date','developer','publisher','popular_tags','game_details','languages','achievements','genre','games_description','mature_content','minimum_requierements','recommended_requierements','original_price','discount_price'])
dataJuegosEscribir.write.csv(sys.argv[3])
