import json
import time

import redis

from app.celery_app import app


def send_to_client(message: str, client_id: int):
    r = redis.Redis(host='localhost', port=6377, db=0)
    data = json.dumps({"client_id": client_id, "message": message})
    r.publish("ws_messages", data)


@app.task
def do_heavy_task(str):
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    send_to_client(f"Task completed: {str}", client_id=1)
    print("Done!")
