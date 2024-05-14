import json
import re


def clean_paragraphs(paragraphs):
    cleaned_paragraphs = []
    for paragraph in paragraphs:
        # Remove unnecessary spaces
        paragraph = paragraph.strip()
        # remove special characters/symbols
        paragraph = re.sub(r'[!?,;]', '', paragraph)
        # Replace \n with space
        paragraph = paragraph.replace('\n', ' ')
        # Replace \u00a0 (non-breaking space) with normal space
        paragraph = paragraph.replace('\u00a0', ' ')
        cleaned_paragraphs.append(paragraph)
    return cleaned_paragraphs


def clean_data(data):
    # Cleaning the title
    title = data.get('title')
    if title:
        title = title.strip()
        title = re.sub(r'[!?,;]', '', title)
        # Replace \n with space in title
        title = title.replace('\n', ' ')
        title = title.replace('\t', ' ')

        # Replace \u00a0 (non-breaking space) with normal space in title
        title = title.replace('\u00a0', ' ')
        title = title.replace('\u00a9', ' ')
        title = title.replace('\u00ae', ' ')
        title = title.replace('\u2013', ' ')


        data['title'] = title
    else:
        data['title'] = ""

    # Cleaning the paragraphs
    data['paragraphs'] = clean_paragraphs(data.get('paragraphs', []))
    return data


def main():
    cleaned_data = []
    with open('merged_results.txt', 'r') as file:
        for line in file:
            data = json.loads(line)
            cleaned_data.append(clean_data(data))
    with open('cleaned_merged_results.txt', 'w') as file:
        for item in cleaned_data:
            file.write(json.dumps(item))
            file.write('\n')


if __name__ == "__main__":
    main()
