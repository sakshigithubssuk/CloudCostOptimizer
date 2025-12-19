import os
from llm_service import generate_project_profile, generate_mock_billing, generate_cost_analysis
from utils import save_to_file, load_json_file

def main():
    while True:
        print("\n--- Cloud Cost Optimizer ---")
        print("1. Enter Project Description")
        print("2. Generate Profile")
        print("3. Generate Billing")
        print("4. Analyze Costs")
        print("5. Exit")
        
        choice = input("Choice: ")

        if choice == '1':
            desc = input("Describe your project: ")
            save_to_file("project_description.txt", desc)
        
        elif choice == '2':
            if os.path.exists("project_description.txt"):
                # ADDED encoding="utf-8" HERE for JSON PARSE
                with open("project_description.txt", "r", encoding="utf-8") as f: 
                    desc = f.read()
                    
                print("Generating profile...")
                data = generate_project_profile(desc)
                if data: save_to_file("project_profile.json", data)
                else: print("❌ AI failed to generate JSON. Try again.")
            else:
                print("❌ Run Step 1 first.")

        elif choice == '3':
            profile = load_json_file("project_profile.json")
            if profile:
                print("Generating billing...")
                data = generate_mock_billing(profile)
                if data: save_to_file("mock_billing.json", data)
                else: print("❌ AI failed.")

        elif choice == '4':
            profile = load_json_file("project_profile.json")
            billing = load_json_file("mock_billing.json")
            if profile and billing:
                print("Analyzing...")
                data = generate_cost_analysis(profile, billing)
                if data: save_to_file("cost_optimization_report.json", data)
                else: print("❌ AI failed.")
        
        elif choice == '5':
            break

if __name__ == "__main__":
    main()
