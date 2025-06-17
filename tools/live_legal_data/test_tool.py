import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from tools.live_legal_data.tool import legal_dataset_search

query = "termination"
response = legal_dataset_search(query)

print("🧾 Search Results:\n")
print(response)