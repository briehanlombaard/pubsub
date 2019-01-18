import datetime
import json
import time
import redis


r = redis.Redis()


while True:
    r.publish('wincam-detector', json.dumps(
        {'t': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'}
    ))
    time.sleep(1)
