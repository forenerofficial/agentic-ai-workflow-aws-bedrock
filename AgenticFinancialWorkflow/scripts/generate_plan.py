import boto3
import json
import os

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

# Plan prompt
plan_prompt = """You are a financial analysis agent. Given transaction data (date, merchant, amount, description), outline a clear 5-step plan to analyze this month's financial activity. Output your plan in JSON format."""

def generate_plan():
    try:
        # Call Bedrock (using claude)
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": plan_prompt}]
            })
        )

        # Parse response
        response_body = json.loads(response['body'].read())
        plan_text = response_body['content'][0]['text']

        os.makedirs('outputs', exist_ok=True)
        with open('outputs/plan.json', 'w') as f:
            f.write(plan_text)

        print("plan.json created")
        print(f"Output:\n{plan_text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_plan()