import boto3
import json
import os
import pandas as pd

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

def categorize_transactions():
    try:
        # Read CSV file
        df = pd.read_csv('data/transactions.csv')

        # Convert to list of dictionaries
        transactions = df.to_dict('records')

        print(f"Loaded {len(transactions)} transactions")

        # Create the categorization prompt
        prompt = f"""Categorize each transaction into: Shopping, Dining, Utilities, Income, or Other. Return a valid JSON structure following: {{ "categorized\": [ {{ \"date\": \"\", \"merchant\": \"\", \"amount\": 0, \"category\": \"\" }} ] }}.

        Transactions:
{       json.dumps(transactions, indent=2)}"""

        print("Calling AWS Bedrock for categories...")

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

        try:
            result_data = json.loads(result_text)
        except json.JSONDecodeError:
            print("Response not valid JSON, trying to extract JSON...")
            # Try to extract JSON from text
            import re
            json_match = re.search(r'\{.*}', result_text, re.DOTALL)
            if json_match:
                result_data = json.loads(json_match.group())
            else:
                raise ValueError("Could not extract JSON from response")

        # Ensure outputs directory exists
        os.makedirs('outputs', exist_ok=True)

        # Save to file
        with open('outputs/categorized.json', 'w') as f:
            json.dump(result_data, f, indent=2)

        print("categorized.json generated successfully!")
        print(f"Output saved to: outputs/categorized.json")

        # Show preview
        print("\nPreview of categorized transactions:")
        print("-" * 50)
        for i, item in enumerate(result_data['categorized'][:3], 1):
            print(f"{i}. {item['merchant']}: ${item['amount']} → {item['category']}")
        if len(result_data['categorized']) > 3:
            print(f"... and {len(result_data['categorized']) - 3} more")
        print("-" * 50)

        return result_data

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    categorize_transactions()