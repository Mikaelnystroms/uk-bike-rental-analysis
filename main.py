import os
import requests
from prefect import flow, task, pause_flow_run
import pandas as pd
import glob
from google.cloud import storage
from dotenv import load_dotenv
from requests.exceptions import RequestException


load_dotenv()


bucket_name = "YOUR_BUCKET_NAME"

@task
def load_data(link):
    output_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(f"Downloading files to directory: {output_dir}")

    try:
        print(f"Attempting to download from: {link}")
        response = requests.get(link)
        if response.status_code == 200:
            file_name = os.path.basename(link)
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download with status code {response.status_code}: {link}")
    except RequestException as e:
        print(f"Request failed for {link}: {e}")

    print("File download completed.")
    return output_dir

@task
def transform_data(file_path):
    """
    Template code for a transformer block.
    """
    print(f"Transforming data from: {file_path}")

    chunksize = 100000
    transformed_chunks = []

    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        chunk = chunk.rename(columns={
            "Number": "journey_id",
            "Start date": "start_datetime",
            "Start station number": "start_station_id",
            "Start station": "start_station_name",
            "End date": "end_datetime",
            "End station number": "end_station_id",
            "End station": "end_station_name",
            "Bike number": "bike_id",
            "Bike model": "bike_model",
            "Total duration": "duration_str",
            "Total duration (ms)": "duration_ms"
        })

        chunk["start_datetime"] = pd.to_datetime(chunk["start_datetime"])
        chunk["end_datetime"] = pd.to_datetime(chunk["end_datetime"])

        chunk["start_date"] = chunk["start_datetime"].dt.date

        chunk.dropna(inplace=True)

        chunk = chunk[(chunk['start_station_id'].apply(lambda x: str(x).isdigit())) & (chunk['end_station_id'].apply(lambda x: str(x).isdigit()))]

        chunk["start_station_name"] = chunk["start_station_name"].str.strip()
        chunk["end_station_name"] = chunk["end_station_name"].str.strip()

        chunk["start_day"] = chunk["start_datetime"].dt.day_name()
        chunk["start_hour"] = chunk["start_datetime"].dt.hour
        chunk["end_day"] = chunk["end_datetime"].dt.day_name()
        chunk["end_hour"] = chunk["end_datetime"].dt.hour

        chunk.drop_duplicates(inplace=True)

        transformed_chunks.append(chunk)

    transformed_data = pd.concat(transformed_chunks, ignore_index=True)

    print("Data transformation completed.")
    print(f"Transformed DataFrame shape: {transformed_data.shape}")
    print("DataFrame info:")
    print(transformed_data.info())
    print(transformed_data.head())

    return transformed_data

def upload_to_gcs(data, bucket_name, destination_blob_name):
    """Uploads a file to the Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    data.to_csv('transformed_data.csv', index=False)

    generation_match_precondition = 0
    blob.upload_from_filename('transformed_data.csv', if_generation_match=generation_match_precondition)

    print(f"File uploaded to GCS: gs://{bucket_name}/{destination_blob_name}")

@flow(log_prints=True)
def main():
    print("Starting data pipeline...")
    link = pause_flow_run(wait_for_input=str)
    output_dir = load_data(link)
    path_pattern = os.path.join(output_dir, "*JourneyDataExtract*.csv")
    csv_files = glob.glob(path_pattern)

    for file_path in csv_files:
        transformed_data = transform_data(file_path)
        file_name = os.path.basename(file_path)
        destination_blob_name = f"uk_bike_data_{file_name}"
        upload_to_gcs(transformed_data, bucket_name, destination_blob_name)

    print("Data pipeline completed successfully.")

if __name__ == "__main__":
    main()
