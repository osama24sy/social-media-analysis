from transformers import BertTokenizer, BertForSequenceClassification

# Load saved model and tokenizer
loaded_model = BertForSequenceClassification.from_pretrained('data/bert_clf_ft')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def predict(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    outputs = loaded_model(**inputs)
    logits = outputs.logits
    predicted_class_id = logits.argmax().item()
    
    if predicted_class_id == 0:
        predicted_label = 'Claim'
    elif predicted_class_id == 1:
        predicted_label = 'Fact'
    elif predicted_class_id == 2:
        predicted_label = 'Counterclaim'
    else:
        predicted_label = 'Rebuttal'

    return predicted_label