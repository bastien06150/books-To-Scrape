import requests
from bs4 import BeautifulSoup
import csv

# URL de la page sport et jeux
url = "https://books.toscrape.com/catalogue/the-book-of-basketball-the-nba-according-to-the-sports-guy_232/index.html"

# analyser the HTML content
reponse = requests.get(url)
soup = BeautifulSoup(reponse.text, "html.parser")

product_page_url = url
universal_product_code = soup.find("th", string="UPC").find_next("td").string.strip()
title = soup.find("h1").string.strip()
price_including_tax = (
    soup.find("th", string="Price (incl. tax)").find_next("td").string.strip()
)
price_excluding_tax = (
    soup.find("th", string="Price (excl. tax)").find_next("td").string.strip()
)
number_available = soup.find("th", string="Availability").find_next("td").string.strip()
product_description = soup.find("meta", {"name": "description"})["content"].strip()
category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
review_rating = soup.find("p", class_="star-rating")["class"][1]
image_url = soup.find("img")["src"]
image_url = "https://books.toscrape.com" + image_url


livre_data = [
    {
        "product_page_url": product_page_url,
        "universal_product_code": universal_product_code,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url,
    }
]


# sauvegarder dans un fichier csv
with open("livre_basket.csv", mode="w", newline="", encoding="utf-8") as fichier_csv:
    fieldnames = [
        "product_page_url",
        "universal_product_code",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url",
    ]

    writer = csv.DictWriter(fichier_csv, fieldnames=fieldnames)

    writer.writeheader()

    writer.writerows(livre_data)

print(" Fichier CSV 'livre_basket.csv' créé avec succès !")
