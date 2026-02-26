# <img width="127" height="51" alt="Captura de Tela 2025-11-27 às 13 12 47" src="https://github.com/user-attachments/assets/d61c7c6d-79e0-48d3-a980-1ae2e2a8fd96" />
BEES Data Engineering - Breweries Case

## 👷 Main Architecture:

<img width="2265" height="1557" alt="png1" src="https://github.com/user-attachments/assets/ede26a3c-560e-4105-88be-643b65aea030" />

## 📊 Project Status

- Status: Active
- Maintenance: Actively maintained by Rachid Elihimas
- Dataset Size: 9,000+ breweries

## Description

The goal of this test is to assess your skills in consuming data from an API, transforming and persisting it into a data lake following the medallion architecture with three layers: raw data, curated data partitioned by location, and an analytical aggregated layer.

> [!IMPORTANT]
> The ideia is to show a high scalable ecossystem that can handle further projects and our focus will be the Docker Compose with Airflow, Postgres and Spark.__

## Overview

- A docker-compose.yml file runs Airflow, Postgres, and Spark in Docker containers.
- Python scripts reach the Breweries data source to extract, transform and load the data into a Postgres database, orchestrated through Airflow on predefined schedule.
- Grafana orchestrates the monitoring and alerts using Loki, Promtail and Prometheus.

