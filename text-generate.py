import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import json

def clean_text(text):
    # Remove unnecessary characters and extra spaces
    text = text.replace('\n', ' ').replace('\r', ' ').strip()
    return text

def fetch_content_and_summarize(url):
    try:
        # Get website content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract website title
        title = soup.title.string if soup.title else "No Title"

        # Extract and clean up the text
        paragraphs = soup.find_all('p')
        text = ' '.join([clean_text(para.get_text()) for para in paragraphs])

        # Dynamically truncate text and handle it in segments
        max_length = 1024
        segments = [text[i:i + max_length] for i in range(0, len(text), max_length)]

        # Summarize the text using the specified pre-trained model
        summarizer = pipeline('summarization', model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")

        # Generate and merge summaries
        summary_parts = []
        for segment in segments:
            summary = summarizer(segment, max_length=512, min_length=150, do_sample=False)
            summary_parts.append(summary[0]['summary_text'])

        final_summary = ' '.join(summary_parts)
        final_summary += f" If you need more information please visit {url}"

        return title, final_summary
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None, None

def main():
    input_file = 'urls.txt'
    output_file = 'summary.json'

    # Create an empty JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump([], file)

    # Read URL file
    with open(input_file, 'r') as file:
        urls = [url.strip() for url in file.readlines() if url.strip()]

    results = []
    for url in urls:
        title, summary = fetch_content_and_summarize(url)
        if title and summary:
            result = {
                "instruction": "tell me about the:",
                "input": title,
                "output": summary
            }
            results.append(result)

            # Real-time update of JSON file
            with open(output_file, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                data.append(result)
                file.seek(0)
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.flush()

if __name__ == "__main__":
    main()
