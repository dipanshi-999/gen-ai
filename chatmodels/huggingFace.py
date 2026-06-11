from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import ChatHuggingFace ,HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Pro"
)

model = ChatHuggingFace(llm=llm)

response = model.invoke("Who are You ?")

print(response.content)