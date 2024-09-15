import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0, encoding="utf-8", decode_responses=True)
# redis는 원래 byte 형태로 저장되나, encoding과 decode_responses=True로 설정하면
# 데이터를 꺼내올 때, byte가 아닌 python에서 제공하는 데이터 타입으로 변환해서 쉽게 사용할 수 있다.
