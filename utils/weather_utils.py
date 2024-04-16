import tenacity
from uuid import uuid4
import os
from utils import time_, retry_

API_ENDPOINT_WEATHER = (
    "https://power.larc.nasa.gov/api/temporal/daily/point?"
    "parameters=T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,WS10M&"
    "community=RE&format=CSV"
)

# Define the base directory
BASE_DIR = "./"

# Define paths for different data types
DATA_DIR = os.path.join(BASE_DIR, "data_v2")
os.makedirs(DATA_DIR, exist_ok=True)

WEATHER_DATA_DIR = os.path.join(BASE_DIR, "weather_data")
os.makedirs(WEATHER_DATA_DIR, exist_ok=True)

LIST_OF_SUPPORTED_CROPS = [
    "Wheat",
    "Rice",
    "Maize",
    "Barley",
    "Soybeans",
    "Potatoes",
    "Tomatoes",
    "Sugarcane",
    "Cotton",
    "Coffee"
]


@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=60),
    stop=tenacity.stop_after_attempt(5),
    retry=tenacity.retry_if_exception_type(Exception),
    reraise=True,
)
def fetch_hist_weather_data(lon, lat, start_date, end_date):
    """
    Fetches weather data for maize from a NASA API given coordinates and date range.


    :param lon: The longitude of the coordinates.
    :param lat: The latitude of the coordinates.
    :param start_date: The sowing date of the maize.

    :return: A DataFrame containing the weather data.
    """

    url = f"{API_ENDPOINT_WEATHER}&longitude={lon}&latitude={lat}&start={start_date.strftime('%Y%m%d')}&end={end_date.strftime('%Y%m%d')}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Skip the initial metadata lines and read CSV data into a DataFrame
        weather_df = pd.read_csv(io.StringIO(response.text), skiprows=13)

        # Convert 'YEAR', 'MO', 'DY' to a datetime 'Date' column
        weather_df["Date"] = pd.to_datetime(
            weather_df[["YEAR", "MO", "DY"]].astype(str).agg("-".join, axis=1)
        )
        weather_df.drop(columns=["YEAR", "MO", "DY"], inplace=True)

        return weather_df

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return pd.DataFrame()


def process_hist_weather_data(weather_df, crop="wheat"):
    """
    Processes weather data for maize, calculating GDD and AGDD.

    :param weather_df: The DataFrame containing the weather data.
    :param temp_base: The base temperature for GDD calculation.

    :return A DataFrame containing the processed weather data for maize.

    :Note reference: https://ndawn.ndsu.nodak.edu/help-corn-growing-degree-days.html
    """

    # Get the temperature base for GDD calculation, based on the crop
    crops_temperature_base = {
        "Wheat": 4,  # Wheat grows at a base temperature of 4°C
        "Rice": 10,  # Rice grows at a base temperature of 10°C
        "Maize": 10,  # Maize (Corn) grows at a base temperature of 10°C
        "Barley": 4,  # Barley grows at a base temperature of 4°C
        "Soybeans": 10,  # Soybeans grow at a base temperature of 10°C
        "Potatoes": 7,  # Potatoes grow at a base temperature of 7°C
        "Tomatoes": 10,  # Tomatoes grow at a base temperature of 10°C
        "Sugarcane": 20,  # Sugarcane grows at a base temperature of 20°C
        "Cotton": 14,  # Cotton grows at a base temperature of 14°C
        "Coffee": 18,  # Coffee grows at a base temperature of 18°C
    }

    temp_base = crops_temperature_base.get(crop, 0)
    #  Check if the weather data is empty
    if weather_df.empty:
        return weather_df

    print(f"Computing GDD and AGDD for {crop}...")

    # Calculate daily GDD, ensuring negative values are set to zero
    weather_df["GDD"] = (
        (weather_df["T2M_MAX"] + weather_df["T2M_MIN"]) / 2 - temp_base
    ).clip(lower=0)

    # Calculate AGDD
    weather_df["AGDD"] = weather_df["GDD"].cumsum()

    # Calculate Accumulated Precipitation
    weather_df["APRECTOTCORR"] = weather_df["PRECTOTCORR"].cumsum()

    # Format 'Date' column for consistency
    weather_df["Date"] = weather_df["Date"].dt.strftime("%Y-%m-%d")

    print(f"Computed GDD and AGDD for {crop}")

    # save the weather data to WEATHER_DATA_DIR as excel file, with a uuid as the filename
    uuid = str(uuid4())

    # create WEATHER_DATA_DIR if it does not exist
    os.makedirs(WEATHER_DATA_DIR, exist_ok=True)

    # save the weather data to WEATHER_DATA_DIR as excel file, with a uuid as the filename
    print(f"Saving weather data to {WEATHER_DATA_DIR} as {crop}_weather_data_{uuid}.xlsx")
    weather_df.to_excel(os.path.join(WEATHER_DATA_DIR, f"{crop}_weather_data_{uuid}.xlsx"), index=False)
    print(f"Saved weather data to {WEATHER_DATA_DIR} as {crop}_weather_data_{uuid}.xlsx")

    # return the weather data, the path to the saved file
    return weather_df, os.path.join(WEATHER_DATA_DIR, f"{crop}_weather_data_{uuid}.xlsx")


@time_
@retry_
def download_hist_weather_data(lon, lat, start_date, end_date, crop="wheat"):
    """
    Downloads and processes weather data specifically for maize.

    :param lon: The longitude of the coordinates.
    :param lat: The latitude of the coordinates.
    :param start_date: The sowing date of the maize.
    :param end_date: The end date of the weather data.

    :return: A DataFrame containing the processed weather data for maize.
    """
    # Fetch weather data
    weather_df = fetch_weather_data(lon, lat, start_date, end_date)

    # Process fetched weather data for maize
    processed_df, saved_data_path = process_hist_weather_data(weather_df, crop="wheat")

    return processed_df, saved_data_path



