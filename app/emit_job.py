import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="192.168.43.170",
        port="30072",
    )
)

channel = connection.channel()

channel.exchange_declare(exchange="asr", exchange_type="topic", durable=True)

routing_key = "transcribe.short.whisper.cpu"

# message = {
#     "pattern": {"group": "SHORT_DURATION", "processor": "CPU"},
#     "data": {
#         "asr_language": "es",
#         "audio_url": (
#             "/Users/alexander/Downloads/calls/210614222408193_ACD_00001.mp3"
#         ),
#         "duration": 11520,
#         "sample_rate": 8000,
#         "channels": 2,
#         "audio_format": "mp3",
#     },
# }


message = {
    "pattern": {"group": "SHORT_DURATION", "processor": "CPU"},
    "data": {
        "transcription_id": "foo",
        "asr_language": "es",
        "audio_url": (
            "/Users/alexander/Downloads/calls/210614222408193_ACD_00001.mp3"
        ),
        "duration": 11520,
        "sample_rate": 8000,
        "channels": 2,
        "audio_format": "mp3",
    },
}
i = 0
while i < 100:
    i += 1
    message["data"]["transcription_id"] = f"{i}"  # [:-1
    channel.basic_publish(
        exchange="asr", routing_key=routing_key, body=json.dumps(message)
    )
    print(f"{i} sent")


connection.close()
