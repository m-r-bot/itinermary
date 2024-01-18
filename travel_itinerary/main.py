# Import necessary libraries
import pandas as pd
import folium
import googlemaps
import numpy as np
from scipy.spatial.distance import cdist
from config import API_KEY
import warnings
import os


warnings.filterwarnings('ignore')

# Load destinations from a text file
def load_destinations(file_path):
    destinations = []
    with open(file_path, 'r') as file:
        for line in file:
            destination = line.strip()
            if destination:
                destinations.append(destination)
    return destinations

def get_lat_lon(destination, api_key):
    """
    Get latitude and longitude of a destination using geocoding.
    geocode should be the cheapest here
    """
    gmaps = googlemaps.Client(key=api_key)
    try:
        result = gmaps.geocode(destination)
        lat = result[0]["geometry"]["location"]["lat"]
        lon = result[0]["geometry"]["location"]["lng"]
        return lat, lon
    except googlemaps.exceptions.ApiError as e:
        print("Error occurred while retrieving geocode: {}".format(e))
        return None, None
    except:
        return None, None

def add_lat_lon_to_dataframe(destinations, api_key):
    """
    Loop through a list of destinations, get their latitude and longitude using geocoding,
    and append the latitude and longitude to a new column in a pandas dataframe.
    """
    # Create an empty dataframe to store the results
    df = pd.DataFrame(columns=['Destination', 'Latitude', 'Longitude'])
    
    # Loop through the list of destinations and add the latitude and longitude to the dataframe
    for destination in destinations:
        lat, lon = get_lat_lon(destination, api_key)
        df = df.append({'Destination': destination, 'Latitude': lat, 'Longitude': lon}, ignore_index=True)
    df.dropna(inplace=True, axis=0, subset=["Latitude"])
    return df


# changed to dcist because using the api would cost me too much money by using the directions function
# Function to calculate distance between two points
# by breaking it up this way i have to give the api key every single time though

def generate_itinirary(destinations, api_key):

    coor_df = add_lat_lon_to_dataframe(destinations, api_key)
    coordinate_array = coor_df.iloc[:,1:].values
    coordinate_array

    # create a copy of the coordinate_array
    remaining_location = coordinate_array.copy()
    itinerary_list = []

    # choose an arbitrary starting index
    start_index = 2

    while len(remaining_location) > 0:
        start = remaining_location[start_index]

        itinerary_list.append(start)

         # delete the already visited location
        remaining_location = np.delete(remaining_location, start_index, axis=0)

        if len(remaining_location) > 0:
            distances = cdist([start], remaining_location)
            closest_index = np.argmin(distances)
            start_index = closest_index
        else:
            break

    itinerary_list = np.array(itinerary_list)

    final_itinerary = pd.DataFrame()
    for iters in range(len(itinerary_list)):
        sorted_temp_df = coor_df.query("(Latitude =={}) & (Longitude == {})".format(itinerary_list[iters][0],itinerary_list[iters][1]))
        final_itinerary = pd.concat([final_itinerary, sorted_temp_df])
    final_itinerary.reset_index(inplace=True, drop=True)

    return final_itinerary

# Get travel duration from user
def get_travel_duration():
    while True:
        try:
            travel_duration = int(input("Enter number of days for travel: "))
            if travel_duration > 0:
                break
            else:
                print("Please enter a valid number of days.")
        except ValueError:
            print("Please enter a valid number of days.")
    return travel_duration

def visualize_itinerary(travel_itinerary, filename):
    # Get center coordinates for map
    center_lat = travel_itinerary["Latitude"].mean()
    center_lon = travel_itinerary["Longitude"].mean()

    # Create map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

    # Add markers for each destination in the itinerary
    for index, row in travel_itinerary.iterrows():
        folium.Marker(location=[row["Latitude"], row["Longitude"]], popup=row["Destination"]).add_to(m)

    # Add polyline for the route
    folium.PolyLine(locations=travel_itinerary[["Latitude", "Longitude"]].values.tolist(), color="black", weight=3).add_to(m)

    # Get current working directory
    cwd = os.getcwd()

    # Save the map to a file in the current working directory
    filepath = os.path.join(cwd, filename)
    m.save(filepath)

    # Return the file path
    return filepath

def main():
    # Get input file path
    file_path = input("Enter file path for destinations: ")

    # Set up Google Maps API key
    api_key = API_KEY 

    # Get starting point
    #origin = input("At which city do you want to start:")

    # Load destinations from text file
    destinations = load_destinations(file_path)

    # Get travel duration from user
    #travel_duration = get_travel_duration()

    # Generate travel itinerary
    travel_itinerary = generate_itinirary(destinations, api_key)

    # Visualize travel itinerary on a map and save to file
    filename = "travel_map.html"
    map_filepath = visualize_itinerary(travel_itinerary, filename)

    # Print the file path
    print("Map saved to file: {}".format(map_filepath))
    
    destinations = list(travel_itinerary["Destination"].values)
    formatted_destinations = "\n".join(destinations)
    

    print("Travel itinerary has been generated and looks like this \n" + str(formatted_destinations))


# Run the main function
if __name__ == "__main__":

    main()

