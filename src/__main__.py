from data_processing.clean_scripts import clean_text
from langchain_utils.llm_scripts import generate_structured_data
from storage.s3_scripts import read_s3_bucket

def main():
    text = read_s3_bucket("mybucket-qwertyui","unstructuredData.txt")
    text = clean_text(text)
    output = generate_structured_data(text)
    print(output)

if __name__ == "__main__":
    main()