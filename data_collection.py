import os
import requests

def fetch_gooey_response(input_prompt):
    """
    Sends a chatbot request to the Gooey AI API and prints the response.

    :arg input_prompt: The text prompt to send to the chatbot API.
    :type input_prompt: str
    :return: None. Prints the status code and JSON response from the API.

    Requires the 'requests' library and 'GOOEY_API_KEY' set as an environment variable.

    Raises AssertionError if the API response is not successful.

    Example:
        request_chatbot_response("Hi")

    Note:
        - Ensure 'GOOEY_API_KEY' is set in your environment variables.
        - This function is designed for the Gooey AI video-bots API endpoint.
    """

    api_key = os.getenv("GOOEY_API_KEY")
    if api_key is None:
        raise Exception(
            "GOOEY_API_KEY is not set. Please check your environment variables."
        )

    payload = {"input_prompt": input_prompt}

    try:
        response = requests.post(
            "https://api.gooey.ai/v2/video-bots/",
            headers={"Authorization": "Bearer " + api_key},
            json=payload,
        )
    except Exception as e:
        print(f"An error occurred while making the API request: {e}")
        return

    # Check if the response is OK
    if not response.ok:
        raise AssertionError(
            f"API request failed with status code {response.status_code}: {response.content}"
        )

    result = response.json()

    return result
