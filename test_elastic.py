# test_elasticsearch_connection.py

from elasticsearch import Elasticsearch
from config.settings import ELASTICSEARCH_API_KEY, ELASTICSEARCH_CLOUD_ID

def probar_conexion():
    es = Elasticsearch(
        cloud_id=ELASTICSEARCH_CLOUD_ID,
        api_key=ELASTICSEARCH_API_KEY
    )

    try:
        info = es.info()
        print("Conexión exitosa a Elasticsearch Cloud")
        print(info)
    except Exception as e:
        print(f"Error al conectar con Elasticsearch Cloud: {e}")

if __name__ == '__main__':
    probar_conexion()