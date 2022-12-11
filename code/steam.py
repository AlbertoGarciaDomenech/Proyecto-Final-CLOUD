# Proyecto final cloud


from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import * 
from pyspark.sql.window import Window
import sys

sc = SparkContext("local", "SteamReviews")

spark = SparkSession.builder \
          .appName("Estudio resenyas steam") \
          .config("spark.some.config.option", "some-value") \
          .getOrCreate()


df_reviews = spark.read.options(header = True, multiLine = True, escape = "\"").csv(sys.argv[1])
df_reviews_with_length = df_reviews.withColumn("len_review", size(split(col("review"), " "))) # aniadimos una columna que incluya la longitud de la review
# CSV utilizado: "steam_reviews.csv"


# Funcion que calcula el numero medio de palabras usadas por review para cada juego
def averageWordForGame():
    df = df_reviews_with_length.select(col("app_name"), col("len_review")).groupBy("app_name").avg("len_review")
    df.show()
    df.write.option("header",True).csv(sys.argv[2])
    

# Funcion que calcula la media de palabras utilizada en una review diferenciando entre reviews favorables y no favorables
def averageWordsByOpinion():
	df = df_reviews_with_length.select(col("app_name"), col("len_review"), col("recommended"))
	df_positive = df.filter(col("recommended") == 'True').groupBy("app_name").avg("len_review")
	df_negative = df.filter(col("recommended") == 'False').groupBy("app_name").avg("len_review")
	df_positive.write.option("header",True).csv(sys.argv[3]) # Longitud de las reviews favorables
	df_negative.write.option("header",True).csv(sys.argv[4]) # Longitud de las reviews negativas


# Funcion que calcula el numero de reviews por cada juego
def numReviewsForGame():
    df_num = df_reviews.groupBy("app_name").count()
    df_num.write.option("header",True).csv(sys.argv[5]) # Numero de reviews por juego


# Funcion que calcula el numero de reviews por cada juego, diferenciando entre los distintos idiomas
def numReviewsForGameAndLenguage():
    df_num = df_reviews.groupBy("app_name", "language").count()
    df_num.write.option("header",True).csv(sys.argv[6]) # Numero de reviews por juego e idioma


# Ver los videojuegos con mayor porcentaje de reviews buenas
def PercentageGoodReviewsPerGame():
    df = df_reviews.groupBy("app_name", "recommended").count().withColumn("porcentaje", col("count")/sum(col("count"))\
        .over(Window.partitionBy(df_reviews['app_name'])))
    df = df.filter(col("recommended") == "True").orderBy(col("porcentaje").desc())
    df.write.option("header",True).csv(sys.argv[7])
    # Luego con pandas podemos hacer filtrado para seleccionar los juegos que tengan bastantes reviews


# Funcion que muestra los lenguajes mas utilizados en las reviews
def MostLanguagesUsed():
    df = df_reviews.groupBy("language").count().orderBy(col('count').desc(), col('language'))
    df.write.option("header", True).csv(sys.argv[8])


# Funcion que devuelve las 30 reviews con mayor 'helpful votes'
def _30mostlikedreviews():
    df = df_reviews.orderBy(col('votes_helpful').desc())
    df = df.filter(col('_c0').between(0, 30)).select(col('app_name'), col('review'))
    df.write.option("header", True).csv(sys.argv[9])


# Funcion que calcula el porcentaje de reviews que recomiendan el juego del que hablan basandose en el idioma
def LanguageAndRecommended():
    df = df_reviews.groupBy("recommended", "language").count()
    df = df.withColumn("porcentaje", col("count")/sum(col("count"))\
        .over(Window.partitionBy(df_reviews['language'])))
    df.write.option("header", True).csv(sys.argv[10])



# Llamadas a las funciones
averageWordForGame()
averageWordsByOpinion()
numReviewsForGame()
numReviewsForGameAndLenguage()
PercentageGoodReviewsPerGame()
MostLanguagesUsed()
_30mostlikedreviews()
LanguageAndRecommended()


