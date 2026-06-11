from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage ,SystemMessage

load_dotenv()

model = init_chat_model(
    "meta-llama/llama-4-scout-17b-16e-instruct",
    model_provider="groq",
    temperature=0.9,
)
print("Choose your ai agent")
print("Press 1 for angry mood")
print("press 2 for happy mood")
print("Press 3 for sad mood")

choice = int(input("tell your response :- "))
if choice == 1 :
    mode = "You are a very angry ai "

elif choice == 2 :
    mode = "You are a happy ai"

else :
    mode = "You are a sad ai "


messages = [
   SystemMessage(content=mode)
]

print("----------------------welcome type 0 to exit the application")

while True:

    prompt = input("You : ")

    if prompt == "0":
        break

    # User message add karo
    messages.append(HumanMessage(content=prompt))

    # Puri history model ko do
    response = model.invoke(messages)

    print("BOT :", response.content)

    # AI response bhi history me save karo
    messages.append(AIMessage(content=response.content))

print (messages)