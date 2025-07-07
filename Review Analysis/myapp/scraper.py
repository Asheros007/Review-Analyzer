import requests
from bs4 import BeautifulSoup

def scrape_reviews(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Unable to fetch the page: {e}"
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: find all review paragraphs inside divs with class 'review-text'
    reviews = soup.find_all('div', class_='quote')

    if not reviews:
        return "No reviews found on this page."

    # Extract text and join
    review_texts = [rev.get_text(strip=True) for rev in reviews]
    combined_text = "\n\n".join(review_texts)

    return combined_text
