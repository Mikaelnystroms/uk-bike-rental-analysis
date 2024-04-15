FROM prefecthq/prefect:2.16-python3.11
COPY requirements.txt /opt/prefect/UK-BIKE-USAGE_ANALYSIS/requirements.txt
RUN python -m pip install -r /opt/prefect/UK-BIKE-USAGE_ANALYSIS/requirements.txt
COPY . /opt/prefect/UK-BIKE-USAGE_ANALYSIS/
WORKDIR /opt/prefect/UK-BIKE-USAGE_ANALYSIS/