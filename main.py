from kafka import KafkaConsumer
import json
import grpc
import psycopg2
import comment_analysis_pb2
import comment_analysis_pb2_grpc

consumer = KafkaConsumer('comments',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

def process_comment(comment):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = comment_analysis_pb2_grpc.CommentAnalysisStub(channel)
        response = stub.AnalyzeComment(comment_analysis_pb2.CommentRequest(text=comment['text'], comment_id=comment['comment_id']))

        print(f"Comment ID: {response.comment_id}")
        print(f"Topic ID: {response.topic_id}")
        print(f"Claim: {response.opinion_class}")
        print(f"Conclusion: {response.conclusion}")
        

for message in consumer:
    comment = message.value
    process_comment(comment)
