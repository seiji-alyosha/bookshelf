"""

NOTE: THIS IS NOT USED IN CURRENT VERSION OF ENNOIA.
originally used for integration with open library.

"""

import requests
from flask import (
    Blueprint, render_template, g, request
)
#not sure if this works
def get_author_name(author_key):
    try:
        author_url = f'https://openlibrary.org/{author_key}.json'
        author_response = requests.get(author_url)
        author_response.raise_for_status()

        author_data = author_response.json()
        author_name = author_data.get('name', 'Name not found')
        return author_name
    
    except requests.exceptions.RequestException as err:
        print(f'Request error occurred: {err}')
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except ValueError as json_error:
        print(f'Could not decode the json response from open library: {json_error}')
