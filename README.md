# Simple ETL: NASA API to AWS S3

## Project Overview
This project extracts astronomical data from NASA's API, specifically the Astronomy Picture of the Day (APOD) and Near-Earth Object (NEO) datasets. The extracted data is stored in an AWS S3 bucket and orchestrated using Managed Workflows for Apache Airflow (MWAA).

## Workflow Steps
1. Project Setup
Initialize the project using Poetry for dependency management.

Set up version control with Git and GitHub.

2. Pipeline Development
- Implement Python scripts to extract data from NASA's APOD and NEO APIs.
- Create utility functions for handling API requests and data processing.
- Design Airflow DAGs to automate the data extraction and loading processes.
- Define necessary variables and configurations in Airflow.

3. Secrets Management
- Create a .env file to store API keys and other environment variables.
- Store sensitive credentials in GitHub Secrets for security

4. Infrastructure Setup with AWS CDK
- Create raw and DAG S3 buckets using AWS CDK to store extracted data and DAG files.
- Deploy MWAA using AWS CDK to orchestrate the data pipeline.

5. CI/CD and Deployment
- Implement automated testing and deployment using GitHub Actions.
- Ensure pipeline reliability with unit tests and workflow monitoring.

##Key Technologies Used
- Poetry: Dependency and package management.
- Airflow (MWAA): Orchestrating ETL processes.
- AWS S3: Storage for raw and processed data.
- AWS CDK: Infrastructure as Code for resource provisioning.
- GitHub Actions: Automating deployment and testing.
- Boto3: AWS SDK for Python to interact with S3.
- NASA API: Data source for astronomical insights