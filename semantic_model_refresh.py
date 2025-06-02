import requests
 
# Service Principal Information (global Parameters)
# client_id = dbutils.secrets.get(scope=, key=)
# client_secret = dbutils.secrets.get(scope=, key=)
client_id = "XX"
client_secret = "XX"
tenant_id = "XX"   # Directory (tenant) ID from Azure AD
base_url = f"https://api.powerbi.com/v1.0/myorg/"
workspace_name = "name"

# Function to get Access Token using App ID and Client Secret
def get_accessToken(client_id, client_secret, tenant_id):
    # Set the Token URL for Azure AD Endpoint
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
 
    # Data Request for Endpoint
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "resource": "https://analysis.windows.net/powerbi/api",
    }
 
    # Send POS request to obtain access token
    response = requests.post(token_url, data=data)
 
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        response.raise_for_status()

# Function to get workspace ID 
def get_pbiWorkspaceId(workspace_name, base_url, headers):
    relative_url = base_url + "groups"
     
    #Set the GET response using the relative URL
    response = requests.get(relative_url, headers=headers)
     
    if response.status_code == 200:
        data = response.json()
        for workspace in data["value"]:
            if workspace["name"] == workspace_name:
                return workspace["id"]
        return None
 
# Function to get Dataset ID 
def get_pbiDatasetId(workspace_id, base_url, headers, dataset_name = ""):
    relative_url = base_url + f"groups/{workspace_id}/datasets"
 
    #Set the GET response using the relative URL
    response = requests.get(relative_url, headers=headers)
     
    if response.status_code == 200:
        dataset_id = []
        data = response.json()
        for dataset in data["value"]:
            if dataset_name != "":
                if dataset["name"] == dataset_name and dataset["isRefreshable"] == True:
                    dataset_id.append(dataset["id"])
                return dataset_id
            if dataset["isRefreshable"] == True:
                dataset_id.append(dataset["id"])
        return dataset_id
    
# Function to Refresh PBI Dataset
def invoke_pbiRefreshDataset(workspace_id, dataset_id, base_url, headers):
    for id in dataset_id:
        relative_url = base_url + f"groups/{workspace_id}/datasets/{id}/refreshes"
        response = requests.post(relative_url, headers=headers)
 
        if response.status_code == 202:
            print(f"Dataset {id} refresh has been triggered successfully.")
        else:
            print(f"Failed to trigger dataset {id} refresh.")
            print("Response status code:", response.status_code)
            print("Response content:", response.json())

# Function to get PBI Dataset Refresh Status
def get_pbiRefreshStatus(workspace_id, dataset_id, base_url, headers):
    relative_url = base_url + f"groups/{workspace_id}/datasets/{dataset_id}/refreshes"
    response = requests.get(relative_url, headers=headers)
 
    refresh_status = response.json()
    latest_refresh = refresh_status["value"][0]
    status = latest_refresh["status"]
    print(status)

access_token = get_accessToken(client_id, client_secret, tenant_id)
headers = {"Authorization": f"Bearer {access_token}"}
 
# Get Workspace ID
workspace_id = get_pbiWorkspaceId(workspace_name, base_url,headers)
dataset_id = get_pbiDatasetId(workspace_id, base_url, headers)
 
# Invoke Refresh
invoke_pbiRefreshDataset(workspace_id, dataset_id, base_url, headers)
 
# Get Refresh Status
get_pbiRefreshStatus(workspace_id, dataset_id[0], base_url, headers)
