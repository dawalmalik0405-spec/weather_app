import requests

def get_coordinates(location):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    response = requests.get(
        url,
        params={
            "name": location,
            "count": 10
        }
    )

    data = response.json()

    # print(data)

    

    results = data.get("results")
    if not results:
        return None

    for result in results:
        if "india" in result.get("country", "").lower():
            item = result
            break
    else:
        item = results[0]
    return {
        "latitude": item["latitude"],
        "longitude": item["longitude"],
        "name": item["name"],
        "country": item.get("country")
    }



def get_location_suggestions(
    query
):

    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": query,
            "count": 5
        }
    )

    data = response.json()

    return data.get(
        "results",
        []
    )