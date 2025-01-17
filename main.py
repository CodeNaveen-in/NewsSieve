import requests
import xml.etree.ElementTree as ET
from flask import Flask, render_template, url_for, request, redirect
from bs4 import BeautifulSoup




# -----------------RSS Feed URLs---------------
#For Wired
TECHNOLOGY_URL = "https://www.wired.com/feed/tag/ai/latest/rss"
BUSINESS_URL = "https://www.wired.com/feed/category/business/latest/rss"
SCIENCE_URL = "https://www.wired.com/feed/category/science/latest/rss"

#For Times of India
MOST_RECENT_URL = "https://timesofindia.indiatimes.com/rssfeedsvideomostrecent.cms"
TOP_STORIES = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
entertainment_url = '1081479906'
world_url = '296589292'
sports_url = '4719148'
health_url = '2886704'


#Function to get news from Wired
def getfromwired(category):
    if category in ['technology', 'business', 'science']:
        if category == "technology":
            response = requests.get(TECHNOLOGY_URL)
        elif category == "business":
            response = requests.get(BUSINESS_URL)
        elif category == "science":
            response = requests.get(SCIENCE_URL)

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

                # Extract the media:thumbnail tag with its namespace
                namespaces = {'media': 'http://search.yahoo.com/mrss/'}
                thumbnail = item.find("media:thumbnail", namespaces)

                # Get the image URL if the media:thumbnail tag exists
                if thumbnail is not None:
                    image_url = thumbnail.attrib.get("url", "No URL found")
                    print(f"Image URL: {image_url}")
                else:
                    print("No thumbnail tag found.")

                info.extend([title, link, pub_date, description, image_url])
                info_list.append(info)
        else:
            print(f"Error fetching feed: {response.status_code}, {response.text}")\

    return info_list

#Function to get news from Times of India
def getfromtimesofindia(category):
    if category in ['topstories', 'latestnews']:
        if category == "topstories":
            response = requests.get(TOP_STORIES)
        elif category == "latestnews":
            response = requests.get(MOST_RECENT_URL)

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
    elif category in ['world', 'entertainment', 'sports', 'health']:
        if category == "world":
            value = world_url
        elif category == "entertainment":
            value = entertainment_url
        elif category == "sports":
            value = sports_url
        elif category == "health":
            value = health_url
        response = requests.get(f"https://timesofindia.indiatimes.com/rssfeeds/{value}.cms")
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

                # Clean the description using BeautifulSoup
                description_soup = BeautifulSoup(description, "html.parser")
                if description_soup.img:
                    description_soup.img.decompose()  # Remove the <img> tag
                clean_description = description_soup.get_text(strip=True)  # Extract plain text

                # Get the image URL from enclosure tag
                enclosure = item.find("enclosure")
                image_url = enclosure.attrib.get("url", "No URL found") if enclosure is not None else "No image URL"

                # Append data to the info list
                info.extend([title, link, pub_date, clean_description, image_url])
                info_list.append(info)
        else:
            print(f"Error fetching feed: {response.status_code}, {response.text}")
            info_list = []

    return info_list


app = Flask(__name__)

@app.route("/")
def index():
    info_list = getfromtimesofindia("topstories")
    return render_template("index.html", info_list=info_list)
    
@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/morenews/<category>")
def morenews(category):
    if category == "topstories":
        info_list = getfromtimesofindia("topstories")
        title = "Trending News"
    elif category == "latestnews":
        info_list = getfromtimesofindia("latestnews")
        title = "Latest News"
    elif category == "world":
        info_list = getfromtimesofindia("world")
        title = "World News"
    elif category == "entertainment":
        info_list = getfromtimesofindia("entertainment")
        title = "Entertainment News"
    elif category == "technology":
        info_list = getfromwired("technology")
        title = "Technology News"
    elif category == "sports":
        info_list = getfromtimesofindia("sports")
        title = "Sports News"
    elif category == "business":
        info_list = getfromwired("business")
        title = "Business News"
    elif category == "health":
        info_list = getfromtimesofindia("health")
        title = "Health News"
    elif category == "science":
        info_list = getfromwired("science")
        title = "Science News"
    return render_template("newsexplore.html", info_list=info_list, page_title=title.title())

@app.route("/inputform" , methods=["POST", "GET"])
def inputform():
    category = request.args.get("category")  # Retrieve the category from the query string
    if not category:
        return "Please select a category", 400

    # Call the appropriate function to fetch news based on the category
    if category == "world":
        return redirect(url_for("morenews", category="world"))
    elif category == "technology":
        return redirect(url_for("morenews", category="technology"))
    elif category == "sports":
        return redirect(url_for("morenews", category="sports"))
    elif category == "entertainment":
        return redirect(url_for("morenews", category="entertainment"))
    elif category == "business":
        return redirect(url_for("morenews", category="business"))
    elif category == "health":
        return redirect(url_for("morenews", category="health"))
    elif category == "science":
        return redirect(url_for("morenews", category="science"))
    else:
        info_list = []  # Handle invalid categories

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

if __name__ == "__main__":
    app.run(debug=True)


