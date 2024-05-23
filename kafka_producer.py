from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

test_comments = [
    {'comment_id': 1, 'text': 'I think the face on Mars is a natural landform.'},
    {'comment_id': 2, 'text': 'It is definitely made by aliens because it looks too perfect.'},
    {'comment_id': 3, 'text': 'There is no evidence of life on Mars, so it must be natural.'},
    {'comment_id': 4, 'text': 'Some scientists believe it is a trick of light and shadow.'}
]

for comment in test_comments:
    producer.send('comments', comment)

producer.flush()
