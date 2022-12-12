from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, length
import csv
import sys

spark = SparkSession.builder.appName('Steam').getOrCreate()

# comando utilizado:
# gcloud dataproc jobs submit pyspark --cluster example-cluster --region=europe-west6 $BUCKET/procesamiento.py
#  -- $BUCKET/steam_reviews.csv $BUCKET/languages.csv $BUCKET/videogamesWithMoreReviews.csv 
# $BUCKET/videogamesWithLessReviews.csv $BUCKET/possitiveReviews.csv $BUCKET/negativeReviews.csv
# $BUCKET/porcentajeModificadas.csv $BUCKET/numeroModificadas.csv $BUCKET/steam_games_reduced.csv $BUCKET/num_games.csv $BUCKET/all_games.csv

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

#porcentaje de reviews que han sido modificadas para cada videojuego
def porcentajeModificadas():
    reviews = dataset.groupBy('app_name').count().withColumn('numReviews', col('count'))
    reviewsModificadas = dataset.filter(col('timestamp_updated') != col('timestamp_created')).groupBy('app_name').count().withColumn('numReviewsModificadas', col('count'))
    
    final = reviewsModificadas.join(reviews,['app_name']).withColumn('porcentaje', col('numReviewsModificadas')*100/col('numReviews'))
    final.show()
    f1 = final.select('app_name', 'porcentaje')
    f1.show()
    f1.write.option("header",True).csv(sys.argv[7])

#numero de reviews que han sido modificadas para cada videojuego
def reviewsModificadas():
    reviewsModificadas = dataset.filter(col('timestamp_updated') != col('timestamp_created')).groupBy('app_name').count()
    reviewsModificadas.show()
    reviewsModificadas.write.option("header",True).csv(sys.argv[8])

# LLamadas a las funciones
mostUsedLanguages()
videogames()
reviewsPositivas()
reviewsNegativas()
porcentajeModificadas()
reviewsModificadas()

# CSV: steam_games_reduced
#datagames = spark.read.options(inferSchema='true', delimiter = ',', header='true', multiLine = 'true', escape = '\"').csv(sys.argv[9])

def aniosJuegos():
    anios = datagames.withColumn('year', split(datagames['release_date'], ',').getItem(1)).filter(col('year').isNotNull()).filter(length(col('year')) == 5)
    numVideojuegos = anios.groupBy('year').count()
    numVideojuegos.show()
    numVideojuegos.write.option("header",True).csv(sys.argv[10])
    
    all_videogames = anios.select('name', 'year')
    all_videogames.show() #cada año con su fecha de lanzamiento
    all_videogames.write.option("header",True).csv(sys.argv[11])

#aniosJuegos()