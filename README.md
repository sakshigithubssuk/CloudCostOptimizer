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

### 1. Clone the repository
```bash
git clone https://github.com/sakshigithubssuk/CloudCostOptimizer.git
cd CloudCostOptimizer
