import boto3
import json
import os

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

def generate_summary():
    try:
        print("Loading financial data...")

        # Load KPI data
        with open('outputs/kpis.json', 'r') as f:
            kpi_data = json.load(f)

        # Load categorized data for context
        with open('outputs/categorized.json', 'r') as f:
            categorized_data = json.load(f)

        # Create the summary prompt (EXACT from PDF)
        prompt = f"""Write a short (<100 words) monthly financial summary using the KPIs and categories generated above.

Financial KPIs:
{json.dumps(kpi_data, indent=2)}

Categorized Transactions (first 5 for context):
{json.dumps(categorized_data['categorized'][:5], indent=2)}"""

        print("Calling AWS Bedrock for summary generation...")

        # Call Bedrock
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        # Parse response
        response_body = json.loads(response['body'].read())
        summary_text = response_body['content'][0]['text'].strip()

        # Ensures outputs directory exists
        os.makedirs('outputs', exist_ok=True)

        # Save to file
        with open('outputs/summary.txt', 'w') as f:
            f.write(summary_text)

        print("summary.txt generated successfully!")
        print(f"Output saved to: outputs/summary.txt")

        print("\nMonthly Financial Summary:")
        print("-" * 50)
        print(summary_text)
        print("-" * 50)

        return summary_text

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    generate_summary()