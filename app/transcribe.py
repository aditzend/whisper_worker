import pika
import logging
import json
import whisper
from whisper.utils import write_srt, write_vtt
from whisper import tokenizer

from os import path
from pathlib import Path
import torch

SAMPLE_RATE = 16000
LANGUAGE_CODES = sorted(list(tokenizer.LANGUAGES.keys()))
model_name = "medium"
if torch.cuda.is_available():
    model = whisper.load_model(model_name).cuda()
else:
    model = whisper.load_model(model_name)
    model_lock = Lock()

logger = logging.getLogger(__name__)


def run_dual_sox(ch, method, properties, body):
    logger.info(" [x] %r:%r" % (method.routing_key, body.decode()))
    message = json.loads(body.decode())

    logger.warning(f"{message['data']['transcription_id']}")
    logger.info("done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume(queue_name="whisper_transcription_jobs"):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="192.168.43.170", port="30072"),
    )

    channel = connection.channel()

    channel.exchange_declare(
        exchange="asr", exchange_type="topic", durable=True
    )
    result = channel.queue_declare(
        queue="whisper", exclusive=False, durable=True
    )

    queue_name = result.method.queue

    channel.queue_bind(
        exchange="asr",
        queue=queue_name,
        routing_key="transcribe.*.whisper.*",
    )
    logger.info(f"Waiting for transcription jobs on {queue_name}")

    channel.basic_consume(
        queue=queue_name, on_message_callback=run_dual_sox, auto_ack=False
    )

    channel.start_consuming()
