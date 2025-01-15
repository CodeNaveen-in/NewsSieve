import requests
import xml.etree.ElementTree as ET
from flask import Flask, render_template



# RSS Feed URL
BASE_URL_1 = "https://www.wired.com/feed/tag/ai/latest/rss"


app = Flask(__name__)

@app.route("/")
def index():
    # Fetching the RSS feed
    response = requests.get(BASE_URL_1)

    if response.status_code == 200:
    # Parse the XML content
        root = ET.fromstring(response.content)
        namespace = {'media': 'http://search.yahoo.com/mrss/'}

        info_list  = []
    # Loop through each item in the feed
        for item in root.findall(".//item"):
            info = []
            title = item.find("title").text
            link = item.find("link").text
            pub_date = item.find("pubDate").text
            description = item.find("description").text
            thumbnail_element = item.find("media:thumbnail", namespace)
            thumbnail_url = thumbnail_element.attrib['url'] if thumbnail_element is not None else "No image URL"

            info.append(title)
            info.append(link)
            info.append(pub_date)
            info.append(description)
            info.append(thumbnail_url)
            info_list.append(info)
        else:
            print(f"Error: {response.status_code}, {response.text}")
        return render_template("index.html", info_list=info_list)

if __name__ == "__main__":
    app.run(debug=True)


