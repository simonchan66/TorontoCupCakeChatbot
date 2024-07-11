import openai
import os
from dotenv import load_dotenv
from app.chatbot_manager import chatbot_manager

dotenv_path = os.path.join(os.path.dirname(__file__), '.env.local')
load_dotenv(dotenv_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

async def process_chat(user_input: str, chat_history: list) -> str:
    store_info = await chatbot_manager.get_store_info()

    conversation = [
        {"role": "system", "content": f"""You are a helpful assistant for Toronto Cupcake. 
        Your task is to assist customers with cupcake selection, order quantities, and provide additional suggestions. 
        Use the following information about our cupcakes and services:
        
        Cupcakes: {store_info['cupcakes']}
        FAQs: {store_info['faqs']}
        Delivery: {store_info['delivery']}
        
        Be friendly, informative, and always try to upsell or suggest complementary items.
        Always greet the customer and say you're Toronto Cupcake's assistant.
        Please reconfirm orders and provide a summary before ending."""},
    ]
    
    for entry in chat_history:
        conversation.append({"role": "user", "content": entry[0]})
        conversation.append({"role": "assistant", "content": entry[1]})
    
    conversation.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].message['content'].strip()