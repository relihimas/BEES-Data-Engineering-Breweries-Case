# <img width="127" height="51" alt="Captura de Tela 2025-11-27 às 13 12 47" src="https://github.com/user-attachments/assets/d61c7c6d-79e0-48d3-a980-1ae2e2a8fd96" />
BEES Data Engineering - Breweries Case

## 👷 Main Architecture:

<img width="3280" height="1967" alt="v3" src="https://github.com/user-attachments/assets/114f61e5-e8d5-4df7-9fe1-43d2e524963b" />

## 📊 Project Status

- Status: Active
- Maintenance: Actively maintained by Rachid Elihimas
- Dataset Size: 9,000+ breweries

## Description

The goal of this test is to assess your skills in consuming data from an API, transforming and persisting it into a data lake following the medallion architecture with three layers: raw data, curated data partitioned by location, and an analytical aggregated layer.

> [!IMPORTANT]
> __As the goal of the project is to evaluate the criteria of the description above, the project will not reflect the architecture drawn interely.
> The ideia is to show a high scalable ecossystem that can handle further projects and our focus will be the Docker Compose with Airflow, Postgres and Spark.__

## Overview

- A docker-compose.yml file runs Airflow, Postgres, and Spark in Docker containers.
- Python scripts reach the Breweries data source to extract, transform and load the data into a Postgres database, orchestrated through Airflow on predefined schedule.

