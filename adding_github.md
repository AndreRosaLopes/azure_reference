# 📘 Add GitHub Repository to Azure Data Factory

## **Description**

This step integrates Azure Data Factory with a GitHub repository to enable source control, versioning, and collaborative development.

Once configured, all changes in ADF (pipelines, datasets, linked services) will be saved as JSON files in the repository instead of being directly published to the live environment.

This enables:

* Version control (history, rollback)
* Branch-based development (dev → main)
* Safer deployments
* Team collaboration

---

## 📊 Access & Permissions Summary

| Resource           | Principal            | Role / Permission        | Purpose                     |
| ------------------ | -------------------- | ------------------------ | --------------------------- |
| Azure Data Factory | Developer / Engineer | Data Factory Contributor | Configure Git integration   |
| GitHub Repository  | Developer            | Write / Admin            | Store ADF artifacts         |
| GitHub Repo        | Azure Data Factory   | OAuth Authorization      | Allow ADF to push/pull code |

---

# 🎯 Objective

Connect Azure Data Factory to a GitHub repository using the Azure portal UI.

---

# 🔹 Step 1 — Open Git Configuration

1. Go to your **Azure Data Factory instance**
2. Click **Manage (⚙️)**
3. On **Source control**, click on **Git configuration**

---

# 🔹 Step 2 — Choose Repository Type

1. Select:

   * **GitHub**

2. Click **Continue**

---

# 🔹 Step 3 — Authenticate with GitHub

1. Click **Sign in to GitHub**
2. Authorize Azure Data Factory

👉 This creates a secure OAuth connection between ADF and GitHub.

---

# 🔹 Step 4 — Configure Repository Settings

Fill in the following:

### 🔧 Configuration

* **Repository type**: GitHub
* **GitHub account**: Your account
* **Repository name**: `your-adf-repo`
* **Collaboration branch**: `main` *(or `develop`, recommended for teams)*
* **Root folder**: `/adf` *(recommended for organization)*

---

## 💡 Recommended Structure

```
/adf
  /pipeline
  /dataset
  /linkedService
  /trigger
```

ADF will automatically generate this structure.

---

# 🔹 Step 5 — Configure Publish Branch

* **Publish branch**: `adf_publish`

👉 This branch is **automatically managed by ADF** and contains ARM templates used for deployment.

⚠️ Do NOT edit this branch manually.

---

# 🔹 Step 6 — Initialize Repository

1. Click **Apply**
2. ADF will:

* Create JSON files for all existing resources
* Push them to GitHub
* Switch ADF to **Git mode**

---

# 🔹 Step 7 — Verify Integration

1. Inside ADF:

   * You should now see branch selection (top bar)

2. Inside GitHub:

   * Navigate to your repository
   * Confirm folders like:

     * `/pipeline`
     * `/dataset`
     * `/linkedService`

---

# 🔹 Step 8 — Working with Git (Day-to-Day)

### 🔄 Development Flow

1. Create a new branch:

   ```
   feature/api-ingestion
   ```

2. Make changes in ADF

3. Click **Save** (NOT Publish)

4. Commit changes:

   * Add comment
   * Commit to branch

5. Open Pull Request in GitHub

6. Merge into `main`

7. Back in ADF:

   * Click **Publish** (deploys to live environment)

---

# ⚠️ Important Concepts

### 🟡 Save vs Publish

| Action  | Meaning                               |
| ------- | ------------------------------------- |
| Save    | Stores changes in Git                 |
| Publish | Deploys to Azure Data Factory runtime |

---

### 🟡 Live Mode vs Git Mode

| Mode      | Behavior                            |
| --------- | ----------------------------------- |
| Live Mode | Direct changes (NO version control) |
| Git Mode  | Changes go to repository            |

---

# 🚀 Best Practices

* Use `develop` branch for development (instead of `main`)
* Protect `main` with pull requests
* Never edit `adf_publish` manually
* Use meaningful commit messages:

  ```
  feat: add breweries ingestion pipeline
  fix: adjust pagination in API source
  ```

---

# 📦 Result

After this setup:

* All ADF artifacts are versioned in GitHub
* You can track changes and rollback
* Pipelines become part of a **Data Engineering CI/CD workflow**

---

Se quiser, posso te ajudar no próximo passo que normalmente vem depois disso:

👉 **CI/CD com Azure DevOps ou GitHub Actions (deploy automático do ADF)**
👉 ou estruturar um **branching strategy profissional (dev / homolog / prod)**
