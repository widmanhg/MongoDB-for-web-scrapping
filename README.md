![MongoDB](https://img.shields.io/badge/MongoDB-Community-green.svg)
[![Python](https://img.shields.io/badge/python-3.12.1-red.svg)](https://www.python.org/)


# MercadoLibre Scraper Project

This project consists of three Python scripts designed to scrape product data from MercadoLibre and store it in a MongoDB database. The scraping process is divided into two main steps, managed asynchronously using a controller script.

---

## Table of Contents

- [Overview](#overview)
- [Files](#files)
  - [1. urls.py](#1-urlspy)
  - [2. info.py](#2-infopy)
  - [3. main.py](#3-mainpy)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Testing](#testing)
- [Future Improvements](#future-improvements)

---

## Overview

This project automates the process of collecting product URLs and extracting detailed product information from MercadoLibre. 

1. **`urls.py`**: Scrapes product URLs based on given keywords and stores them in a MongoDB database.
2. **`info.py`**: Extracts detailed product information from the stored URLs and saves it back into the database.
3. **`main.py`**: Orchestrates the execution of the two scripts, ensuring that `info.py` runs 5 seconds after `urls.py`.

---

## Files

### 1. `urls.py`

This script is responsible for:
- Scraping product URLs for specified keywords and multiple pages.
- Saving the unique URLs into a MongoDB collection named `urls`.

#### Key Features:
- Connects to a MongoDB database.
- Avoids duplicate entries by checking for existing URLs in the database.

#### Output:
- A collection named `urls` in MongoDB containing the scraped product URLs.

#### Example Output:
*(Add screenshots or terminal output here.)*

---

### 2. `info.py`

This script processes the URLs stored in MongoDB and:
- Retrieves the product page.
- Extracts details such as:
  - Title
  - Price
  - Rating
  - Availability
  - Number of reviews
  - Discount and original prices
  - Product code
  - Image URLs
- Saves this information into a MongoDB collection named `info`.

#### Key Features:
- Uses `BeautifulSoup` for HTML parsing.
- Handles potential exceptions during HTTP requests.

#### Output:
- A collection named `info` in MongoDB containing detailed product data.

#### Example Output:
*(Add screenshots or terminal output here.)*

---

### 3. `main.py`

This script controls the asynchronous execution of `urls.py` and `info.py`. It:
- Executes `urls.py` first.
- Waits for 5 seconds before starting `info.py`.
- Ensures both scripts run asynchronously and outputs their progress to the console.

#### Key Features:
- Implements asynchronous execution using `asyncio`.
- Provides clear console logs for debugging.

#### Example Output:


![WhatsApp Image 2025-01-26 at 11 28 15_9c0b3de0](https://github.com/user-attachments/assets/46e760bd-d29f-421f-a5e9-c1be56cf5077)

![WhatsApp Image 2025-01-26 at 11 28 37_f8e93a3b](https://github.com/user-attachments/assets/134c72f3-d08d-45ec-baee-f56e3a0ef585)


---

## Setup and Installation

### Prerequisites:
- Python 3.7 or higher
- MongoDB installed and running locally
- Required Python libraries: `pymongo`, `beautifulsoup4`, `requests`, and `asyncio`

