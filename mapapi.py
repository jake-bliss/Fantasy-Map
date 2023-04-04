import requests
import json

class MapAPI:
    def __init__(self, auth):
        self.auth = auth

    def create_marker(self, name, lat, lng, date_modified):
        url = "https://map-api-gsarurbmea-uc.a.run.app/api/createMarker"
        payload = json.dumps({
            "name": name,
            "lat": lat,
            "lng": lng,
            "date_modified": date_modified
        })
        headers = {
            'Authorization': self.auth,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        return response

    def update_marker(self, name, lat, lng, date_modified):
        url = "http://172.20.40.227:8080/api/updateMarker"
        payload = json.dumps({
            "name": name,
            "lat": lat,
            "lng": lng,
            "date_modified": date_modified
        })
        headers = {
            'Authorization': self.auth,
            'Content-Type': 'application/json'
        }
        response = requests.put(url, headers=headers, data=payload)
        return response

    def get_marker(self, name):
        url = f"https://map-api-gsarurbmea-uc.a.run.app/api/getMarker?name={name}"
        headers = {
            'Authorization': self.auth,
        }
        response = requests.get(url, headers=headers)
        return response

    def delete_marker(self, lat, lng):
        url = f"https://map-api-gsarurbmea-uc.a.run.app/api/deleteMarker?lat={lat}&lng={lng}"
        headers = {
            'Authorization': self.auth,
        }
        response = requests.delete(url, headers=headers)
        return response


    def get_locations(self):
        url = "https://map-api-gsarurbmea-uc.a.run.app/api/locations"
        headers = {
            'Authorization': self.auth,
        }
        response = requests.get(url, headers=headers)
        return response
    

    def get_summary(self, url):
        """
        Gets a summary for a given URL.
        Args:
            url (str): The URL for which to retrieve a summary.
        Returns:
            The summary for the given URL.
        """
        url = "https://map-api-gsarurbmea-uc.a.run.app/api/getSummary"
        payload = json.dumps({
            "url": url
        })
        headers = {
            'Authorization': 'Basic dXNlcjE6cGFzc3dvcmQx',
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text


    def delete_summary(self, url):
        """
        Deletes the summary for a given URL.
        Args:
            url (str): The URL for which to delete the summary.
        Returns:
            The response text from the server.
        """
        url = "https://map-api-gsarurbmea-uc.a.run.app/api/deleteSummary"
        payload = json.dumps({
            "url": url
        })
        headers = {
            'Authorization': 'Basic dXNlcjE6cGFzc3dvcmQx',
            'Content-Type': 'application/json'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        return response.text


    def get_all_summaries(self):
        """
        Gets all summaries stored on the server.
        Returns:
            The response text from the server.
        """
        url = "https://map-api-gsarurbmea-uc.a.run.app/api/getAllSummaries"
        payload = {}
        headers = {
            'Authorization': 'Basic dXNlcjE6cGFzc3dvcmQx'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text


    def create_summary(self, url, summary):
        """
        Creates a summary for a given URL.
        Args:
            url (str): The URL for which to create a summary.
            summary (str): The summary to create.
        Returns:
            The response text from the server.
        """
        url = "https://map-api-gsarurbmea-uc.a.run.app/api/createSummary"
        payload = json.dumps({
            "url": url,
            "summary": summary
        })
        headers = {
            'Authorization': 'Basic dXNlcjE6cGFzc3dvcmQx',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

if __name__ == "__main__":
    auth = 'Basic dXNlcjE6cGFzc3dvcmQx'
    map_api = MapAPI(auth)
    
    # # Example usage:
    # response = map_api.create_marker("New Marker 3", "37.7749", "-122.4194", "2022-04-02T15:25:30Z")
    # print(response.text)
    
    # response = map_api.update_marker(2, "New Marker 2 V2", "37.0000", "-122.4194", "2022-04-03T15:25:30Z")
    # print(response.text)
    
    # response = map_api.get_marker("New Marker 3")
    # print(response.text)
    
    # response = map_api.delete_marker("New Marker")
    # print(response.text)
    
    response = map_api.get_locations()
    print(response.text)




