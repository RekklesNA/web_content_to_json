def remove_duplicates(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    unique_urls = set(urls)
    with open(file_path, 'w') as file:
        for url in unique_urls:
            file.write(url)

def main():
    remove_duplicates('urls.txt')

if __name__ == "__main__":
    main()