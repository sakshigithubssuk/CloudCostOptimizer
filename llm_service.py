import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
API_TOKEN = os.getenv("HF_API_TOKEN")


#INITIALLY I used - Llama-3 (Permission issues) -> Mistral (Old URL issues) -> Zephyr (Task issues) -> Qwen 2.5 Coder
REPO_ID = "Qwen/Qwen2.5-Coder-32B-Instruct"


client = InferenceClient(token=API_TOKEN, model=REPO_ID)

def clean_json_response(response_text):
    """
    Cleans the AI response to extract only valid JSON.
    """
    try:
        if not response_text: return None

        # Print raw text for debugging 
        # print(f"DEBUG RAW AI TEXT: {response_text[:200]}...") 

        
        start_idx = response_text.find('{')
        list_start = response_text.find('[')
        
        
        if list_start != -1 and (start_idx == -1 or list_start < start_idx):
            start_idx = list_start
            end_idx = response_text.rfind(']') + 1
        else:
            if start_idx == -1: return None
            end_idx = response_text.rfind('}') + 1

        json_str = response_text[start_idx:end_idx]
        return json.loads(json_str)
    except Exception as e:
        print(f"⚠️ JSON Parse Error: {e}")
        return None

def query_llm(messages):
    """
    Sends a chat conversation to the AI.
    """
    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=2000, 
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None
def generate_project_profile(description):
    print("⏳ Asking AI to create profile...")
    messages = [
        {"role": "system", "content": "You are a Cloud Architect. Output ONLY valid JSON. No Markdown. No code blocks."},
        {"role": "user", "content": f"""
        Extract a structured JSON profile from this description:
        "{description}"
        
        Instructions:
        1. Parse the text to find the project name, budget, and requirements.
        2. In "tech_stack", extract ALL mentioned technologies (e.g., database, storage, monitoring, proxies, cloud providers).
        
        REQUIRED JSON STRUCTURE:
        {{
          "name": "Project Name",
          "budget_inr_per_month": 0,
          "description": "Short summary",
          "tech_stack": {{ 
             "frontend": "React/Angular/etc", 
             "backend": "Node/Python/etc", 
             "database": "Postgres/MongoDB/etc", 
             "storage": "S3/Blob/etc", 
             "monitoring": "Tools/Services"
             // Add other keys as needed based on input
          }},
          "non_functional_requirements": ["Scalability", "Security", "etc"]
        }}
        """}
    ]
    text = query_llm(messages)
    return clean_json_response(text)
def generate_mock_billing(profile):
    print("⏳ Asking AI to generate billing data...")
    messages = [
        {"role": "system", "content": "You are a Cloud Billing System. Output ONLY valid JSON List. No Markdown."},
        {"role": "user", "content": f"""
        Generate 10 realistic cloud billing records for this project:
        {json.dumps(profile)}
        
        REQUIRED JSON FORMAT:
        [
          {{ "month": "2025-01", "service": "EC2", "usage_quantity": 720, "unit": "hours", "cost_inr": 1500, "desc": "Web Server" }}
        ]
        """}
    ]
    text = query_llm(messages)
    return clean_json_response(text)

def generate_cost_analysis(profile, billing):
    print("⏳ Asking AI to analyze costs...")
    messages = [
        {"role": "system", "content": "You are a Financial Analyst. Output ONLY valid JSON. No Markdown."},
        {"role": "user", "content": f"""
        Analyze this data:
        Profile: {json.dumps(profile)}
        Billing: {json.dumps(billing)}
        
        REQUIRED JSON STRUCTURE:
        {{
            "analysis": {{
                "total_monthly_cost": 0,
                "budget": 0,
                "is_over_budget": false
            }},
            "recommendations": [
                {{
                    "title": "...",
                    "service": "...",
                    "potential_savings": 0,
                    "cloud_providers": ["AWS", "Azure"]
                }}
            ]
        }}
        """}
    ]
    text = query_llm(messages)
    return clean_json_response(text)