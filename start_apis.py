import subprocess
import sys

apis = [
    "mock_apis/pos_api.py",
    "mock_apis/warehouse_api.py",
    "mock_apis/erp_api.py",
    "mock_apis/supplier_api.py",
    "mock_apis/external_api.py",
]

processes = []
for api in apis:
    p = subprocess.Popen([sys.executable, api])
    processes.append(p)
    print(f"✅ Started {api}")

print("\n🚀 All APIs running!")
print("Press Ctrl+C to stop all...")

try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    for p in processes:
        p.terminate()
    print("\n⛔ All APIs stopped!")