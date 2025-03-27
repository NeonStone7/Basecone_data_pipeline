"DAG to perform ETL"
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

# Import the pipeline functions from other scripts
from pipelines.apod_pipeline import apod_pipeline
from pipelines.neo_pipeline import neo_pipeline 


# Default arguments for the DAG
default_args = {
    'owner': 'oamen',
    'email': ['oamenmodupe@gmail.com'],
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3)
}

def create_dag() -> DAG:
    """
    Creates and returns the DAG for extracting data from NASA's API.

    This DAG defines a pipeline to extract data from NASA's Astronomy Picture of the Day (APOD) 
    and Near-Earth Object (NEO) APIs and load them into S3.

    Returns:
        DAG: The defined Airflow DAG.
    """
    # Define the DAG
    with DAG(
        'etl_pipeline_nasa',
        default_args=default_args,
        description="Pipeline to extract and s3-load data from NASA's API",
        schedule_interval=timedelta(days=1),
        start_date=datetime(2025, 3, 27),
        tags=['nasa', 'etl']
    ) as dag:

        # Start task
        task_1 = EmptyOperator(task_id='start')

        # Task to run the APOD ETL pipeline
        task_2 = PythonOperator(
            task_id='APOD_ETL',
            python_callable=apod_pipeline
        )

        # Task to run the NEO ETL pipeline
        task_3 = PythonOperator(
            task_id='NEO_ETL',
            python_callable=neo_pipeline
        )

        # End task
        task_4 = EmptyOperator(task_id='end')

        # Task dependencies: task_1 must run first, then task_2 and task_3 run in parallel, and finally task_4 runs.
        task_1 >> [task_2, task_3] >> task_4

    return dag

# Create the DAG
run_dag = create_dag()
