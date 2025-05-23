import requests
import os
import csv
from bs4 import BeautifulSoup
import re


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*#]', "_", filename)


# Récupérer le contenu HTML
base_url = "https://books.toscrape.com/"
url = f"{base_url}index.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# trouver le lien de chaque catégorie
categories = soup.find("ul", class_="nav nav-list").find_all("a")[1:]


def livre_data(livre_url):
    response = requests.get(livre_url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table table-striped")
    upc = table.find("th", string="UPC").find_next("td").string.strip()
    type_de_produit = (
        table.find("th", string="Product Type").find_next("td").string.strip()
    )
    price_excl_tax = (
        table.find("th", string="Price (excl. tax)").find_next("td").string.strip()
    )
    price_incl_tax = (
        table.find("th", string="Price (incl. tax)").find_next("td").string.strip()
    )
    tax = table.find("th", string="Tax").find_next("td").string.strip()
    availability = (
        table.find("th", string="Availability").find_next("td").string.strip()
    )
    Number_of_reviews = (
        table.find("th", string="Number of reviews").find_next("td").string.strip()
    )

    image_url = base_url + soup.find("img")["src"].replace("../..", "")

    print(image_url)

    return {
        "UPC": upc,
        "type_De_produit": type_de_produit,
        "Price_excl_tax": price_excl_tax,
        "price_incl_tax": price_incl_tax,
        "Tax": tax,
        "availability": availability,
        "Number_of_reviews": Number_of_reviews,
        "Image_url": image_url,
    }


def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, mode="wb") as file:
            file.write(response.content)


def save_to_csv(data, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "Category",
            "Title",
            "UPC",
            "Product Type",
            "Price",
            "Tax",
            "Availability",
            "Number of Reviews",
            "Image Path",
        ]
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)


all_books_data = []
images_folder = "images"

# création du dossier pour les images
os.makedirs(images_folder)


for category in categories:
    category_name = category.string.strip()

    category_url = base_url + category["href"].lstrip("/")
    print(f"Scraping category: {category_name} - URL: {category_url}")
    page_number = 1

    while True:
        # Construction de l'URL de la page
        page_url = (
            f"{category_url.replace('index.html', '')}page-{page_number}.html"
            if page_number > 1
            else category_url
        )

        # Récupération du contenu de la page
        response = requests.get(page_url)
        if response.status_code != 200:
            print(f"echec {page_url}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        # Extraction des informations sur les livres
        for book in books:
            book_title = book.h3.a["title"]
            book_url = (
                base_url + "catalogue/" + book.h3.a["href"].replace("../../../", "")
            )
            book_info = livre_data(book_url)
            # Limiter le titre pour éviter les chemins trop longs
            short_title = book_title[:100]  # limite à 100 caractères
            image_filename = sanitize_filename(f"{short_title.replace('/', '_')}.jpg")

            image_path = os.path.join(images_folder, image_filename)

            download_image(book_info["Image_url"], image_path)
            book_data = {
                "Category": category_name,
                "Title": book_title,
                "UPC": book_info["UPC"],
                "Product Type": book_info["type_De_produit"],
                "Price": book_info["Price_excl_tax"],
                "Tax": book_info["Tax"],
                "Availability": book_info["availability"],
                "Number of Reviews": book_info["Number_of_reviews"],
                "Image Path": image_path,
            }
            all_books_data.append(book_data)

        # Vérification de la présence de la page suivante
        next_page = soup.find("li", class_="next")
        if next_page:
            page_number += 1
        else:
            break

# Sauvegarde des données dans un fichier CSV
save_to_csv(all_books_data, "books_info.csv")
