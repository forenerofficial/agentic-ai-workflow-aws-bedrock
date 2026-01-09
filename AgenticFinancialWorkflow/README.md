# Welcome to Tiger Tech!

# Agentic Financial Insights Workflow

## Project Overview
This project uses an AI agent workflow using AWS Bedrock to analyze financial transaction data and make insights for businesses and individual consumers.

## Team Roles
- **Prompt Engineer**: Md Hasnat - Designs and adjusts prompts for every stage
- **Data Engineer**: Md Hasnat - Manages input CSV and checks JSON outputs  
- **Financial Analyst**: Md Hasnat - Interprets outputs and writes financial summaries

##Dataset 
- **Rows**: 13 transactions 
- **Columns**: date, merchant, amount, description 
- **Type**: Personal financial data 

## Phase 1: Planning
- **Script:** `scripts/generate_plan.py`
- **Command:** `python scripts/generate_plan.py`
- **Output:** `outputs/plan.json`
- **Purpose:** Make a 5-step analysis plan following the reasoning pattern

## Phase 2: Categorization  
- **Script:** `scripts/categorize_transactions.py`
- **Command:** `python scripts/categorize_transactions.py`
- **Output:** `outputs/categorized.json`
- **Purpose:** Put transaction into: Shopping, Dining, Utilities, Income, or Other

## Phase 3: KPI Calculation
- **Script:** `scripts/compute_kpis.py`
- **Command:** `python scripts/compute_kpis.py`
- **Output:** `outputs/kpis.json`
- **Purpose:** Compute financial KPIs: spending, income, etc. 

## Phase 4: Summary & Reflection
- **Script:** `scripts/generate_summary.py`
- **Command:** `python scripts/generate_summary.py`
- **Output:** `outputs/summary.txt`
- **Purpose:** Generate a short monthly financial summary

- **Script:** `scripts/generate_reflection.py`
- **Command:** `python scripts/generate_reflection.py`
- **Output:** `outputs/reflection.txt`
- **Purpose:** Self-evaluate the analysis and suggest improvements

## Workflow Stages
1. **PLAN** - Analysis strategy and steps
2. **ACT** - Transaction categorization  
3. **OBSERVE** - KPI calculation
4. **SUMMARIZE** - Financial narrative
5. **REFLECT** - Self-evaluation and improvements

## Project Structure
/AgenticFinancialWorkflow/
├── data/
│ └── transactions.csv # Sample transaction data (13 rows)
├── scripts/
│ ├── generate_plan.py # Phase 1: Generate analysis plan
│ ├── categorize_transactions.py # Phase 2: Categorize transactions
│ ├── compute_kpis.py # Phase 3: Calculate financial KPIs
│ ├── generate_summary.py # Phase 4: Generate monthly summary
│ └── generate_reflection.py # Phase 4: Self-reflection
├── outputs/
│ ├── plan.json # Generated analysis plan
│ ├── categorized.json # Categorized transactions
│ ├── kpis.json # Financial KPIs
│ ├── summary.txt # Monthly financial summary
│ └── reflection.txt # Self-evaluation
└── README.md

## How to Run

### Prerequisites 
- Python 3.8+
- AWS Account with Bedrock access
- AWS CLI configured

### Installation
```bash
pip install boto3 pandas
aws configure 
#Enter all the info as asked 

# Navigate to project folder
cd /AgenticFinancialWorkflow/

# Run all scripts in order
python scripts/generate_plan.py
python scripts/categorize_transactions.py
python scripts/compute_kpis.py
python scripts/generate_summary.py
python scripts/generate_reflection.py

## Prompts Used (From Project Specifications)

### Plan Prompt (Step 1)
"You are a financial analysis agent. Given transaction data (date, merchant, amount, description), outline a clear 5-step plan to analyze this month's financial activity. Output your plan in JSON format."

### Categorization Prompt (Step 2)
"Categorize each transaction into: Shopping, Dining, Utilities, Income, or Other. Return a valid JSON structure following: { \"categorized\": [ { \"date\": \"\", \"merchant\": \"\", \"amount\": 0, \"category\": \"\" } ] }."

### KPI Prompt (Step 3)
"From the categorized transactions, compute: - total spend - total income - top 3 merchants - average expense amount Return valid JSON."

### Summary Prompt (Step 4)
"Write a short (<100 words) monthly financial summary using the KPIs and categories generated above."

### Reflection Prompt (Step 5)
"Review all your outputs. Identify at least two possible categorization or computation errors. Suggest improvements or better rules for next time."

### Reflection Summary
The reflection highlights two main issues: inconsistent transaction categorization and an inaccurate method for calculating average expenses. It recommends creating clearer category guidelines and using more robust statistical methods (like medians or category-based averages) to produce more meaningful financial insights.

###JSON Troubleshooting
Just need to make sure scripts are filtering for JSON outputs or just make sure prompt only returns JSON output instead of text with JSON. 



