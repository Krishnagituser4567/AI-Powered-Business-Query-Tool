import unittest
from app.services.ai_engine import query_ai

class TestAIEngine(unittest.TestCase):
    def test_query_ai(self):
        # Mock inputs
        model = "text-davinci-003"
        question = "What is the top-selling product?"
        schema = "[{'table_name': 'products', 'columns': ['id', 'name', 'sales']}]
"
        
        # Mock response (replace with actual mock setup if needed)
        response = query_ai(model, question, schema)
        self.assertIsInstance(response, str)

if __name__ == "__main__":
    unittest.main()