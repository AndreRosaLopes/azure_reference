# 🚀 CD Setup with GitHub Actions

## Step 1 — Service Principal (SP)

First thing is to create a Service Principal (SP) and assign the role of contributor to the resource group where the ADF is located.

### Check users and sp

List all users in the tenant:
```bash
az ad user list --output table
az ad sp list --output table

```

Check account:
```bash
az account list --output table
az account show
```

Create a service principal:
```bash
az ad sp create-for-rbac \
  --name "github-adf-deploy" \
  --role contributor \
  --scopes /subscriptions/<ID/SUBSCRIPTION_ID>


az ad sp create-for-rbac --name "github-actions-adf-cd" --role contributor --scopes /subscriptions/<ID/SUBSCRIPTION_ID>/resourceGroups/test-rg-one --sdk-auth -o json
```

Take notes of output:
```
clientId : appId
clientSecret : password
tenantId : tenant
subscriptionId : <ID/SUBSCRIPTION_ID>
```
If you lost the credentials, you can reset them doing the following:
```bash
# find App ID
az ad sp list --display-name "github-adf-deploy" --query "[].appId" -o tsv
# finaly reset credentials:
az ad sp credential reset --id <APP_ID>
ou 
az ad sp credential reset --id <APP_ID> -o json
```

---

## 🔹 1. Create Environments in GitHub

Go to:

```
Repo → Settings → Environments
```

Create:

### 🧪 `test`

* No approval required (optional)

Add environment secrets:

key: AZURE_CREDENTIALS
value:
```json
{
  "clientId": "<APP_ID>",
  "clientSecret": "<PASSWORD>",
  "tenantId": "<TENANT_ID>",
  "subscriptionId": "<SUBSCRIPTION_ID>"
}
```

### 🚀 `prod`

* Add **Required reviewers**
  👉 This enables the **manual approval gate**

Add environment secrets:

key: AZURE_CREDENTIALS
value:
```json
{
  "clientId": "<APP_ID>",
  "clientSecret": "<PASSWORD>",
  "tenantId": "<TENANT_ID>",
  "subscriptionId": "<SUBSCRIPTION_ID>"
}
```
---

## 🔹 4. Create Workflow File

Create:

```
.github/workflows/azure_CD_pipeline.yml
```
