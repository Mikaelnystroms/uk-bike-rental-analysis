Bike-sharing systems have increased in popularity across the UK as environmentally friendly and convenient transportation options. These systems generate data that can be analyzed to improve service efficiency and user experience. This project focuses on analyzing bike rental data from across the UK for the year 2023.

Problem Statement
This project aims to analyze UK bike rental data from 2023 to identify patterns and trends that can enhance the efficiency and user engagement of bike-sharing systems. The project will address the following key questions:

Demand Forecasting: Identify peak usage times and variations in bike rental demand by time and day to optimize bike availability.
Geospatial Analysis: Determine high-demand locations and popular routes to guide the strategic placement of new rental stations.
The insights derived from this analysis can potentially help urban planners and bike-sharing providers make informed decisions to improve the sustainability and functionality of their services.

Project Overview: UK Bike Rental Data Analysis
Introduction
This capstone project employs a suite of modern technologies to analyze UK bike rental data from 2023, aiming to visualise the operational efficiency and user experience of bike-sharing systems.

Infrastructure
I have been using GCP services during the course of this project, and terraform for managing aspects of the infrastructure such as creating the cloud storage bucket.

Technologies and Architecture
Data Ingestion and Transformation
Prefect is used for robust data workflow management, allowing for dynamic data ingestion and transformation. I wanted to try out something that i've heard good things about but haven't explored during the zoomcamp DE-course. 

Development Environment
Development was conducted on a Google Cloud Platform (GCP) Virtual Machine (VM), utilizing Poetry for dependency management to ensure consistency across development environments. I have also prepared a dev container if you would rather run the project using github codespaces.

Continuous Integration and Deployment (CI/CD)
GitHub Actions automates the CI/CD pipeline, deploying updates to a Prefect work pool on GCP. This setup facilitates automatic updates and scheduling of the data pipeline.

Data Processing and Storage
Post-transformation, data is stored in Google Cloud Storage, then we make a partitioned and clustered dataset in Google BigQuery for optimized query performance.

Visualization
Looker Studio is used for visualizing and reporting on the data, helping to extract actionable insights through interactive dashboards.

This architecture ensures efficient handling, analysis, and visualization of our dataset, supporting scalable and effective data-driven decision-making.


Pre-requisites
- Google Cloud Platform account
- Service account information for creation of cloud storage bucket, uploading of data and container instance deployment of Prefect flow. You may create a service account using google cloud console, and download the json file for your service account alternatively just use the content of the json file to authenticate. For more information on service accounts and required roles for creating the resources used in this project, please refer to google's documentation https://cloud.google.com/iam/docs/service-accounts-create (for this project you will need atleast cloud run developer, storage object admin, storage bucket creator, bigquery data owner permissions)
- Terraform installed (see https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli for guidance on installation, alternatively Data Slinger has a wonderful primer on Terraform here: https://www.youtube.com/watch?v=s2bOYDCKl_M)


The 'main.py' file is configured to accept a runtime parameter (A link to UK bike data) The idea for this is to make it possible to keep updating the data when new data is uploaded to the UK government site. Accepting runtime parameters is currently only possible via the Prefect UI.

The 'download_full_set.py' is intended to take all the links for the year 2023, perform necessary transformations for further analysis and upload this data to GCS. 

My recommendation is to deploy the 'main.py' prefect flow to Prefect using github actions, making for a good learning experience in how to use terraform to set up the necessary resources, how to use prefect for ETL workflows as well as using github actions for easy CI/CD.
After you have deployed the 'main.py' workflow to Prefect, we can use the 'download_full_set.py' in order to merge the data from 2023 and perform further analysis using bigquery and Looker Studio. 

Pre-requisites
- Google Cloud Platform account
- Service account information for creation of cloud storage bucket, uploading of data and container instance deployment of Prefect flow. You may create a service account using google cloud console, and download the json file for your service account alternatively just use the content of the json file to authenticate. For more information on service accounts and required roles for creating the resources used in this project, please refer to google's documentation https://cloud.google.com/iam/docs/service-accounts-create (for this project you will need atleast cloud run developer, storage object admin, storage bucket creator, bigquery data owner permissions)
- Terraform installed (see https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli for guidance on installation, alternatively Data Slinger has a wonderful primer on Terraform here: https://www.youtube.com/watch?v=s2bOYDCKl_M)

Getting started
1. Clone this repository https://github.com/Mikaelnystroms/uk-bike-rental-analysis.git
2. Use Poetry to make a venv and install required packages (https://python-poetry.org/docs/) use 'poetry install' when you have installed poetry
3. If you don't want to use Poetry, use pip instead :) pip install -r requirements.txt
4. Run Terraform init to prepare necessary providers, then look through the files in terraform_resources directory and make sure you enter your own information where applicable (api keys and urls for prefect and desired account name in main.tf and variables.tf)
5. Run terraform apply to create the necessary infrastructure resources for the project
6. Go to https://www.prefect.io/ and login with your account. Create a workspace and under the menu "Work Pool" create a cloud run:push type work pool. Under the menu "Blocks", create a new block using Prefects' GCP Credentials block and paste your service account json into 'service account info', use that block for authentication in your recently created work pool so Prefect can create container instances and upload data to Google Cloud Storage(GCS) when running jobs.
7. Configure your github actions secrets for CI/CD setup, see '.github/workflows/deploy-prefect-flow.yaml' for what secrets you need to add in github actions, see here for more guidance on how to add secrets to github actions: https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions
8. When you push code to the 'main' branch, the github actions workflow runs, updating and deploying your prefect workflow. After github actions has deployed the workflow, go to prefect.io and perform a "Quick Run" of the deployment. After a short while the flow run will pause, and in the top right corner you will have an option to "resume" which will prompt you for input. Enter one of the links in "listoflinks.txt" and the flow will continue, transforming the data and uploading it to GCS.
9. When we have the data uploaded to GCS, go to the bigquery dataset created by Terraform (default name is 'uk_bike_rentals') From bigquery, import the data from the storage bucket 'uk_bike_rentals'.
10. To make queries less costly and more efficient, we will partition the dataset by DATE from the start_datetime column and cluster the dataset by start_station_id and end_station_id. This clustering makes sense since we would like to find out more regarding the most/least popular stations and also perform some time series visualization.


link to visualization:
https://lookerstudio.google.com/s/thD2-BJ1b-M
