import sys
import re

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import csv

spark = SparkSession.builder.appName('StockSummary').getOrCreate() 
df = spark.read.options(inferSchema='True', delimiter=',', header='True', multiline = 'True',escape = '\"').csv(sys.argv[1])
years = [2013,2014,2015,2016,2017,2018,2019,2020,2021] #end of the years
yearsInEpoch = [0,1388534399,1420070399,1451606399,1483228799,1514764799,1546300799,1577836799,1609459199,1640995199]

# filtramos las reviews que hayan sido actualizadas y vemos el porcentaje de recomendados de los juegos con las reviews actualizadas
for i in range(1,len(yearsInEpoch)):
    dfi = df.filter((df.timestamp_created < yearsInEpoch[i]) & (df.timestamp_created > yearsInEpoch[i-1]))
    dfi = dfi.groupBy("app_name", "app_id").count()
    dfi.write.option("header",True).csv(sys.argv[2]+str(years[i-1]))
