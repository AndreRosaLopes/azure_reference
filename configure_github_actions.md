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
```

Take notes of output:
```
clientId : appId
clientSecret : password
tenantId : tenant
subscriptionId : <ID/SUBSCRIPTION_ID>
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

* AZURE_CLIENT_ID
* AZURE_CLIENT_SECRET
* AZURE_TENANT_ID
* AZURE_SUBSCRIPTION_ID

### 🚀 `prod`

* Add **Required reviewers**
  👉 This enables the **manual approval gate**

Add environment secrets:

* AZURE_CLIENT_ID
* AZURE_CLIENT_SECRET
* AZURE_TENANT_ID
* AZURE_SUBSCRIPTION_ID
---

## 🔹 4. Create Workflow File

Create:

```
.github/workflows/azure_CD_pipeline.yml
```

---



---

# 🔄 How This Matches Your Flow

## Trigger

```
Publish All (ADF)
   ↓
updates adf_publish
   ↓
push → triggers GitHub Actions
```

---

## CI/CD Behavior

```
adf_publish
   ↓
Deploy TEST (automatic)
   ↓
⏸️ WAIT (GitHub Environment approval)
   ↓
Deploy PROD
```
