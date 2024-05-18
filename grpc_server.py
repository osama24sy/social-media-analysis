from concurrent import futures
import grpc
import comment_analysis_pb2
import comment_analysis_pb2_grpc

from preprocessor import preprocess_text
from classifier import classify_text
from summarizer import summarize_text

class CommentAnalysisServicer(comment_analysis_pb2_grpc.CommentAnalysisServicer):
    def AnalyzeComment(self, request, context):
        text = request.text
        comment_id = request.comment_id

        # Preprocess text
        preprocessed_text = preprocess_text(text)

        # Classify text
        claim_label, claim_score = classify_text(preprocessed_text)
        evidence_label, evidence_score = classify_text(preprocessed_text)
        counterclaim_label, counterclaim_score = classify_text(preprocessed_text)
        rebuttal_label, rebuttal_score = classify_text(preprocessed_text)

        # Summarize text
        conclusion = summarize_text(claim_label, evidence_label, counterclaim_label, rebuttal_label)

        return comment_analysis_pb2.AnalyzeCommentResponse(
            comment_id=comment_id,
            topic='Mars Face',
            claim=claim_label,
            evidence=evidence_label,
            counterclaim=counterclaim_label,
            rebuttal=rebuttal_label,
            conclusion=conclusion,
        )
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    comment_analysis_pb2_grpc.add_CommentAnalysisServicer_to_server(CommentAnalysisServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()