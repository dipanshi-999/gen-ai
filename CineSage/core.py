from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel 
from typing import List,Optional 
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

model = init_chat_model(
    "meta-llama/llama-4-scout-17b-16e-instruct",
    model_provider="groq",
)

class Movie(BaseModel):
    title:str
    release_year : Optional[int]
    genre:List[str]
    director : Optional[str]
    cast:List[str]
    rating:Optional[float]
    summary:str


parser = PydanticOutputParser(pydantic_object=Movie)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert movie information extraction agent.

Extract all available information from the given paragraph.

{format_instructions}
"""
    ),
    (
        "human",
        "{paragraph}"
    )
])



print("Paste your paragraph (type END on a new line when finished):")

lines = []

while True:
    line = input()
    if line == "END":
        break
    lines.append(line)

para = "\n".join(lines)

final_prompt = prompt.invoke(
    {"paragraph": para,
     "format_instructions":parser.get_format_instructions()}
)

response = model.invoke(final_prompt)

print(response.content)


