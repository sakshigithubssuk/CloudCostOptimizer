import os
import json
import re
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
API_TOKEN = os.getenv("HF_API_TOKEN")
REPO_ID = "Qwen/Qwen2.5-Coder-32B-Instruct"
client = InferenceClient(model=REPO_ID, token=API_TOKEN)

def clean_json_response(text):
    """
    Robustly extracts JSON from raw LLM output, handling Markdown fences
    and extra conversation text.
    """
    try:
        if not text:
            return None
        text = text.replace("```json", "").replace("```", "").strip()
        # 2. Find the first '{' or '['
        start_brace = text.find("{")
        start_bracket = text.find("[")
     
        if start_brace == -1 and start_bracket == -1:
            return None
        
        if start_brace != -1 and (start_bracket == -1 or start_brace < start_bracket):
            start = start_brace
            end = text.rfind("}") + 1
        else:
            start = start_bracket
            end = text.rfind("]") + 1

        if end <= start:
            return None

        json_str = text[start:end]
        return json.loads(json_str)

    except json.JSONDecodeError as e:
        print(f"⚠️ JSON Decode Error: {e}")
       
        return None
    except Exception as e:
        print(f"⚠️ General Parsing Error: {e}")
        return None
def query_llm(messages, max_tokens=1500):
    try:
        response = client.chat_completion(
            messages=messages,
            temperature=0.1, 
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ API Error:", e)
        return None
def generate_project_profile(description):
    print("⏳ Generating project profile...")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a Cloud Solution Architect. "
                "Extract structured data from the user description. "
                "Return ONLY valid JSON. No markdown formatting, no conversational text."
            )
        },
        {
            "role": "user",
            "content": f"""
Analyze the following project description and generate a JSON profile.

CRITICAL INSTRUCTION FOR "NAME": 
1. If the project name is explicitly stated, use it.
2. If NO name is stated, you MUST generate a creative, professional name based on the functionality (e.g., "EcoTrack", "FinWiz", "AutoMate"). Do not leave it empty.

Return EXACTLY this JSON structure:
{{
  "name": "Project Name string",
  "budget_inr_per_month": 0,
  "description": "A refined summary of the project",
  "tech_stack": {{
    "backend": "Language/Framework",
    "database": "Specific Database",
    "storage": "Type of storage",
    "monitoring": "Tool name",
    "analytics": "Tool name"
  }},
  "non_functional_requirements": ["Requirement 1", "Requirement 2"]
}}

Input Description:
{description}
"""
        }
    ]

    return clean_json_response(query_llm(messages))

def generate_mock_billing(profile):
    if not profile:
        print("⚠️ Skipping billing generation (No profile data)")
        return None
        
    print(f"⏳ Generating synthetic billing for '{profile.get('name', 'Unknown')}'...")

    messages = [
        {
            "role": "system",
            "content": "You are a Cloud FinOps expert. Return ONLY a JSON array."
        },
        {
            "role": "user",
            "content": f"""
Generate a realistic monthly bill breakdown in INR (Indian Rupees) for this project.
Ensure the services align with the tech stack: {json.dumps(profile.get('tech_stack'))}

Return EXACTLY this JSON format (Array of objects):
[
  {{ "service": "Compute (e.g., EC2/Lambda)", "cost_inr": 0, "desc": "Brief explanation" }},
  {{ "service": "Database (e.g., RDS)", "cost_inr": 0, "desc": "Brief explanation" }},
  {{ "service": "Storage (e.g., S3)", "cost_inr": 0, "desc": "Brief explanation" }},
  {{ "service": "Monitoring/Logging", "cost_inr": 0, "desc": "Brief explanation" }},
  {{ "service": "Networking/Data Transfer", "cost_inr": 0, "desc": "Brief explanation" }}
]

Project Details:
{json.dumps(profile)}
"""
        }
    ]

    return clean_json_response(query_llm(messages))

def generate_cost_analysis(profile, billing):
    if not profile or not billing:
        print("⚠️ Skipping cost analysis (Missing data)")
        return None
    print("⏳ Generating cost optimization report...")
    messages = [
        {
            "role": "system",
            "content": "You are a Cloud Auditor. Return ONLY valid JSON."
        },
        {
            "role": "user",
            "content": f"""
Analyze the costs against the budget. Calculate totals.
If the budget_inr_per_month in the profile is 0 or null, assume a default budget of 10,000 INR for calculation purposes.
Return EXACTLY this JSON format:
{{
  "total_cost_inr": 0,
  "budget_inr": 0,
  "variance_inr": 0,
  "over_budget": boolean,
  "recommendations": [
    {{
      "title": "Optimization Title",
      "current_cost": 0,
      "potential_savings": 0,
      "cloud_providers": ["AWS", "Azure", "GCP"],
      "action_plan": "Short specific advice"
    }}
  ]
}}
Profile Data:
{json.dumps(profile)}
Billing Data:
{json.dumps(billing)}
"""
        }
    ]

    return clean_json_response(query_llm(messages))

if __name__ == "__main__":
    user_input = "I want to build a simple e-commerce website selling handmade shoes using Python and React."
    project_profile = generate_project_profile(user_input)
    if project_profile:
        print("\n✅ Profile Generated:")
        print(json.dumps(project_profile, indent=2))
        billing_data = generate_mock_billing(project_profile)
        
        if billing_data:
            print("\n✅ Billing Generated:")
            print(json.dumps(billing_data, indent=2))
            analysis = generate_cost_analysis(project_profile, billing_data)
            if analysis:
                print("\n✅ Analysis Generated:")
                print(json.dumps(analysis, indent=2))
            else:
                print("❌ Failed to generate analysis.")
        else:
            print("❌ Failed to generate billing.")
    else:
        print("❌ Failed to generate project profile.")
