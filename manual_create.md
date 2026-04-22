# Objective

Manually create all resources for Phase 1 with azure web interface.

## 🔹 Step 1 — Create HTTP Linked Service

1. Go to **Manage (⚙️)**
2. Click **Linked services**
3. Click **+ New**
4. Search and select **HTTP**
5. Click **Continue**

### Configure:

* **Name**: `ls_http_api`
* **Base URL**: `https://api.your-source.com`
* **Authentication**: Anonymous (or API Key / Bearer if required)

6. Click **Test connection**
7. Click **Create**

## 🔹 Step 2 — Create Dataset for source

1. Go to **Author (✏️)** > **Datasets** > **+ New**
2. Search and select **HTTP**
* **Linked service**: select your HTTP linked service
* **Request method**: GET

## 🔹 Step 3 — Create Dataset for sink

1. Go to **Author (✏️)** > **Datasets** > **+ New**
2. Select **Azure Data Lake Storage Gen2**
3. Select format: **JSON**
4. Set properties:
* **Name**: `sink_json_adls2`
* **Linked service**:  `DataLakeStorageGen2Sink`
* **Azure subscription**: select your Azure subscription
* **Storage account name**: select your storage account name
* **Parameters**:
    > ```
    > p_container
    > p_folder
    > p_file
    > ```
3. **Set properties**
    * **Name**: Sink
    * **Linked service**: `DataLakeStorageGen2Sink`
4. Add parameters to the pipeline directly to the dataset `file path`
* Create
    > ```
    > p_container: one
    > p_folder: raw
    > p_file: file.json
    > ```
* Apply:
    > ```
    > p_container: @dataset().p_container
    > p_folder: @dataset().p_folder
    > p_file: @dataset().p_file
    > ```

## 🔹 Step 2 — Source Configuration (one to api)

1. Open your **Pipeline**
2. Select the **Copy Activity**
3. Go to the **Source** tab

* **Source dataset**: `ds_api_source`
* **Request method**: `GET`
* **Pagination**: configure if API returns paged results
* **Request timeout / Retry**: adjust for reliability

## 🔹 Step 4 — Create Pipeline

1. Go to **Author (✏️)**
2. Click **+** → **Pipeline**
3. Select **Pipeline**
4. Set properties:

* **Name**: `one_pipeline`

---

## 🔹 Step 5 — Add Copy Activity

1. In the pipeline canvas, search for **Copy data**
2. Drag it into the canvas
3. General:
* **Name**: `breweries`
* **Activity state**: Activated
* **Timeout**: 00:10:00
* **Retry**: 3
* **Retry interval**: 60 (seconds)
4. Source:
* **Source dataset**: `breweries_json`
* **Request method**: `GET`
* **Request timeout**: 00:00:02
* **Max concurrent connections**: 1
5. Sink:
* **Sink dataset**: `sink_json_adls2`
* **File path**: 
    
    * p_container: one
    * p_folder:
```
@concat(
    'raw/api/openbrewery/',
    formatDateTime(
        convertTimeZone(utcNow(),'UTC','E. South America Standard Time'),
        'yyyy/MM/dd'
    )
)
```
    * p_file:
```
@concat(
    'response_',
    formatDateTime(
        convertTimeZone(utcNow(),'UTC','E. South America Standard Time'),
        'HHmmss'
    ),
    '_',
    pipeline().RunId,
    '.json'
)
``` 
    
* **Copy behavior**: Preserve hierarchy
* **Max concurrent connections**: 1
* **Block size (MB)**: 4


## 🔹 Step 6 — Validate all

## 🔹 Step 7 — Plublish all

## 🔹 Step 8 — Trigger/schedule the pipeline
1. Add Trigger > New/Edit
2. Add new trigger:
* **Name**: daily
* **Type**: Schedule
* **Start date**: 4/22/2026, 12:00:00 AM
* **Time zone**: Brasilia (UTC-3)
* **Recurrence**: Every 1 Day(s)
* **Schedule execution times**: 01:00
* **Start trigger**: Start trigger on creation (enable)

## 🔹 Step 7 — Plublish all