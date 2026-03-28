import pika
from pika.exceptions import IncompatibleProtocolError, ConnectionClosedByBroker, AMQPConnectionError
import sys
import os
import time
import datetime
import json
import hashlib
import traceback

from utils import get_rabbitmq_connection, get_couch_client
from job_llm_inference_task import JobLLMInferenceTask

worker_id = hashlib.sha256(os.getpid().to_bytes(8, "big")).hexdigest()[:16]

def log(line, level=1):
    dts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z")
    ll = "INFO"
    if level>1:
        ll = "WARN"
    if level>2:
        ll = "ERR "
    if level>3:
        ll = "CRIT"

    print("[" + dts + "] [" + worker_id + "] [" + ll + "] " + line)

def main():
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue="jobs")

    def callback(ch, method, properties, body):
        uuid_str = body.decode("utf-8")
        log(f"Handling job {uuid_str}")

        worker_mapping = {
                "LLM_INFERENCE_TASK": JobLLMInferenceTask
            }

        try:
            couch_client = get_couch_client()
            couch_client.set_timeout(1)
            couch_client.set_max_retries(1)
            job_md = couch_client.get_document("jobs", uuid_str)
            couch_client.patch_document("jobs", uuid_str, {"worker_id": worker_id})

            def progress_func(prog_num):
                couch_client.patch_document("jobs", uuid_str, {"progress": prog_num})

            try:
                if job_md["type"] in worker_mapping:
                    worker = worker_mapping[job_md["type"]]
                    result = worker().execute(job_md, progress_func)

                    couch_client.patch_document("jobs", uuid_str, {"status": "COMPLETE", "progress": 1, "result": result})
                    log(f"Finished job {uuid_str}")
                else:
                    couch_client.patch_document("jobs", uuid_str, {"status": "ERROR", "msg": "Invalid job type"})
                    log(f"Job {uuid_str} threw an error")
            except Exception as e:
                couch_client.patch_document("jobs", uuid_str, {"status": "ERROR", "msg": str(e), "trace": traceback.format_exc()})
                log(f"Job {uuid_str} threw an error")

        except Exception as e:
            print(e)
            log(f"Job {uuid_str} threw an error on initial access")


    channel.basic_consume(queue="jobs", auto_ack=True, on_message_callback=callback)

    log("Worker ready for jobs")
    channel.start_consuming()

if __name__ == '__main__':
    try:
        while True:
            try:
                main()
            except IncompatibleProtocolError:
                log("RabbitMQ protocol error - Has the server fully booted?", 2)
            except AMQPConnectionError:
                log("Could not connect to RabbitMQ", 3)
            except ConnectionClosedByBroker:
                log("RabbitMQ connection lost", 4)
            time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
