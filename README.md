# Proyecto-Final-CLOUD
* Javier García Viana
* Daniel Cobos Peñas
* Francisco Prieto Gallego
* Alberto García Doménech

# Links de Interés
* [Presentación idea](https://docs.google.com/presentation/d/1bndRXzmOWwVLmoXwjcvGRPQskVZk58VQPU7JXqMCTfA/edit?usp=sharing)
* [Presentación proyecto](https://docs.google.com/presentation/d/1aw33uY-hWUdKajTlh4gqRxzWQbkhSbJq-773M9P2hH8/edit?usp=sharing)
* [Página web del proyecto](https://danicobos01.github.io/)

# Descripción:
Ánalisis relacional y estudio de mercado de alrededor de 21 millones reseñas de 300 diferentes videojuegos utilizando técnicas de big data y herramientas de cloud computing

# Datos
* [Página de Kaggle del dataset de reseñas](https://www.kaggle.com/datasets/najzeko/steam-reviews-2021)

Dataset de 21 millones de reseñas en  diferentes idiomas con las siguientes características: app_id, app_name, review_id, language, review, timestamp_created, timestamp_updated, recommended, votes_helpful.

* [Página de Kaggle del dataste de los juegos](https://www.kaggle.com/datasets/trolukovich/steam-games-complete-dataset)

Dataset de la información de 40.000 juegos de la plataforma Steam con las siguientes características: url, types, name, desc_snippet, recent_reviews, all_reviews, release_date, developer, publisher, popular_tags.

# ¿Cómo ejecutar el código?
* Usar Spark en local:

Para poder ejecutar el código que realiza un procesamiento de los datos, es necesario instalar Java en tu dispositivo Linux. Se puede instalar con el siguiente comando:

  *sudo apt install default-jre*
  
Una vez instalado, comprobamos que verdaderamente se ha instalado con el siguiente comando:

  *java -version*
  
También se necesita Python, pero no es necesario instalarlo porque suele suele venir instalado por defecto en Linux.

Habiendo instalado Java, es momento de instalar Spark:

  *curl -O https://archive.apache.org/dist/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz*
  
  *tar xvf spark-3.3.1-bin-hadoop3.tgz*
  
  *sudo mv spark-3.3.1-bin-hadoop3 /usr/local/spark*
  
  *echo 'PATH="$PATH:/usr/local/spark/bin"' >> ~/.profile*
  
  *source ~/.profile*
  
Se cargan los archivos necesarios.

Ahora que está instalado Spark y los archivos necesarios están cargados, se puede realizar el procesamiento de datos mediante el envío de trabajos a Spark con el siguiente comando:

  *spark-submit yourFile.py inputFile(s).extension outputFile(s).extension (opcional)*
  
* Usar un Cluster Hadoop en Google Cloud:

Para poder ejecutar el código que procesa los datos, es necesario crear un cluster Hadoop. Se puede utilizar una región cualquiera, en nuestro caso hemos utilizado europe-west6. Para crearlo, se puede utilizar el siguiente comando:

  *gcloud dataproc clusters create nombre-cluster --region europe-west6 --enable-component-gateway --master-boot-disk-size 50GB --worker-boot-disk-size 50GB*
  
Una vez creado el cluster, es necesario crear un bucket donde se almacenarán, tanto los archivos con los datos, como los archivos de entrada y salida.

Para crear un cluster, es necesario especificar una región, que puede ser cualquiera de las disponibles.

Ahora es momento de subir al cluster los archivos que contienen los datos, y los archivos de contienen el código para procesar los datos.

Habiendo subido todos los archivos necesarios al bucket, para poder realizar el procesamiento de datos mediante el envío de trabajos a Spark, es necesario especificar el bucket, que se puede hacer con el siguiente comando:

  *BUCKET=gs://nombre-bucket*
  
Procedemos a enviar el trabajo a Spark:

  *gcloud dataproc jobs submit pyspark --cluster nombre-cluster --region=europe-west6 $BUCKET/archivoParaProcesar.py -- $BUCKET/archivo(s)DeDatos $BUCKET/output(s)*
  
También se puede realizar una ejecución paralela con distintos nodos mediante las siguientes opciones, pero ejecutándolo desde el nodo master del cluster con el comando:

  *spark submit --num-executors numExecutors --executor-cores numCores <script>*
