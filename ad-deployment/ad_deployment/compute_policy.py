import requests
import json
from ad_deployment import settings, log

# Setup logger and global settings
logger = log.get_logger(__name__)
DATABRICKS_DOMAIN = settings.SETTINGS["DATABRICKS_DOMAIN"]
TOKEN = settings.SETTINGS["TOKEN"]
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}


def create_or_update_policy(name, definition):
    create_policy_url = f"{DATABRICKS_DOMAIN}/api/2.0/policies/clusters/create"
    policy_data = {
        "name": name,
        "definition": json.dumps(definition)
    }
    try:
        response = requests.post(create_policy_url, headers=HEADERS, json=policy_data)
        if response.status_code == 200:
            logger.info(f"Policy '{name}' created successfully.")
            return
        else:
            logger.warning(f"Failed to create policy '{name}'. Attempting to update existing policy. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create policy '{name}'. Error: {e}")
        return

    policies = list_policies()
    policy_id = next((policy['policy_id'] for policy in policies if policy['name'] == name), None)
    if policy_id:
        update_policy(policy_id, name, definition)
    else:
        logger.error(f"Policy '{name}' does not exist and could not be created.")

def list_policies():
    policy_url = f"{DATABRICKS_DOMAIN}/api/2.0/policies/clusters/list"
    try:
        response = requests.get(policy_url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('policies', [])
        else:
            logger.error(f"Failed to list policies. Status Code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to list policies. Error: {e}")
        return []

def update_policy(policy_id, name, definition):
    policy_url = f"{DATABRICKS_DOMAIN}/api/2.0/policies/clusters/edit"
    policy_data = {
        "policy_id": policy_id,
        "name": name,
        "definition": json.dumps(definition)
    }
    try:
        response = requests.post(policy_url, headers=HEADERS, json=policy_data)
        if response.status_code == 200:
            logger.info(f"Policy '{name}' updated successfully.")
        else:
            logger.error(f"Failed to update policy '{name}'. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to update policy '{name}'. Error: {e}")

def main():
     # General compute policy configuration
    general_compute_policy = {
        "instance_pool_id": {
            "type": "forbidden",
            "hidden": True
        },
        "spark_version": {
            "type": "regex",
            "pattern": "12\\.[0-9]+\\.x-scala.*"
        },
        "node_type_id": {
            "type": "allowlist",
            "values": [
                "Standard_L4s",
                "Standard_L8s",
                "Standard_L16s"
            ],
            "defaultValue": "Standard_L16s_v2"
        },
        "driver_node_type_id": {
            "type": "fixed",
            "value": "Standard_L16s_v2",
            "hidden": True
        },
        "autoscale.min_workers": {
            "type": "fixed",
            "value": 1,
            "hidden": True
        },
        "autoscale.max_workers": {
            "type": "range",
            "maxValue": 25,
            "defaultValue": 5
        },
        "autotermination_minutes": {
            "type": "fixed",
            "value": 30,
            "hidden": True
        },
        "custom_tags.team": {
            "type": "fixed",
            "value": "product"
        }
    }

    # Simple medium-sized policy configuration
    simple_medium_sized_policy = {
        "instance_pool_id": {
            "type": "forbidden",
            "hidden": True
        },
        "spark_conf.spark.databricks.cluster.profile": {
            "type": "forbidden",
            "hidden": True
        },
        "autoscale.min_workers": {
            "type": "fixed",
            "value": 1,
            "hidden": True
        },
        "autoscale.max_workers": {
            "type": "fixed",
            "value": 10,
            "hidden": True
        },
        "autotermination_minutes": {
            "type": "fixed",
            "value": 60,
            "hidden": True
        },
        "node_type_id": {
            "type": "fixed",
            "value": "Standard_L8s_v2",
            "hidden": True
        },
        "driver_node_type_id": {
            "type": "fixed",
            "value": "Standard_L8s_v2",
            "hidden": True
        },
        "spark_version": {
            "type": "fixed",
            "value": "auto:latest-ml",
            "hidden": True
        },
        "custom_tags.team": {
            "type": "fixed",
            "value": "product"
        }
    }

    # Job-only policy configuration
    job_only_policy = {
        "cluster_type": {
            "type": "fixed",
            "value": "job"
        },
        "dbus_per_hour": {
            "type": "range",
            "maxValue": 100
        },
        "instance_pool_id": {
            "type": "forbidden",
            "hidden": True
        },
        "num_workers": {
            "type": "range",
            "minValue": 1
        },
        "node_type_id": {
            "type": "regex",
            "pattern": "Standard_[DLS]*[1-6]{1,2}_v[2,3]"
        },
        "driver_node_type_id": {
            "type": "regex",
            "pattern": "Standard_[DLS]*[1-6]{1,2}_v[2,3]"
        },
        "spark_version": {
            "type": "unlimited",
            "defaultValue": "auto:latest-lts"
        },
        "custom_tags.team": {
            "type": "fixed",
            "value": "product"
        }
    }

    # Post policies
    create_or_update_policy("General Compute Policy", general_compute_policy)
    create_or_update_policy("Simple Medium-Sized Policy", simple_medium_sized_policy)
    create_or_update_policy("Job-Only Policy", job_only_policy)

if __name__ == "__main__":
    main()
