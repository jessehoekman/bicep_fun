import subprocess
import requests
import json

from ad_deployment import settings, log

logger = log.get_logger(__name__)

DATABRICKS_DOMAIN = settings.SETTINGS["DATABRICKS_DOMAIN"]
TOKEN = settings.SETTINGS["TOKEN"]

HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

def create_compute_policy():    
    print("hello")
    policy_url = f"{DATABRICKS_DOMAIN}/api/2.0/policies/clusters/create"
    policy_definition = json.dumps({
        "autotermination_minutes": {"type": "fixed", "value": 120, "hidden": True},
        "node_type_id": {"type": "fixed", "value": "Standard_D3_v2", "hidden": True},
        "spark_version": {"type": "fixed", "value": "7.3.x-scala2.12", "hidden": True},
        "custom_tags": {
            "type": "fixed",
            "value": {
                "Project": "MediumCompanySetup",
                "Environment": "Production"
            },
            "hidden": False
        },
        "runtime_engine": {"type": "fixed", "value": "PHOTON", "hidden": True},
        "num_workers": {"type": "range", "minValue": 1, "maxValue": 10, "defaultValue": 2, "hidden": False},
        "libraries": [
            {"pypi": {"package": "pandas"}},
            {"pypi": {"package": "scikit-learn"}}
        ]
    })
    
    policy_data = {
        "name": "medium-company-policy",
        "description": "Policy for medium-sized company with specific configurations.",
        "definition": policy_definition
    }

    logger.info("Posting compute policy")
    try:
        response = requests.post(policy_url, headers=HEADERS, json=policy_data)
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create compute policy. Error: {e}")
        raise
    
    
    if response.status_code == 200:
        print("Compute policy created successfully. Policy ID:", response.json()['policy_id'])
    else:
        print(f"Failed to create compute policy. Status Code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    print("hello")
    create_compute_policy()
