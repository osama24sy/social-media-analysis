from transformers import GPT2Tokenizer, GPT2LMHeadModel
import psycopg2

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def summarize_text(topic_id):
    # Fetch topic text from database
    conn = psycopg2.connect(dbname="digitalpulse", user="osama24sy", password="test123", host="localhost")
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM topics WHERE topic_id = %s", (topic_id,))
    text = cursor.fetchone()[0]
    cursor.close()

    cursor = conn.cursor()
    cursor.execute("SELECT text FROM opinions WHERE topic_id = %s", (topic_id,))

    inputs = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=100, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary