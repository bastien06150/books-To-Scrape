# Books to Scrape - Price Tracker

Ce projet développe un système automatisé pour surveiller et enregistrer les prix des livres d'occasion sur [Books to Scrape](https://books.toscrape.com/), une librairie en ligne. Utilisant Python et BeautifulSoup, le script extrait les détails des produits tels que le titre, le prix, la disponibilité, et l'image, pour chaque livre listé

## Fonctionnalités

- Extraction des informations d'un produits **pour un livre**.
- Extraction des informations d'un produits **pour une catégorie**.
- Extraction des informations de produits **par catégorie**
- Enregistrement des données dans des **fichiers CSV par catégorie**
- Téléchargement et sauvegarde des **images des couvertures de livres**.

## Installation

Instructions pour configurer l'environnement, installer les dépendances, et exécuter le script.

### Prérequis

-Python 3.13.3
-BeautifulSoup4
-Requests

### Configuration de l'environement à partir du terminal

1. Clonez le dépot GitHub :

   ```
   Cloner git https://github.com/bastien06150/Books-to-Scrape.git

   ```

2. Installer l'environement virtuel :

   ```
   python -m venv env

   ```

3. Activer l'environement virtuel :

   ```
   .\env\scripts\activate.ps1.

   ```

4. Installer les dépendances :

   ```
   pip install -r requirements.txt

   ```
