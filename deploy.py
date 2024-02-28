import subprocess
import requests

from settings import SETTINGS

DATABRICKS_DOMAIN = SETTINGS["DATABRICKS_DOMAIN"]

# Step 1: Upload the bash script to DBFS
def upload_init_script():
    subprocess.run(["databricks", "fs", "cp", "./install_libraries.sh", "dbfs:/databricks/init-scripts/install_libraries.sh"], check=True)
    print("Init script uploaded to DBFS.")

# Step 2: Create a compute policy
def create_compute_policy():
    policy_url = f"{DATABRICKS_DOMAIN}/api/2.0/policies/clusters/create"
    policy_data = {
        "name": "medium-company-policy",
        "definition": {
            "spark_version": {"type": "fixed", "value": "7.3.x-scala2.12"},
            "node_type_id": {"type": "fixed", "value": "Standard_D3_v2"},
            "autotermination_minutes": {"type": "fixed", "value": 120},
            "init_scripts": [{"dbfs": {"destination": "dbfs:/databricks/init-scripts/install_libraries.sh"}}],
            "custom_tags": {"type": "fixed", "value": {"Project": "MediumCompanySetup"}},
        }
    }
    response = requests.post(policy_url, headers=HEADERS, json=policy_data)
    if response.status_code == 200:
        print("Compute policy created successfully.")
    else:
        print(f"Failed to create compute policy. Status Code: {response.status_code}")

if __name__ == "__main__":
    upload_init_script()
    create_compute_policy()