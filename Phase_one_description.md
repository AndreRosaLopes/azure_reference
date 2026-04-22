# 📘 Phase 1 — Data Ingestion (API → ADLS Gen2)

**Description:**
This phase focuses on ingesting data from external APIs into Azure Data Lake Storage Gen2 in its raw, unmodified format. The process is orchestrated using Azure Data Factory, which performs HTTP requests and persists the response as-is.
The objective is to ensure reliable data collection, preserve source fidelity, and enable traceability for downstream processing.

---

## 📊 Access & Permissions Summary

| Resource                                 | Principal                              | Role / Permission                         | Purpose                                         |
| ---------------------------------------- | -------------------------------------- | ----------------------------------------- | ----------------------------------------------- |
| ADLS Gen2  | Managed Identity of Azure Data Factory | Storage Blob Data Contributor             | Read/write/delete raw data files                |
| ADLS Gen2       | Managed Identity of Azure Data Factory | ACL (rwx on folders)                      | Read/Write/Execute (Hierarchical access control is required) |
| Azure Data Factory                       | Developer / Engineer                   | Data Factory Contributor                  | Create and manage pipelines                     |
| ADLS Gen2                                | Developer / Engineer                   | Storage Blob Data Reader (or Contributor) | Validate data and troubleshoot ingestion        |

---

# Progress of work

* [Manually create resource in azure web interface](manual_create.md)
* [Manually adding github repository for ADF](to do....)