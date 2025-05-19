import requests
from bs4 import BeautifulSoup
import csv

# URL de la page principale
base_url = "https://books.toscrape.com/index.html"


# Fonction pour extraire les liens des catégories
def get_category_links():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    categories = soup.find("ul", class_="nav-list").find_all("a")
    category_links = [
        "https://books.toscrape.com/catalogue" + category["href"][8:]
        for category in categories
    ]
    return category_links


# Fonction pour extraire les informations d'un livre
def get_book_info(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1").text.strip()
    price = soup.find("p", class_="price_color").text.strip()
    availability = soup.find("p", class_="instock availability").text.strip()
    rating = soup.find("p", class_="star-rating")["class"][1]
    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating,
    }


# Fonction pour extraire les livres d'une catégorie
def get_books_from_category(category_url):
    books = []
    page_number = 1
    while True:
        url = (
            category_url.replace("index.html", f"page-{page_number}.html")
            if page_number > 1
            else category_url
        )
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        book_links = [
            "https://books.toscrape.com/catalogue" + book.find("a")["href"][8:]
            for book in soup.find_all("h3")
        ]
        if not book_links:
            break
        for book_link in book_links:
            book_info = get_book_info(book_link)
            books.append(book_info)
        page_number += 1
    return books


# Fonction pour enregistrer les livres dans un fichier CSV
def save_books_to_csv(category_name, books):
    if books:
        keys_list = list(books[0].keys())  # Conversion en liste
        with open(
            f"{category_name}_books.csv", mode="w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=keys_list)
            writer.writeheader()
            writer.writerows(books)
    else:
        print(f"Aucun livre trouvé pour la catégorie {category_name}.")


# Extraction des catégories et des livres
category_links = get_category_links()
for category_link in category_links:
    category_name = category_link.split("/")[-2]
    print(f"Extraction des livres de la catégorie : {category_name}")
    books = get_books_from_category(category_link)
    save_books_to_csv(category_name, books)

print(" Extraction terminée pour toutes les catégories.")
