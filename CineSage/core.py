from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = init_chat_model(
    "meta-llama/llama-4-scout-17b-16e-instruct",
    model_provider="groq",
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert Information Extraction Agent.

Analyze the given paragraph and extract the most useful information.

Please provide:

1. Entity Type (Movie, Book, Company, Person, Event, Product, etc.)
2. Title / Name
3. Important People
4. Genre / Category
5. Release Year / Date (if available)
6. Main Topic or Plot
7. Ratings or Scores (if available)
8. Important Keywords
9. Interesting Facts
10. A quick summary (2-3 lines)
        """
    ),
    (
        "human",
        """
Extract information from this paragraph:

{paragraph}
        """
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
    {"paragraph": para}
)

response = model.invoke(final_prompt)

print(response.content)