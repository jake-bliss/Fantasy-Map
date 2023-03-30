from flask import Flask, render_template, request
import difflib
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, Document
from llama_index.node_parser import SimpleNodeParser
import os
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from secrets import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


app = Flask(__name__)


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
        input_text, subpages, n=1, cutoff=0.1)
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
        documents = [Document(text)]
        parser = SimpleNodeParser()
        nodes = parser.get_nodes_from_documents(documents)
        index = GPTSimpleVectorIndex.from_documents(documents)

        # Query the index
        response = index.query("<summarization_query>",
                               response_mode="tree_summarize")

        # Insert the URL and summary into the database
        insert_website_data(url, response)

    else:

        return check_url_exists(url)

    # response = 'The Get Summary function is working.'

    return str(response)


def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS website_data 
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                  URL TEXT, 
                  Summary TEXT, 
                  DateUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


def insert_website_data(url, summary):
    # create connection and cursor
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # check if url already exists in the database
    c.execute('SELECT * FROM website_data WHERE URL = ?', (url,))
    data = c.fetchone()
    if data is not None:
        print('URL already exists in the database')
        conn.close()
        return

    # insert data into table
    date_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO website_data (URL, Summary, DateUpdated) VALUES (?, ?, ?)',
              (url, str(summary), date_updated))

    # commit changes and close connection
    conn.commit()
    conn.close()


def check_url_exists(url):
    # create connection and cursor
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # execute query to check if URL exists in database
    c.execute('SELECT * FROM website_data WHERE URL=?', (url,))
    result = c.fetchone()

    # close connection
    conn.close()

    # return summary of result
    if result is not None:
        return result[2]
    else:
        return


@app.before_first_request
def init_db():
    create_table()
    print('Database created.')


if __name__ == '__main__':
    app.run(debug=True)
