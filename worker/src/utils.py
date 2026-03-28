import couchbeans
import os
import re
import json
import pika

couch_user = os.environ.get("COUCHDB_ROOT_USER")
couch_password = os.environ.get("COUCHDB_ROOT_PASSWORD")
couch_host = os.environ.get("COUCHDB_HOST")
couch_port = os.environ.get("COUCHDB_PORT", 5984)
couch_base_uri = "http://" + couch_user + ":" + couch_password + "@" + couch_host + ":" + str(couch_port) + "/"

rabbitmq_credentials = pika.PlainCredentials(os.environ.get("RABBITMQ_DEFAULT_USER", "root"), os.environ.get("RABBITMQ_DEFAULT_PASS", "root"))
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.environ.get("RABBITMQ_PORT", 5672)

def get_rabbitmq_connection():
    print("Connecting to RabbitMQ server at " + str(rabbitmq_host) + ":" + str(int(rabbitmq_port)))
    return pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, int(rabbitmq_port), "/", rabbitmq_credentials))

def get_couch_client():
    return couchbeans.CouchClient(couch_base_uri)

def advertise_job(job_id):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue="crab_jobs")
    channel.basic_publish(exchange="", routing_key="crab_jobs", body=job_id)
    connection.close()

def to_snake_case(str_in):
    str_out = re.sub("(?<!^)(?<![A-Z])(?=[A-Z]+)", "_", str_in).lower() # Prepend all strings of uppercase with an underscore
    str_out = re.sub("[^a-z0-9]", "_", str_out) # Replace all non-alphanumeric with underscore
    str_out = re.sub("_+", "_", str_out) # Clean up double underscores
    str_out = re.sub("(^_)|(_$)", "", str_out) # Clean up trailing or leading underscores
    return str_out