## Stack
- Breweries Data: Open Brewery DB API to fetch data, listing breweries companies: [Open Brewery DB](https://www.openbrewerydb.org/).
- Docker: Docker Compose with other Dockerfiles to support.
- Orchestration: Airflow v3.1.3.
- Monitoring & Alerts: Grafana v10.4.2 / Promtail v2.9.8 / Loki v2.9.8 / Prometheus v2.55.0 / Statsd-exporter v0.26.1.
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
There will be found two DAGs, the "breweries_full_pipeline" which will orchestrate all the project and the "run_pipeline_tests" which will run all unit tests for each layer.
You can start the proccess manually by executing the DAGs.

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

## Detailing the Project

The app folder contains all layers (Bronze, Silver and Gold) have a similar structure following:

`main.py`

> Python file to set up which classes will be used further on the service file, for each layer.

`service.py`

> Python file to set up each step the code will process, for each layer.

`repository.py`

> Python file to run each step defined on the service file using the core settings, for each layer.

`schemas.py`

> Python file to retain the correct schema for data validation and quality, for each layer. 

The core folder, within app folder,  has all setting and other reusable code for the project run:

`config.py`

> Python file to set up variables.

`database.py`

> Python file to set the Postgres database connection.

`exceptions.py`

> Python file to set up the exceptions for error handling.

`logging.py`

> Python file to set up the logging properties.

`spark_manager.py`

> Python file to set up Spark functions to be reusable and clean code.

The dags folder contains all DAGs usend on the project

`breweries_pipelne.py`

> Python file which contain the DAG for running the project pipeline.

`test_dag.py`

> Python file which contain the DAG for running the unit tests.

The db folder contains a SQL file that is used during the initialization of the project to set up the tables.

The monitoring folder contains all yml/yaml files that is used during the initialization of the project to set up the monitoring and alerts properties.

The tests folder contains all python files related to the unit tests.

### Pipeline Steps

#### bronze

- Connects to the data source, extracting from the API all available registries for the Breweries.
- Writes the extracted data into the bronze_breweries_simulation for retention and recovery.
- After truncates the bronze_breweries table to avoid duplicated data, insert the new data from the bronze_breweries_simulation and truncates it at the end.

#### silver

- Truncate the silver_breweries table
- Drop columns - "id", "address_1", "address_2", "address_3", "postal_code", "phone", "state_province", "website_url", "longitude", "latitude", "street", "created_at", "updated_at" and "batch_id"
- Trim column "country"
- Capitalize columns "brewwery_type" and "country"
- Drop duplicates
- Writes the parquet file partitioned by "country", "state" and "city"
- Writes the data into silver_breweries table for retention and recovery

#### gold 

- Truncate the gold_breweries table
- Read data from the silver_breweries table
- Create the view grouping by "country", "state", "city" and "brewery_type" counting the total name as "brewery_count"
- Writes the data into gold_breweries table for retention and recovery

## Overall Solution

My primary objective is to deliver a robust, scalable, and nearly zero-touch Data Engineering solution. The entire architecture and implementation strategy were designed to ensure that once deployed, the system operates with minimal human intervention while maintaining reliability, observability, and a high standard of data quality.

To achieve this, the solution is packaged entirely using Docker Compose and custom Dockerfiles. Building on the standard Airflow Docker Compose structure, I extended the environment with two additional Dockerfiles:

- A customized Airflow Dockerfile to install additional Python dependencies required by the orchestration and data processing tasks.

- A dedicated Spark Dockerfile to enable PySpark execution with full compatibility and dependency isolation.

This modular Docker approach guarantees reproducible deployments, eliminates environment drift, and ensures that both Airflow and PySpark run consistently across different environments.

Also, using the Docker Compose to ensure that the monitoring tools will be up and running united with all other systems.

## Pipeline Behavior and Execution Strategy

The ETL/ELT processes are intentionally simple, transparent, and optimized for performance, using a combination of Python and PySpark where scalability is beneficial.

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

This project includes a production-style observability stack designed to provide full visibility over Airflow DAG executions, task behavior, logs, and operational health.

The monitoring architecture is fully containerized and automatically provisioned via Docker Compose.

### Observability Architecture

The stack integrates the following components:

- Airflow – Workflow orchestration
- StatsD (Airflow native) – Internal metric emission
- statsd-exporter – Converts StatsD metrics into Prometheus format
- Prometheus – Metrics collection and storage
- Promtail – Log shipping from containers
- Loki – Log aggregation and indexing
- Grafana – Dashboards and alerting engine

### Metrics

Airflow → StatsD → statsd-exporter → Prometheus → Grafana

Airflow is configured to emit internal metrics via StatsD, including:

1. Task success/failure counters
2. Task execution duration
3. DAG-level execution behavior
4. Scheduler heartbeat and health
5. Operator execution metrics

The statsd-exporter converts these into Prometheus-compatible metrics such as:

> airflow_task_success_total

> airflow_task_failure_total

> airflow_task_duration_seconds

> airflow_scheduler_heartbeat_total

Prometheus scrapes these metrics and makes them available to Grafana for visualization and alerting.

### Log Forwarding

Docker Containers → Promtail → Loki → Grafana

Promtail collects logs directly from running containers (including all Airflow services).

This enables:

- Full-text search across logs

- Filtering by container, DAG, task, and execution window

- Fast root-cause investigation

- Correlation between metrics and log spikes

Example use cases:

- Identify all ERROR logs from Airflow in the last 5 minutes

- Inspect task-level failures alongside performance degradation

- Drill down into specific container logs during incidents

### Dashboards

Dashboards set to include:

- Task failures (last 1h)

- Failures by DAG (last 6h)

- Task throughput

- Real-time Airflow error logs

This ensures the environment is immediately observable without manual configuration.

## Alerting

Alerts set to include:

- Task Failure Alert: Triggers if any Airflow task fails within the last 5 minutes.

- Log Error Alert: Triggers if ERROR appears in Airflow logs within the last 5 minutes.

Alerts are evaluated directly in Grafana using Prometheus and Loki as data sources.

Notification routing is defined through provisioned contact points and policies.

This allows:

Immediate failure detection

Early detection of silent issues (via logs)

Automatic escalation via email or webhook (configurable)

## Conclusion

The final result is a self-contained, zero-touch data engineering product that is:

- Easy to deploy

- Simple to maintain

- Fully observable

- Fast and scalable

- Built with data governance in mind

- Aligned with industry best practices for modern data platforms

Its design ensures reliability, extensibility, and maintainability without requiring day-to-day engineer intervention.

