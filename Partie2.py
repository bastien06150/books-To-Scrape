import requests
from bs4 import BeautifulSoup
import csv

# URL de la catégorie "Sports and Games"
base_url = (
    "https://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html"
)

# Liste pour stocker les données des livres
all_books_data = []


# Fonction pour extraire les informations d'un livre
def livre_sport_data(livre_url):
    response = requests.get(livre_url)
    soup = BeautifulSoup(response.text, "html.parser")

    product_page_url = livre_url
    universal_product_code = soup.find("th", string="UPC").find_next("td").text.strip()
    title = soup.find("h1").text.strip()
    price_including_tax = (
        soup.find("th", string="Price (incl. tax)").find_next("td").text.strip()
    )
    price_excluding_tax = (
        soup.find("th", string="Price (excl. tax)").find_next("td").text.strip()
    )
    number_available = (
        soup.find("th", string="Availability").find_next("td").text.strip()
    )
    product_description = soup.find("meta", {"name": "description"})["content"].strip()
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    image_url = "https://books.toscrape.com" + soup.find("img")["src"][5:]

    return {
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


# Fonction pour parcourir les pages de la catégorie et extraire les liens des livres
def scrape_category_pages():
    page_number = 1
    while True:
        # Construction de l'URL de la page
        if page_number == 1:
            url = base_url
        else:
            url = base_url.replace("index.html", f"page-{page_number}.html")

        print(f"Scraping page {page_number}: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraction des liens des livres
        books = soup.find_all("h3")
        if not books:
            break  # Si aucun livre n'est trouvé, la boucle s'arrête

        for book in books:
            book_url = (
                "https://books.toscrape.com/catalogue"
                + book.find("a")["href"][
                    8:
                ]  # Suppression des parties du chemin qui ne sont pas nécessaires pour accéder à l'image
            )
            book_data = livre_sport_data(book_url)
            all_books_data.append(book_data)

        page_number += 1


# Lancer l'extraction des données
scrape_category_pages()

# Enregistrement des données dans un fichier CSV
with open("sports_and_games_books.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=all_books_data[0].keys())
    writer.writeheader()
    writer.writerows(all_books_data)

print(" Extraction terminée et données enregistrées dans 'sports_and_games_books.csv'.")
