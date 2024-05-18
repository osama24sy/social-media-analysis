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
        response = stub.AnalyzeComment(comment_analysis_pb2.AnalyzeCommentRequest(text=comment['text'], comment_id=comment['comment_id']))

        conn = psycopg2.connect(dbname="digitalpulse", user="osama24sy", password="test123", host="localhost")
        cur = conn.cursor()
        cur.execute("INSERT INTO comments (comment_id, topic, claim, evidence, counterclaim, rebuttal, conclusion) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (response.comment_id, response.topic, response.claim, response.evidence, response.counterclaim, response.rebuttal, response.conclusion)
                )
        conn.commit()
        cur.close()
        conn.close()


for message in consumer:
    comment = message.value
    process_comment(comment)
    print(f"Processed message: {comment}")