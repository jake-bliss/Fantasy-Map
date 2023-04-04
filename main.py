from flask import Flask, render_template, request, jsonify
import difflib
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, Document
from llama_index.node_parser import SimpleNodeParser
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mapapi as mapapi
# import config
import json
# os.environ["OPENAI_API_KEY"] = config.set_openai_key()
# config.set_openai_key()

# configure postgresql db connection


app = Flask(__name__)
auth = 'Basic dXNlcjE6cGFzc3dvcmQx'
map_api = mapapi.MapAPI(auth)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_text', methods=['POST'])
def get_text():
    print('In Function')
    print(request.get_json())
    input_text = str(request.get_json())
    subpages = []
    with open('static/subpages.txt', 'r') as f:
        for line in f:
            subpages.append(line.strip())

    closest_match = difflib.get_close_matches(
        'https://forgottenrealms.fandom.com/wiki/' + input_text, subpages, n=1, cutoff=0.1)
    if closest_match:
        return closest_match[0]
    else:
        return None

    return find_closest_match('troll bark', subpages)


@app.route('/get_summary', methods=['POST'])
def get_summary():
    # Get the HTML content of the web page
    url = "https://forgottenrealms.fandom.com/wiki/Semberholme"

    # Get the URL passed to us from the frontend
    url = str(request.get_json()['text'])
    # print(url)

    # Get the HTML content of the web page
    html_content = requests.get(url).text

    # Use BeautifulSoup to extract the text from <p> and <h> tags
    soup = BeautifulSoup(html_content, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    headings = [h.get_text() for h in soup.find_all(
        "h1") + soup.find_all("h2") + soup.find_all("h3")]

    # Combine the headings and paragraphs into a single string
    text = " ".join(headings + paragraphs)

    if check_url_exists(url) is None:
        # Create a GPTSimpleVectorIndex object
        # documents = [Document(text)]
        # parser = SimpleNodeParser()
        # nodes = parser.get_nodes_from_documents(documents)
        # index = GPTSimpleVectorIndex.from_documents(documents)

        # # Query the index
        # response = index.query("<summarization_query>",
        #                        response_mode="tree_summarize")

        response = 'The Get Summary function is working. But I do not want to pay for the API.'

        # Insert the URL and summary into the database
        map_api.create_summary(url, response)

    else:

        return check_url_exists(url)

    # response = 'The Get Summary function is working.'

    return str(response)


@app.route('/map_locations', methods=['GET'])
def get_map_locations():
    # Connect to the database
    locations = map_api.get_locations().json()

    # print(locations)
    return jsonify(locations)


@app.route('/map_location_create', methods=['POST'])
def map_location():
    data = request.get_json()
    lat = data['lat']
    lng = data['lng']
    title = data['title']
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Do something with the location and title data here
    message = 'Location received: ' + str(lat) + ', ' + str(lng) + ', ' + title
    response = {'message': message}

    map_api.create_marker(title, lat, lng, current_time)

    return jsonify(response)


@app.route('/map_location_delete', methods=['POST'])
def delete_map_location():
    # Get the latitude and longitude from the AJAX request data
    data = request.get_json()
    lat = data['lat']
    lng = data['lng']

    # Delete the map location with the given latitude and longitude from the database
    map_api.delete_marker(lat, lng)

    return 'Map location deleted successfully'

def check_url_exists(url):
    # Check API

    result = map_api.get_all_summaries()
    print (result)
    # Find URL in the response
    for item in json.loads(result):
        if item['url'] == url:
            return item['summary']
        else:
            return

    # return summary of result
    if result is not None:
        return result
    else:
        return

# @app.before_first_request
# def init_db():
#     return


if __name__ == '__main__':
    app.run(debug=True)
