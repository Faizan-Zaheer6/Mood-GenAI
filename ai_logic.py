import os
import json
from groq import Groq
from dotenv import load_dotenv
from schemas import MoodRequest, MoodResponse

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔴 GLOBAL CHAT MEMORY CONTAINER
CHAT_MEMORY = []

async def generate_mood_content(user_data: MoodRequest) -> MoodResponse:
    global CHAT_MEMORY
    
    # Strict context guardrails and structural schema enforcement
    system_prompt = (
        "You are an expert, respectful poet and emotional companion. "
        "Strict Guardrails: Check the input for bad words or slang insults in Roman Urdu/Hinglish (e.g., 'chawal', 'badtameez'). "
        "If detected, do not write poetry; return a polite refusal instead.\n"
        "Crucial: Always reply strictly in valid JSON format matching this schema:\n"
        '{"mood_detected": "string", "content": "string", "author_or_poet": "string"}'
    )
    
    # Maintain safety compliance at index 0
    if not CHAT_MEMORY:
        CHAT_MEMORY.append({"role": "system", "content": system_prompt})
    else:
        CHAT_MEMORY[0] = {"role": "system", "content": system_prompt}
        
    # Append fresh client interaction to context window
    user_prompt = f"User says/asks: '{user_data.mood}' in {user_data.language} language context."
    CHAT_MEMORY.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  
        messages=CHAT_MEMORY, 
        temperature=0.6,         
        response_format={"type": "json_object"}  
    )

    ai_response_text = response.choices[0].message.content
    raw_json = json.loads(ai_response_text)
    
    # Save state to maintain continuous history threads
    CHAT_MEMORY.append({"role": "assistant", "content": ai_response_text})
    
    return MoodResponse(**raw_json)