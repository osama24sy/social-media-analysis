from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

def classify_text(text):
    result = classifier(text)
    return result[0]['label'], result[0]['score']