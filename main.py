import os
import requests
from prefect import flow, task
import pandas as pd
import glob
from google.cloud import storage
from dotenv import load_dotenv
# from prefect_gcp.cloud_storage import GcsBucket

load_dotenv()
# gcp_cloud_storage_bucket_block = GcsBucket.load("gcp-auth")

list_of_links = [
    "https://cycling.data.tfl.gov.uk/usage-stats/351JourneyDataExtract02Jan2023-08Jan2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/352JourneyDataExtract09Jan2023-15Jan2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/353JourneyDataExtract16Jan2023-22Jan2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/354JourneyDataExtract23Jan2023-29Jan2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/355JourneyDataExtract30Jan2023-05Feb2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/356JourneyDataExtract06Feb2023-12Feb2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/357JourneyDataExtract13Feb2023-19Feb2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/358JourneyDataExtract20Feb2023-26Feb2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/359JourneyDataExtract27Feb2023-05Mar2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/360JourneyDataExtract06Mar2023-12Mar2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/361JourneyDataExtract13Mar2023-19Mar2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/362JourneyDataExtract20Mar2023-26Mar2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/363JourneyDataExtract27Mar2023-02Apr2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/364JourneyDataExtract03Apr2023-09Apr2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/365JourneyDataExtract10Apr2023-16Apr2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/366JourneyDataExtract17Apr2023-23Apr2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/367JourneyDataExtract24Apr2023-30Apr2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/368JourneyDataExtract01May2023-07May2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/369JourneyDataExtract08May2023-14May2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/370JourneyDataExtract15May2023-21May2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/371JourneyDataExtract22May2023-28May2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/372JourneyDataExtract29May2023-04Jun2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/373JourneyDataExtract05Jun2023-11Jun2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/374JourneyDataExtract12Jun2023-18Jun2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/375JourneyDataExtract19Jun2023-30Jun2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/376JourneyDataExtract01Jul2023-14Jul2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/377JourneyDataExtract15Jul2023-31Jul2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/378JourneyDataExtract01Aug2023-14Aug2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/378JourneyDataExtract15Aug2023-31Aug2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/379JourneyDataExtract01Sep2023-14Sep2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/380JourneyDataExtract15Sep2023-30Sep2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/381JourneyDataExtract01Oct2023-14Oct2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/382JourneyDataExtract15Oct2023-31Oct2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/383JourneyDataExtract01Nov2023-14Nov2023.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/384JourneyDataExtract15Nov2023-30Nov2023.csv"
    ]

@task
def load_data():
    """
    Function that uses our list of links to download them to a directory,
    where we then can perform transformations and load the data to our cloud storage.
    """
    output_dir = os.path.join(os.getcwd(), "data")
    print(f"Downloading files to directory: {output_dir}")

    for link in list_of_links:
        response = requests.get(link)
        if response.status_code == 200:
            file_name = os.path.basename(link)  # Extract the file name from the link
            file_path = os.path.join(output_dir, file_name)  # Construct the file path
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download: {link}")

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

@flow
def main():
    print("Starting data pipeline...")
    output_dir = load_data()
    path_pattern = os.path.join(output_dir, "*JourneyDataExtract*.csv")
    csv_files = glob.glob(path_pattern)

    for file_path in csv_files:
        transformed_data = transform_data(file_path)
        file_name = os.path.basename(file_path)
        destination_blob_name = f"uk_bike_data_{file_name}"
        upload_to_gcs(transformed_data, 'uk_bike_rentals', destination_blob_name)

    print("Data pipeline completed successfully.")

if __name__ == "__main__":
    main()
