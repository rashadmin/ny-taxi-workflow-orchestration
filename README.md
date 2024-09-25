# ny-taxi-workflow-orchestration

# Ingesting Data to Local Postgres with Airflow

This project demonstrates how to use Apache Airflow to automate the ingestion of data into a local Postgres instance.

## Steps:

1. **Set Up Airflow Folder**: 
   - Created a new folder `dags_new` for our DAGs.
   - Updated `docker-compose.yaml` to reflect the new directory.

2. **Start Airflow**:
   - Ran `docker compose up airflow-init` followed by `docker compose up` to initialize and start Airflow.
   - Accessed the Airflow webserver at `localhost:8080`.

3. **Create Data Ingestion DAG**:
   - Added a new DAG file `data_ingestion_local.py` to the `dags_new` folder.
   - Developed a script `ingest_script.py` for data ingestion logic.

4. **Install Dependencies**:
   - Updated the `Dockerfile` to install required libraries.

5. **Rebuild Airflow**:
   - Rebuilt the Airflow containers to apply changes using `docker compose up --build`.

6. **Set Environment Variables**:
   - Configured Postgres connection details as environment variables in `.env` and referenced them in `docker-compose.yaml`.

7. **Connect Docker Networks**:
   - Ensured the Postgres service was connected to the correct Docker network by linking network configurations between YAML files.

8. **Access Postgres**:
   - Connected to Postgres locally using `pgcli`:
     ```bash
     pgcli -h localhost -p 5432 -U root -d ny_taxi
     ```

9. **Testing and Monitoring**:
   - Used the Airflow UI to monitor DAG runs, view logs, and ensure the data ingestion tasks were successfully executed.

10. **Extend Workflow**:
    - Updated the ingestion logic to create monthly tables, with potential future tasks to join the data into a consolidated table each month.
