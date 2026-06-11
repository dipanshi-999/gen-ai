from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

texts = [
    "hello i am dipanshi gupta"
    "hello your name is youtube"
    "And You are very beautiful"
]

vector = embeddings.embed_documents(texts)

print(len(vector))
print(vector[:5])