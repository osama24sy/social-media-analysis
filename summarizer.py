from transformers import pipeline
import psycopg2

generator = pipeline('text-generation', model='gpt2')

def summarize_text(topic_id, text, predicted_class):
    # Fetch topic text from database
    conn = psycopg2.connect(dbname="digitalpulse", user="osama24sy", password="test123", host="localhost")
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM topics WHERE topic_id = %s", (topic_id,))
    prompt = 'Topic= ' + cursor.fetchone()[0]
    cursor.close()

    cursor = conn.cursor()
    cursor.execute("SELECT text, type FROM opinions WHERE topic_id = %s", (topic_id,))
    opinions = cursor.fetchall()
    cursor.close()
    conn.close()

    # Generate summary
    if opinions:
        for row in opinions:
            prompt = prompt + f' {row[1]}= ' + row[0]
    
    prompt += f'{predicted_class}= ' + text + ' TL;DR:'

    summary = generator(prompt, max_new_token=200, min_new_token=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = summary[0]['generated_text']

    ind = summary.find('TL;DR:')
    summary = summary[ind + 6:]
    
    return summary