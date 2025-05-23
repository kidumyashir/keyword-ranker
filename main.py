from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["POST"])
def check_ranking():
    data = request.get_json()
    keyword = data.get("keyword")
    domain = data.get("domain")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    search_url = f"https://www.google.co.il/search?q={keyword.replace(' ', '+')}&hl=en&gl=il"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='yuRUbf')

    position = -1

    for index, result in enumerate(results, start=1):
        link = result.find('a')['href']
        if domain in link:
            position = index
            break

    return jsonify({
        "keyword": keyword,
        "domain": domain,
        "position": position
    })
