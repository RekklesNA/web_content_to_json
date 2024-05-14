import json
import glob

def merge_files(output_file):
    data = []
    for file in glob.glob("results/result*.txt"):
        with open(file, 'r') as f:
            data.append(json.load(f))
    with open(output_file, 'w') as f:
        for item in data:
            f.write(json.dumps(item))
            f.write('\n')

def main():
    merge_files("merged_results_new.txt")

if __name__ == "__main__":
    main()