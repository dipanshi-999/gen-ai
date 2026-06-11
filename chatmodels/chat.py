from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(
    "meta-llama/llama-4-scout-17b-16e-instruct",
    model_provider="groq",
    temperature = 0.9 ,
    
)

response = model.invoke("Write a Poem on cricket")

print(response.content)