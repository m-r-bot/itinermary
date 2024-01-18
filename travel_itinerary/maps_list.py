import requests

def add_to_google_maps_list(api_key, list_name, places):

    # Create a new list with the provided name
    create_list_url = f"https://maps.googleapis.com/maps/api/place/userdefinedlist/create?name={list_name}&key={api_key}"
    response = requests.post(create_list_url)
    if response.status_code == 200:
        list_id = response.json().get('id', None)
        if list_id is None:
            print("Failed to create list.")
            return
        else:
            print(f"List '{list_name}' created with ID: {list_id}")
    else:
        print(f"Failed to create list: {response.json().get('error_message', 'Unknown error')}")
        return

    # Add places to the created list
    for place in places:
        name = place.get('name', '')
        address = place.get('address', '')
        add_place_url = f"https://maps.googleapis.com/maps/api/place/userdefinedlist/addplace?list_id={list_id}&place_id=&name={name}&address={address}&key={api_key}"
        response = requests.post(add_place_url)
        if response.status_code == 200:
            print(f"Place '{name}' added to list '{list_name}'")
        else:
            print(f"Failed to add place '{name}' to list '{list_name}': {response.json().get('error_message', 'Unknown error')}")

