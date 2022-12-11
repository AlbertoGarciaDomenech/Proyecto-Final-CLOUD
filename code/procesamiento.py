from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import csv
import sys

spark = SparkSession.builder.appName('StockSummary').getOrCreate()

# comando utilizado:
# gcloud dataproc jobs submit pyspark --cluster example-cluster --region=europe-west6 $BUCKET/procesamiento.py -- $BUCKET/steam_reviews.csv $BUCKET/languages.csv $BUCKET/videogamesWithMoreReviews.csv $BUCKET/videogamesWithLessReviews.csv $BUCKET/possitiveReviews.csv $BUCKET/negativeReviews.csv

# CVS utilizado: "steam_reviews.csv"
dataset = spark.read.options(inferSchema='true', delimiter = ',', header='true', multiLine = 'true', escape = '\"').csv(sys.argv[1])

# Función que calcula los idiomas más utilizados en las reseñas
def mostUsedLanguages():
    languages = dataset.groupBy('language').count().orderBy(col('count').desc(), col('language'))
    languages.show(10) # se muestran por pantalla los 10 idiomas mas utilizados
    languages.write.option("header",True).csv(sys.argv[2])

# Función que calcula los videojuegos con más y menos reseñas
def videogames():
    videogames = dataset.groupBy('app_name').count()
    # videojuegos con más reseñas
    mas = videogames.orderBy(col('count').desc(), col('app_name'))
    mas.show(10) # se muestran por pantalla los 10 videojuegos con más reseñas
    mas.write.option("header",True).csv(sys.argv[3])
    # videojuegos con menos reseñas
    menos = videogames.orderBy(col('count').asc(), col('app_name'))
    menos.show(10) # se muestran por pantalla los 10 videojuegos con menos reseñas
    menos.write.option("header",True).csv(sys.argv[4])

# Función que calcula el número de reviews positivas por cada videojuego
def reviewsPositivas():
    positivas = dataset.filter(col('recommended') == 'True').groupBy('app_id').count()
    positivas.show() # se muestran por pantalla el número de reviews positivas por cada videojuego
    positivas.write.option("header",True).csv(sys.argv[5])

# Función que calcula el número de reviews negativas por cada videojuego
def reviewsNegativas():
    negativas = dataset.filter(col('recommended') == 'False').groupBy('app_id').count()
    negativas.show() # se muestran por pantalla el número de reviews negativas por cada videojuego
    negativas.write.option("header",True).csv(sys.argv[6])

# LLamadas a las funciones
mostUsedLanguages()
videogames()
reviewsPositivas()
reviewsNegativas()
