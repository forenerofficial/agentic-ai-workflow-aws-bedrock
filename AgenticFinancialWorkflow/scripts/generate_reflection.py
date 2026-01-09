import boto3
import json
import os
import re

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

def generate_reflection():
    try:
        print("Loading all outputs for reflection...")
        
        # DEBUG: Check each file first
        files_to_check = [
            'outputs/plan.json',
            'outputs/categorized.json', 
            'outputs/kpis.json',
            'outputs/summary.txt'
        ]
        
        for file_path in files_to_check:
            if not os.path.exists(file_path):
                print(f"Missing: {file_path}")
                return None
                
            size = os.path.getsize(file_path)
            print(f"Found: {file_path} ({size} bytes)")
            
            # Quick peek at content
            with open(file_path, 'r') as f:
                first_line = f.readline().strip()
                print(f"   First line: '{first_line[:50]}...'")
        
        # Load plan.json with extraction
        with open('outputs/plan.json', 'r') as f:
            plan_content = f.read().strip()
            
        if not plan_content:
            print("plan.json is EMPTY!")
            # Create a simple fallback plan
            plan_data = {"plan_steps": ["Categorize", "Calculate KPIs", "Summarize", "Reflect"]}
            print("⚠Using fallback plan data")
        else:
            # Extract JSON from possible text wrapper
            json_match = re.search(r'\{.*\}', plan_content, re.DOTALL)
            if json_match:
                plan_data = json.loads(json_match.group())
                print("Extracted JSON from plan.json")
            else:
                print("Could not find JSON in plan.json")
                return None
        
        # Load other files
        with open('outputs/categorized.json', 'r') as f:
            cat_content = f.read()
            json_match = re.search(r'\{.*\}', cat_content, re.DOTALL)
            if json_match:
                categorized_data = json.loads(json_match.group())
            else:
                categorized_data = json.loads(cat_content)
        
        with open('outputs/kpis.json', 'r') as f:
            kpi_content = f.read()
            json_match = re.search(r'\{.*\}', kpi_content, re.DOTALL)
            if json_match:
                kpi_data = json.loads(json_match.group())
            else:
                kpi_data = json.loads(kpi_content)
        
        with open('outputs/summary.txt', 'r') as f:
            summary_text = f.read().strip()
        
        print(f"Loaded: {len(categorized_data.get('categorized', []))} transactions")
        
        # Create the reflection prompt (EXACT from PDF)
        prompt = f"""Review all your outputs. Identify at least two possible categorization or computation errors. Suggest improvements or better rules for next time.

All Outputs:

1. PLAN:
{json.dumps(plan_data, indent=2)}

2. CATEGORIZED TRANSACTIONS (Sample):
{json.dumps(categorized_data.get('categorized', [])[:3], indent=2)}

3. FINANCIAL KPIs:
{json.dumps(kpi_data, indent=2)}

4. MONTHLY SUMMARY:
{summary_text}"""

        print("Calling AWS Bedrock for self-reflection...")
        
        # Call Bedrock
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}]
            })
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        reflection_text = response_body['content'][0]['text'].strip()
        
        # Extract JSON if needed
        json_match = re.search(r'\{.*\}', reflection_text, re.DOTALL)
        if json_match:
            reflection_text = json_match.group()
        
        # Ensure outputs directory exists
        os.makedirs('outputs', exist_ok=True)
        
        # Save to file
        with open('outputs/reflection.txt', 'w') as f:
            f.write(reflection_text)
        
        print("reflection.txt generated successfully!")
        print(f"Output saved to: outputs/reflection.txt")
        
        print("\nSelf-Reflection:")
        print("-" * 50)
        print(reflection_text[:500] + "..." if len(reflection_text) > 500 else reflection_text)
        print("-" * 50)
        
        return reflection_text
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    generate_reflection()
