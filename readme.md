# UK Bike Rental Data Analysis
<img width="1203" alt="image" src="https://github.com/Mikaelnystroms/uk-bike-rental-analysis/assets/67004061/74a8a8d5-d0e0-4863-ade1-a1641a7afd93">
<img width="1660" alt="image" src="https://github.com/Mikaelnystroms/uk-bike-rental-analysis/assets/67004061/2b3ddc49-0ebe-4eae-98f1-80ec95ea6f9d">


## Introduction

Bike-sharing systems have increased in popularity across the UK as environmentally friendly and convenient transportation options. These systems generate data that can be analyzed to improve service efficiency and user experience. This project focuses on analyzing bike rental data from across the UK for the year 2023.

If you have issues during the setup and usage of this repo, feel free to contact me and i'll gladly help guide you through it! @mikaelnystrom on Telegram. 

## Problem Statement

This project aims to analyze UK bike rental data from 2023 to identify patterns and trends that can enhance the efficiency and user engagement of bike-sharing systems. The project will address the following key questions:

- **Demand Forecasting:** Identify peak usage times and variations in bike rental demand by time and day to optimize bike availability.
- **Geospatial Analysis:** Determine high-demand locations and popular routes to guide the strategic placement of new rental stations.

The insights derived from this analysis can potentially help urban planners and bike-sharing providers make informed decisions to improve the sustainability and functionality of their services.

## Project Overview

### Infrastructure

- **GCP services** are used during the course of this project.
- **Terraform** is used for managing aspects of the infrastructure such as creating the cloud storage bucket.

### Technologies and Architecture

#### Data Ingestion and Transformation

- **Prefect** is used for robust data workflow management, allowing for dynamic data ingestion and transformation.

#### Development Environment

- Development was conducted on a **Google Cloud Platform (GCP) Virtual Machine (VM)**. [See this really good guide for setting it up](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=15)
- [**Poetry**](https://python-poetry.org/) is used for dependency management to ensure consistency across development environments.
- A dev container is prepared for running the project using **GitHub Codespaces**. [See this guide for setting up codespaces if you prefer to develop there](https://youtu.be/XOSUt8Ih3zA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=15)

#### Continuous Integration and Deployment (CI/CD)

- **GitHub Actions** automates the CI/CD pipeline, deploying updates to a Prefect work pool on GCP.
- This setup facilitates automatic updates whenever we push new code to the repo and scheduling of the data pipeline via Prefect's deployment arguments, alternatively via the Prefect Cloud UI.

#### Data Processing and Storage

- Post-transformation, data is stored in **Google Cloud Storage**.
- A partitioned and clustered dataset is created in **Google BigQuery** for optimized query performance.

#### Visualization

- **Looker Studio** is used for visualizing and reporting on the data, helping to extract actionable insights through interactive dashboards.

## Getting Started

### Pre-requisites

- Google Cloud Platform account
- Service account information for creation of cloud storage bucket, uploading of data, and container instance deployment of Prefect flow.
- Terraform installed - [use this and subsequent clips for setting up/learning a bit about terraform](https://youtu.be/s2bOYDCKl_M&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=11)

### Steps

1. Clone the repository.
2. Use Poetry to create a virtual environment and install required packages, or use pip to install from `requirements.txt`.
3. Run `terraform init` to prepare necessary providers (Prefect and GCP).
4. Review and update the files in the `terraform_resources` directory with your own information.
5. Run `terraform apply` to create the necessary infrastructure resources.
6. Set up a Prefect workspace and work pool, and create a GCP Credentials block for authentication. If you have made a private repository for this project, you will also need to setup github credentials in Prefect so you can clone the repo when deploying.
7. Configure GitHub Actions secrets for CI/CD setup. You need to setup the secrets 'PREFECT_API_KEY', 'PREFECT_API_URL', as well as 'DOCKER_USERNAME' and 'DOCKER_PASSWORD' (if using docker hub for your deployment.) [info on how to find prefect api url and key](https://docs.prefect.io/latest/api-ref/rest-api/)
8. Push code to the 'main' branch to trigger the GitHub Actions workflow. The 'prefect.yaml' file also allows versioning of our workflow.
9. Perform a "Quick Run" of the Prefect deployment. After a while, the flow will run and pause giving you the option in the top right corner to "resume". When clicking resume, it will prompt you for a link to fetch the data from. Feel free to use one of the links in the 'listoflinks.txt'. Prefect flows can also be configured to run on schedule if you have source links that are predictable and uploads new data with a regular frequency. For this project however, we'll use a parameterized run in prefect as an example, and the option to ingest all data at once using the 'download_full_set.py' script.
10. If you would rather run the code locally, simply run the python scripts as you would with any python script. The decorators @task and @flow is what makes them prefect runs. 
11. Import the data from Google Cloud Storage to BigQuery and partition and cluster the dataset. See 'queries.txt' for partitioning and clustering of the dataset as well as making a view for more accurate map visualization.
12. Use Looker Studio to visualize the data and create interactive dashboards.

## Visualizations and Insights

To address the problem statement, the following visualizations can be created using Looker Studio:

### Demand Forecasting:

- Line charts showing the total number of bike rentals by hour of the day and day of the week to identify peak usage times.
- Heatmaps representing the intensity of bike rental demand across different time periods.

### Geospatial Analysis:

- Bar charts displaying the most popular start and end stations to identify high-demand locations.
- Maps with markers indicating the locations of rental stations, with marker size representing the popularity of each station.
- Flow maps illustrating the most common routes taken by bike renters.

Additional visualizations that can provide valuable insights include:

- Pie chart showing the distribution of bike types rented.
- Average trip duration by hour of the day and day of the week.
- Comparison of rental patterns between weekdays and weekends.

The interactive nature of Looker Studio dashboards allows for dynamic filtering and exploration of the data. For example, users can select a specific start station to see the most popular end stations and the hourly usage patterns for that particular station.

By leveraging these visualizations, urban planners and bike-sharing providers can gain a better understanding of the demand patterns and popular locations, enabling them to optimize bike availability, strategically place new rental stations, and improve overall service efficiency.

[Link to Looker Studio Dashboard](https://lookerstudio.google.com/reporting/4e845285-d288-4799-bf9a-8a951982bc9d)
