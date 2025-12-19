# Cloud Cost Optimizer (AI-Powered)

This is a CLI tool I built to simulate and optimize cloud costs using Generative AI. It takes a plain English project description, estimates the architecture, generates synthetic billing data, and suggests ways to save money across AWS, Azure, and GCP.

## 📌 Project Overview
The goal of this assignment was to create a backend system that uses an LLM to automate cost analysis. I used the Hugging Face API (specifically the `Qwen2.5-Coder` model) because it's reliable at outputting strict JSON, which was a requirement for the data processing pipeline.

### What it does:
1.  **Profile Extraction:** Reads a text description (e.g., "I need a React app with Node backend on AWS") and converts it into a structured JSON profile.
2.  **Mock Billing:** Generates realistic monthly billing data based on that profile (since I don't have live access to a cloud billing API).
3.  **Cost Analysis:** Compares the estimated costs against the user's budget.
4.  **Recommendations:** Suggests specific changes (like using Reserved Instances or Open Source alternatives) to reduce costs.

## 🛠️ Tech Stack
*   **Language:** Python 3.10+
*   **AI Service:** Hugging Face Inference API
*   **Model Used:** `Qwen/Qwen2.5-Coder-32B-Instruct` (Selected for better JSON handling)
*   **Environment:** `.env` for API security

## 🚀 How to Run Locally
 ** python main.py

###  Usage Steps
Follow the interactive menu options in sequence:

1. **Select Choice 1:**
   * Enter your project description when prompted.
   * **Note:** Ensure the description is a full sentence, not a bulleted list.
   * **Example:** "We are building a food delivery app for 10,000 users per month. Budget: ₹50,000 per month. Tech stack: Node.js backend, PostgreSQL database, object storage for images, monitoring, and basic analytics. Non-functional requirements: scalability, cost efficiency, uptime monitoring."
   * Press **Enter**.

2. **Select Choice 2 (Profile Generator):**
   * Type `2` and press **Enter** to parse the description into a JSON profile.

3. **Select Choice 3 (Mock Billing):**
   * Type `3` and press **Enter** to generate synthetic billing data.

4. **Select Choice 4 (Cost Optimization & Recommendation):**
   * Type `4` and press **Enter** to receive AI-powered cost-saving suggestions.

5. **Select Choice 5 (Exit):**
   * Type `5` to close the application.

👍 **DONE!!!**
  
### 1. Clone the repository
```bash
git clone https://github.com/sakshigithubssuk/CloudCostOptimizer.git
cd CloudCostOptimizer
