# Steps to automate Power BI semantic model refresh

Pre-requisites:
1. Have Fabric trial license
2. Have admin access

Steps:
1. Login to Azure client portal https://portal.azure.com/ and browse “App registrations” in the search bar and select “App registrations” from the Services highlighted in grey.
2. Register new application.
3. Generate a Client Secret by clicking on the “Certificates & Secrets” tab from the menu bar on the left under “Manage”.
4. Once the client secret is created, the value will only be exposed once and needs to be copied into Key-Vault or another appropriate password manager tool.
5. The next step would be to give appropriate API Permissions to the APP to enable accessing Power BI objects. Click on “API permissions” from the menu bar on the left under “Manage”.
6. Once opened, click on “Delegated permissions” and select the appropriate permissions to be given to the App and click “Add permissions” from the bottom. The important ones are:
![Alt text](https://github.com/hanashah-01/Semantic-Model-Refresh/blob/main/api-permissions.png)
8. Once the App is registered, the next step is to create a Security Group that will have the App Id (Service Principal) as one of the members.
9. Open Azure Portal and browse “Groups” to create a new security group. To create a security group, you will need at least “Group Creator” or higher permissions.
10. Click on “New group” to create a new security group. Select “Security” as “Group Type” and provide the appropriate group name under “Group name”. Next, click on “No members selected” from the bottom left to add Service Principal as a member. Once the App ID is selected then click on “Select” from the bottom to save the configuration.
11. Login to Power BI and navigate to “Admin portal” under Settings.
12. Select Tenant settings from the menu bar on the left and browse for “Developer settings” on the right. Then add the new security group under “Allow service principals to use Power BI APIs” and click “Apply”.
13. Once applied, go to the Workspace that needs to be accessed by the Rest API and add Service Principal as “Member"/"Contributor".
14. Add the Python script at the end of the ETL.

Where to get parameters in the script:
1. In the app's Overview tab:
- Application (client) ID = client_id
- Directory (tenant) ID = tenant_id
2. Go to Certificates & Secrets → "New client secret"
- Copy the generated value right away (it won't be shown again). This is your client_secret.

References:
1. https://prodata.ie/2023/07/25/refresh-fabric-dataset-using-python/
