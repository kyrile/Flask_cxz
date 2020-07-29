from redis import Redis

rd = Redis(host='192.168.43.112',
           db=9,
           decode_responses=True)