## Features
- Breweries Data: Open Brewery DB API to fetch data, listing breweries companies: [Open Brewery DB](https://www.openbrewerydb.org/).
- Docker: Docker Compose with other Dockerfiles to support.
- Orchestration: Airflow v3.1.3.
- Database: Postgres SQL (already provided by Airflow).
  - Tables:

Bronze Layer|Silver Layer|Gold Layer|
|---|---|---|
|bronze_breweries_simulation|silver_breweries|gold_breweries
|bronze_breweries|-|-|

- Programming Language: Python with PySpark.
- DataLake Architecture: Medallion Architecture.

## Running the Pipeline

Git clone this repository and run the following Docker commands:

```git
   git clone https://github.com/relihimas/BEES-Data-Engineering-Breweries-Case.git
```
```
   cd BEES-Data-Engineering-Breweries-Case
```
```
   docker compose build --no-cache && docker compose up -d && docker compose ps
```

The build should take around 10 minutos to set up.

Once up and running, open your preferred web browser to access Airflow and enter the URL http://localhost:8080 or change the localhost for the IP of the machine you are using.
To access the application use the credentials bellow:

user: airflow

password: airflow

You will land onto the Airflow mainpage. Go to the DAGs section.
The pipeline is orchestrated by a Master Orchestrator which will conduce the three main other Orchestrators.
You can start the proccess manually by executing the Master Orchestrator which will orchestrate the entire pipeline or running each Orchestrator following the step Bronze > Silver > Gold.

## DAG Schedules:

|Master Orchestrator|Bronze Orchestrator|Silver Orchestrator|Gold Orchestrator|
|---|---|---|---|
|@weekly|pushed by Master|pushed by Bronze|pushed by Silver|

For checking the data you can go to the Postgres CLI and 

```
   docker exec -it bees-rachid-postgres-1 psql -U airflow -d airflow
```

And SELECT * or SELECT COUNT(*) the tables informed before.

## Breweries Data:

   - Fetch Data from the [API List Breweries](https://www.openbrewerydb.org/documentation#list-breweries) 
   
   Each brewery entry contains the following fields:
   
   ```json
    {
        "id": "5128df48-79fc-4f0f-8b52-d06be54d0cec",    
        "name": "(405) Brewing Co",                     
        "brewery_type": "micro",                       
        "address_1": "1716 Topeka St",                  
        "address_2": null,                              
        "address_3": null,                             
        "city": "Norman",                               
        "state_province": "Oklahoma",                   
        "postal_code": "73069-8224",                    
        "country": "United States",                     
        "longitude": -97.46818222,                     
        "latitude": 35.25738891,                      
        "phone": "4058160490",                         
        "website_url": "http://www.405brewing.com",     
        "state": "Oklahoma",                            
        "street": "1716 Topeka St"                     
    }
   ```

## Detailing the Pipeline

`bronze_raw_extraction.py`

This script connects to the data source, extracting from the API all available registries for the Breweries.
Writes the extracted data into the bronze_breweries_simulation and replicates it to a json file for retention and recovery.

> For further expansion the json file will be sent to a S3 Bucket as shown on the architecture - /raw.

`bronze_ingestion.py`

This script truncates the bronze_breweries table to avoid duplicated data, insert the new data from the bronze_breweries_simulation and truncates it at the end.

`bronze_monitor.py`

This script creates a new line at the bronze_monitor to monitor amount of breweries extracted, source endpoint, source query, when the query has runned and a id for tracking.
This id is also updated on the bronze_breweries, for traceability.

   ```json
   {
      "total_amount_breweries": 9.038,
      "source_endpoint": "https://api.openbrewerydb.org/v1/breweries",
      "source_query": "page=47&per_page=200",
      "creation_timestamp": "20251127 14:53:52",
      "batch_id": "8b52-d06be5",
   }
   ```

`bronze_orchestrator.py`

This script orchestrates all previous bronze scripts. If any error occurs, a json containing the error will be created and stored for further review.

> For further expansion the parquet files will be sent to a S3 Bucket as shown on the architecture - /error_logs.

`silver_ingestion.py`

This script reads the data from bronze_breweries and apply the following transformations:

- Truncate the silver_breweries table
- Drop columns - "id", "address_1", "address_2", "address_3", "postal_code", "phone", "state_province", "website_url", "longitude", "latitude", "street", "created_at", "updated_at" and "batch_id"
- Trim column "country"
- Capitalize columns "brewwery_type" and "country"
- Drop duplicates
- Writes the parquet file partitioned by "country", "state" and "city"
- Writes the data into silver_breweries table for retention and recovery

> For further expansion the parquet files will be sent to a S3 Bucket as shown on the architecture - /silver.

`silver_orchestrator.py`

This script orchestrates all previous silver scripts. If any error occurs, a json containing the error will be created and stored for further review.

> For further expansion the parquet files will be sent to a S3 Bucket as shown on the architecture - /error_logs.

`gold_ingestion.py`

This script reads the data from silver_breweries and apply the following transformations:

- Truncate the gold_breweries table
- Read data from the silver_breweries table
- Create the view grouping by "country", "state", "city" and "brewery_type" counting the total name as "brewery_count"
- Writes the data into gold_breweries table for retention and recovery

`gold_orchestrator.py`

This script orchestrates all previous gold scripts. If any error occurs, a json containing the error will be created and stored for further review.

> For further expansion the parquet files will be sent to a S3 Bucket as shown on the architecture - /error_logs.

`master_orchestrator.py`

This script orchestrates all previous orchestrator scripts. If any error occurs, a json containing the error will be created and stored for further review.

> For further expansion the parquet files will be sent to a S3 Bucket as shown on the architecture - /error_logs.
> For further expansion the back up routine for the database will be sent to a S3 Bucket as shown on the architecture - /back_up_db.

`constants.py`

Dedicated module to store and centralized fixed parameters, settings, and reusable static variables.

## Overall Solution

My primary objective is to deliver a robust, scalable, and nearly zero-touch Data Engineering solution. The entire architecture and implementation strategy were designed to ensure that once deployed, the system operates with minimal human intervention while maintaining reliability, observability, and a high standard of data quality.

To achieve this, the solution is packaged entirely using Docker Compose and custom Dockerfiles. Building on the standard Airflow Docker Compose structure, I extended the environment with two additional Dockerfiles:

- A customized Airflow Dockerfile to install additional Python dependencies required by the orchestration and data processing tasks.

- A dedicated Spark Dockerfile to enable PySpark execution with full compatibility and dependency isolation.

This modular Docker approach guarantees reproducible deployments, eliminates environment drift, and ensures that both Airflow and PySpark run consistently across different environments.

## Pipeline Behavior and Execution Strategy

Once the pipeline is deployed, it runs on a weekly schedule, which is appropriate for this dataset’s refresh cadence. The ETL/ELT processes are intentionally simple, transparent, and optimized for performance, using a combination of Python and PySpark where scalability is beneficial.

With this design, the entire processing workflow completes in approximately 2 to 3 minutes, and all output data is made available through the integrated Postgres database, accessible via the Postgres CLI already provided within the Airflow Compose setup.

## Architecture — Medallion Design with Strong Engineering Principles

The data platform follows the Medallion Architecture (Bronze → Silver → Gold), and each layer was chosen with the following engineering criteria in mind:

1. Retention & Recovery

Storing immutable raw data enables complete data recovery without relying again on external APIs or systems.

2. Traceability

Maintaining raw snapshots ensures full lineage, supporting operational traceability and compliance with regulations such as LGPD.

3. Immutability

Raw data remains unaltered, enabling reliable historical comparisons and eliminating data corruption risks.

4. Easy Reprocessing

Any Bronze/Silver/Gold transformation can be re-executed without new API calls, reducing operational costs and improving resilience.

5. Source Decoupling

Once ingested, the system no longer depends on the availability or reliability of the external data source.

6. Schema Evolution

By preserving the original structure, schema adjustments in downstream layers (Bronze/Silver/Gold) become safe, controlled, and fully auditable.

7. Data Quality Framework

- Raw data enables robust quality checks across all refined layers, ensuring:

- Accuracy — data faithfully represents the source.

- Completeness — no missing required fields.

- Consistency — uniformity across sources and systems.

- Timeliness — pipeline ensures updated, fresh data weekly.

- Validity — structural and type validation is enforced.

## Reliability, Alerts, Monitoring & Observability

Any operational failure triggers automatic email alerts configured at the Airflow level. To improve observability and support proactive incident response, the architecture integrates Airflow + Grafana.

### Metrics

Airflow natively exposes internal metrics such as:

- Task duration

- Scheduler latency

- Success/failure counts

- DAG execution time

These metrics are collected and forwarded by the Grafana Agent running as an external container.

### Log Forwarding

The Grafana Agent also captures logs from:

/opt/airflow/logs

### Log ingestion allows for:

- Full-text search

- Filtering by task, DAG, execution date

- Root-cause analysis

### Error JSON Reports

All orchestrators (Bronze, Silver, Gold) include a function to generate a detailed JSON error report whenever an exception occurs. These JSON files feed directly into the monitoring layer for:

- Deep-dive troubleshooting

- Automated parsing

- Enhanced failure correlation

This enables:

- Faster root-cause identification

- Ability to trigger custom Grafana alerts

- Creation of dashboards with reliability KPIs

## Conclusion

The final result is a self-contained, zero-touch data engineering product that is:

- Easy to deploy

- Simple to maintain

- Fully observable

- Fast and scalable

- Built with data governance in mind

- Aligned with industry best practices for modern data platforms

Its design ensures reliability, extensibility, and maintainability without requiring day-to-day engineer intervention.

