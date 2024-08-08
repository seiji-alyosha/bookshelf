import requests

#to get general information from the book via isbn number, including the works key. This is needed to get a description.
def get_book_info(isbn):
    try:
        response = requests.get(f'https://openlibrary.org/isbn/{isbn}.json')
        response.raise_for_status()
        book_response = response.json()
        return book_response
    
    except requests.exceptions.RequestException as err:
        print(f'Request error occurred: {err}')
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except ValueError as json_error:
        print(f'Could not decode the json response from open library: {json_error}')

    #This is a general error message for instances that the above exceptions could not handle.
    return 'We could not load the book data.'
        

#to get the book description from the works response. works key is provided by the isbn response above.
def get_book_description(works_key):
    try:
        response = requests.get(f"https://openlibrary.org{works_key}.json")
        works_response = response.json()
        description = works_response.get('description','This ISBN does not provide a book description :()')

        if isinstance(description, dict):
            return description
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ValueError as json_error:
        print(f'Could not decode the json response from open library: {json_error}')

    return 'We could not load information about the book based on the works_key.'