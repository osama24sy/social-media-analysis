from concurrent import futures
import grpc
import comment_analysis_pb2
import comment_analysis_pb2_grpc
import sys
import logging

from topic_classifier import topic_classify
from opinion_classifier import opinion_classify
from summarizer import summarize
from preprocessor import preprocess_text

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("grpc_server.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CommentAnalysisServicer(comment_analysis_pb2_grpc.CommentAnalysisServicer):
    def AnalyzeComment(self, request, context):
        text = request.text
        comment_id = request.comment_id
        
        try:
            print(f"Comment: '{text}' was received.")

            text = preprocess_text(text)

            topic_id, topic_score = topic_classify(text)
            print(f"THE TOPIC ID IS: {topic_id} - {topic_score}")

            predicted_class = opinion_classify(text)
            print(f"THE OPINION CLASS IS: {predicted_class}")
            
            conclusion = summarize(topic_id, text, predicted_class)
            print(f"THE CONCLUSION IS: {conclusion}")
            
            
            return comment_analysis_pb2.CommentResponse(
                comment_id=comment_id,
                topic_id=topic_id,
                opinion_class=predicted_class,
                conclusion=conclusion
            )
        except Exception as e:
            logging.error(f"Error processing comment {comment_id}: {str(e)}")
            context.set_details(f"Internal error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return comment_analysis_pb2.CommentResponse(
                comment_id=comment_id,
                topic_id=-1,
                opinion_class="Unknown",
                conclusion="Unknown"
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    comment_analysis_pb2_grpc.add_CommentAnalysisServicer_to_server(CommentAnalysisServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
