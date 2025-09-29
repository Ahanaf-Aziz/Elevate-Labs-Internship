import requests
from bs4 import BeautifulSoup

# Choose a news website (example: BBC News)
URL = "https://www.bbc.com/news"

# Fetch HTML
response = requests.get(URL)
response.raise_for_status()  # Raises error if request failed

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find headline elements (commonly <h2> tags)
headlines = soup.find_all("h2")

# Extract text and save to list
headline_texts = [headline.get_text(strip=True) for headline in headlines if headline.get_text(strip=True)]

# Save to .txt file
with open("headlines.txt", "w", encoding="utf-8") as f:
    for line in headline_texts:
        f.write(line + "\n")

print(f"Saved {len(headline_texts)} headlines to headlines.txt")
