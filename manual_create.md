# Objective

Manually create all resources for Phase 1 with azure web interface.



# Creating basic resources for each environment

Let's take the Directory ID for build a unique identifier for resources. Example:

263ad61f-3f87-41a2-92f8-1970496f74b3 => 1970496f74b3



## 🔹 Step 1 — Create a resource group

1. Go to **Resource groups** > **+ Create**
* subsciption: `Azure subscription 1`
* Resource group name: `dev-rg-one`
* Region: `(US) East US 2`
2. Click **Review + create** >  **Create** 

## 🔹 Step 2 — Storage account
1. Go to **Storage accounts** > **+ Create**
* subsciption: `Azure subscription 1`
* Resource group name: `dev-rg-one`
* Storage account name: `devac1970496f74b3`
* Region: `(US) East US 2`
* Preferred storage type: Azure Blob Storage or Azure Data Lake Storage Gen2 
* Performance: Standard
* Redundancy: Locally-redundant storage (LRS)
2. Click **Next**
* Enable hierarchical namespace: `enable`
3. Click **Review + create** >  **Create** 

## 🔹 Step 3 — Data Lake Storage Gen2

1. Go to **Storage accounts**
2. In left side menu: Data storage > Containers > + Add container
* Name: one
3. Create
4. Click on created container name: one
5. Click on + Add Directory
* Name: raw
6. Create

Repeat the process for the following directories:
* Name: curated
* Name: gold


## 🔹 Step 4 — Data Factory

1. Go to **Data factories** > **+ Create**
* subsciption: `Azure subscription 1`
* Resource group: `dev-rg-one`
* Name: `dev-adf-one-1970496f74b3`
* Region: `(US) East US 2`
* Version: `V2`
2. Click **Review + create** >  **Create** 

Repeat the Step 1 to 2 for each environment:
* `test`
* `prod`


# Setting up permissions and access to resources

We are going to set up the permissions and access to resources for each environment according to the following table (the users and groups must be created in azure AD): 

| Resource           | resource-env | Principal                              | principal-env | Role / Permission             | Purpose                          |
| ------------------ | ------------ | -------------------------------------- | ------------- | ----------------------------- | -------------------------------- |
| Storage Account    | dev          | Managed Identity of Azure Data Factory | dev           | Storage Blob Data Contributor | Read/write/delete raw data files |
| root Container     | dev          | Managed Identity of Azure Data Factory | dev           | ACL (rwx)                     | Full pipeline access             |
| Azure Data Factory | dev          | Developer / Engineer                   | -           | Data Factory Contributor      | Create and modify pipelines      |
| ADLS Gen2          | dev          | Developer / Engineer                   | -           | Storage Blob Data Contributor | Test and validate data           |
| Storage Account    | test         | Managed Identity of Azure Data Factory | test          | Storage Blob Data Contributor | Pipeline execution               |
| root Container     | test         | Managed Identity of Azure Data Factory | test          | ACL (r-x / restricted rwx)    | Controlled execution             |
| Azure Data Factory | test         | Developer / Engineer                   | -          | Data Factory Operator         | Execute and monitor pipelines    |
| ADLS Gen2          | test         | Developer / Engineer                   | -          | Storage Blob Data Reader      | Validate data (read-only)        |
| Storage Account    | prod         | Managed Identity of Azure Data Factory | prod          | Storage Blob Data Contributor | Write via pipelines only         |
| root Container     | prod         | Managed Identity of Azure Data Factory | prod          | ACL (rwx – MI only)           | Automated execution              |
| Azure Data Factory | prod         | Developer / Engineer                   | -          | Data Factory Reader           | Monitoring only                  |
| Azure Data Factory | prod         | DataOps Operator                       | -          | Data Factory Operator         | Trigger and operate pipelines    |
| Azure Data Factory | prod         | CI/CD pipeline(Service Principal)      | prod          | Data Factory Contributor      | Automated deployments            |
| ADLS Gen2          | prod         | Developer / Engineer                   | -          | Storage Blob Data Reader      | Audit and troubleshooting        |
| ADLS Gen2          | prod         | DataOps Operator                       | -          | Storage Blob Data Reader      | Operational support              |
| ADLS Gen2          | prod         | BI Tools (e.g., Power BI)              | prod          | Storage Blob Data Reader      | Data consumption                 |

## 🔹 Step 1 — Set Storage Blob Data Contributor Role for the Managed Identity of ADF

1. Go to **Storage accounts**
2. Click on your storage account
3. In left side menu: **Access control (IAM)**
4. Click on **+ Add role assignment**
5. Select **Storage Blob Data Contributor** role
6. Click **Next**
7. Assign access to: **Managed identity**
8. Click **Select members**
9. Search for the Managed Identity you created in Step 1
10. Click **Select**
11. Click **Review + assign**


## 🔹 Step 2 — Set root Container ACL (r-x / restricted rwx) for the Managed Identity of ADF

1. Go to **Storage accounts**
2. Click on your storage account
3. In left side menu: **Data storage > Containers**
4. Click on your container
5. Click on **Settings** > **Manage ACL**
6. For both, **Access permissions** and **Default permissions**:
7. Click on **+ Add principal**
8. Search for `dev` > Select
9. Mark down: Read / Write / Execute
10. Click **Save**
