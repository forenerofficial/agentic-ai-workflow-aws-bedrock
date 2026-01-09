import boto3
import json
import os

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

def compute_kpis():
    try:
        print("Loading categorized transactions...")

        # Load categorized data
        with open('outputs/categorized.json', 'r') as f:
            categorized_data = json.load(f)

        transactions = categorized_data['categorized']
        print(f"Loaded {len(transactions)} categorized transactions")

        # Create the KPI prompt
        prompt = f"""You are a financial analysis agent. 
From the following categorized transactions, compute these financial KPIs:

1. total_spend (sum of all positive amounts)
2. total_income (sum of all negative amounts - income is negative in the data)
3. top_3_merchants (by total amount spent, excluding income)
4. average_expense_amount (average of positive amounts)

Categorized Transactions:
{json.dumps(transactions, indent=2)}

Return ONLY valid JSON in this exact format:
{{
  "total_spend": 0,
  "total_income": 0,
  "top_3_merchants": ["merchant1", "merchant2", "merchant3"],
  "average_expense_amount": 0
}}

Calculate carefully and show your work in the response before the JSON.
"""

        print("Calling AWS Bedrock for KPI calculation...")

        # Call Bedrock
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        # Parse response
        response_body = json.loads(response['body'].read())
        result_text = response_body['content'][0]['text']

        print("Raw response from Bedrock:")
        print("-" * 40)
        print(result_text)
        print("-" * 40)

        # Try to extract JSON
        import re
        json_match = re.search(r'\{.*}', result_text, re.DOTALL)
        if json_match:
            result_data = json.loads(json_match.group())
        else:
            raise ValueError("Could not extract JSON from response")

        # Ensure outputs directory exists
        os.makedirs('outputs', exist_ok=True)

        # Save to file
        with open('outputs/kpis.json', 'w') as f:
            json.dump(result_data, f, indent=2)

        print("kpis.json generated successfully!")
        print(f"Output saved to: outputs/kpis.json")

        # Show results
        print("\n KPI Results:")
        print("-" * 30)
        print(f"Total Spend: ${result_data.get('total_spend', 0):.2f}")
        print(f"Total Income: ${abs(result_data.get('total_income', 0)):.2f}")
        print(f"Top 3 Merchants: {result_data.get('top_3_merchants', [])}")
        print(f"Average Expense: ${result_data.get('average_expense_amount', 0):.2f}")
        print("-" * 30)

        return result_data

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    compute_kpis()
