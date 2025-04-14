def get_default_prompt(metadata, question=None):
    """
    Generate a default prompt for AI based on metadata and business questions.
    """
    default_questions = {
        "SCM": [
            "1. Who are our top-performing suppliers by delivery time and quality?",
            "2. What is the average procurement cycle time?",
            "3. Are we getting the best pricing compared to historical purchases?",
            "4. What is our order fulfillment rate?",
            "5. Where are delays occurring in the order-to-cash cycle?",
            "6. Which customers have the highest return or cancellation rates?",
            "7. How efficient is our transportation network?",
            "8. What are the lead times by carrier and region?",
            "9. Are shipments being delivered on time and in full?",
            "10. How accurate are our demand forecasts compared to actual sales?",
            "11. What are the most/least predictable SKUs?",
            "12. Are we overstocking or understocking high-value items?",
        ],
        "HCM": [
            "1. What is our current headcount by department/location?",
            "2. What is our turnover rate and what are the main reasons for attrition?",
            "3. How diverse is our workforce?",
            "4. What is the time-to-fill for open positions?",
            "5. Which hiring sources yield the best candidates?",
            "6. Are new hires meeting performance expectations?",
            "7. How many employees are meeting or exceeding performance goals?",
            "8. What is the adoption rate of training programs?",
            "9. Are high performers being promoted or retained?",
            "10. Is our pay structure aligned with market benchmarks?",
            "11. What is the cost per employee including benefits?",
            "12. Are there compensation disparities across departments or demographics?",
        ],
        "Finance": [
            "1. What is our current profit margin?",
            "2. Are we on track with our budget forecasts?",
            "3. What are the main contributors to revenue growth or decline?",
            "4. What is our DSO (Days Sales Outstanding) and DPO (Days Payable Outstanding)?",
            "5. Who are our largest outstanding debtors?",
            "6. Are we paying vendors on time to take advantage of discounts?",
            "7. How much cash do we have available today vs forecast?",
            "8. What are the expected inflows and outflows for this quarter?",
            "9. Where can we improve liquidity?",
            "10. What departments are exceeding their budgets?",
            "11. What are the largest cost drivers in our operations?",
            "12. How do our actual costs compare to standard costs?",
        ],
        "Inventory Management": [
            "1. What is our current inventory value by location?",
            "2. What are our fastest and slowest-moving items?",
            "3. Are we at risk of stockouts or overstocking?",
            "4. What is the order picking and packing time?",
            "5. How accurate is our inventory count vs physical count?",
            "6. How efficient is space utilization in our warehouses?",
            "7. What portion of inventory is aged over 90/180/365 days?",
            "8. What’s the write-off risk due to obsolete or expired stock?",
            "9. Are there items with zero movement for a prolonged period?",
            "10. How often are discrepancies found in cycle counts?",
            "11. What’s the financial impact of inventory inaccuracies?",
            "12. Which SKUs have the most frequent adjustments?",
        ],
    }

    if not question:
        question = "\n".join(
            [
                f"\n{module}\n\n" + "\n".join(questions)
                for module, questions in default_questions.items()
            ]
        )

    prompt = f"""
You are a data modeling expert and subject Matter experts for all modules provided here. I will provide you with metadata for tables in a database and Business questions.

Each table's metadata includes:
- table_name: Name of the table
- columns: A list of columns with their name and datatype
- sample_data: First 5 rows of data for reference

I will provide the business question for each Module (SCM, HCM, Finance, Inventory Management):

{question}

Using this information and Business questions, perform the following tasks:

1. Identify and List Fact Tables
   - Specify the keys and measures for each fact table.
   - Explain which business requirement each table fulfills in one point.

2. Surrogate Keys Assignment
   - Assign a surrogate key to each fact and dimension table.
   - The format should be: TableNameKey (e.g., Fact_SalesKey).
   - These surrogate keys should be auto-generated.

3. Data Modeling Relationships
   - Use the surrogate keys as foreign keys in fact tables to reference dimension tables.
   - For date columns, map them to a DateKey in a Dim_Date dimension.

4. List Dimension Tables and Their Attributes
   - Identify dimension tables and list their meaningful attributes.

5. Justification
   - Provide a brief justification for your modeling decisions, including how fact and dimension tables were identified.

6. Summary
   - Total number of fact and dimension tables created.

Input data:
metadata: {metadata}
    """

    return prompt