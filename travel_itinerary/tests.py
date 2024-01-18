import numpy as np
import os
from main import generate_itinirary, main
from config import API_KEY

api_key = API_KEY

# Test case 1
destinations1 = ["London", "Manchester", "Liverpool", "Birmingham", "Leeds", "Newcastle", "Glasgow", "Edinburgh", "Bristol", "Cardiff", "Belfast", "Dublin", "Cork", "Galway", "Limerick"]
api_key = "<insert API key here>"
itinerary1 = generate_itinirary(destinations1, api_key)
assert len(itinerary1) == 15
assert all(dest in itinerary1["Destination"].values for dest in destinations1)

# Test case 2
destinations2 = ["Cambridge", "Oxford", "York", "Brighton", "Bath", "Canterbury", "Nottingham", "Sheffield", "Southampton", "Exeter", "Plymouth", "Bournemouth", "Reading", "Leicester", "Coventry"]
api_key = "<insert API key here>"
itinerary2 = generate_itinirary(destinations2, api_key)
assert len(itinerary2) == 15
assert all(dest in itinerary2["Destination"].values for dest in destinations2)

# Test case 3
destinations3 = ["Bristol", "Cardiff", "Bath", "Plymouth", "Exeter", "Southampton", "Reading", "Oxford", "Bournemouth", "Brighton", "Canterbury", "London", "Manchester", "Liverpool", "Birmingham"]
api_key = "<insert API key here>"
itinerary3 = generate_itinirary(destinations3, api_key)
assert len(itinerary3) == 15
assert all(dest in itinerary3["Destination"].values for dest in destinations3)


def test_main():
    # Test case 1: Valid input file path
    assert main("test_destinations.txt") == "Map saved to file: {}\nTravel itinerary has been generated and looks like this \n".format(os.path.join(os.getcwd(), "travel_map.html"))

    # Test case 2: Invalid input file path
    assert main("invalid_path.txt") == "File not found at path: invalid_path.txt"

    # Test case 3: Empty input file
    assert main("test_empty.txt") == "No destinations found in file: test_empty.txt"

    # Test case 4: Single destination in input file
    assert main("test_single_destination.txt") == "Map saved to file: {}\nTravel itinerary has been generated and looks like this \nLondon"

    # Test case 5: Input file with duplicate destinations
    assert main("test_duplicate_destinations.txt") == "Map saved to file: {}\nTravel itinerary has been generated and looks like this \nLondon\nBirmingham\nManchester\nGlasgow\nEdinburgh".format(os.path.join(os.getcwd(), "travel_map.html"))

    # Test case 6: Input file with non-existent destinations
    assert main("test_nonexistent_destinations.txt") == "Error occurred while retrieving geocode: 'NoneType' object is not subscriptable"
