import requests
import xml.etree.ElementTree as ET
from flask import Flask, render_template, url_for



# RSS Feed URL
BASE_URL_1 = "https://www.wired.com/feed/tag/ai/latest/rss"
BASE_URL_2 = "https://www.wired.com/feed/category/business/latest/rss"
# https://www.wired.com/feed/category/business/latest/rss
SPORTS_URL = "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms"
ENTERTAINMENT_URL = "https://timesofindia.indiatimes.com/rssfeeds/2647163.cms"
MOST_RECENT_URL = "https://timesofindia.indiatimes.com/rssfeedsvideomostrecent.cms"
TOP_STORIES = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"

def getfromtimesofindia(category):
    if category == "topstories":
        response = requests.get(TOP_STORIES)
        if response.status_code == 200:
            # Parse the XML content
            root = ET.fromstring(response.content)

            info_list = []
            # Loop through each item in the feed
            for item in root.findall(".//item"):
                info = []
                title = item.find("title").text
                link = item.find("link").text
                pub_date = item.find("pubDate").text
                description = item.find("description").text

                # Get the image URL from enclosure tag
                enclosure = item.find("enclosure")
                image_url = enclosure.attrib.get("url", "No URL found") if enclosure is not None else "No image URL"

                # Append data to the info list
                info.extend([title, link, pub_date, description, image_url])
                info_list.append(info)
        else:
            print(f"Error fetching feed: {response.status_code}, {response.text}")
            info_list = []

        return info_list

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
    
@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/morenews/<string:category>")
def morenews(category):
    # Fetch news based on category
    if category in ["topstories"]:
        info_list = getfromtimesofindia(category)
    else:
        info_list = []  # Default empty list if the category is invalid

    return render_template("newsexplore.html", info_list=info_list)


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

if __name__ == "__main__":
    app.run(debug=True)


