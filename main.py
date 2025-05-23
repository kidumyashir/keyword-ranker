from flask import Flask, request, jsonify
import requests
import os
from urllib.parse import urlparse

app = Flask(__name__)

# מפתח SerpAPI שלך - לשימוש מקומי בלבד (לפרודקשן תשתמש ב־SECRET)
SERPAPI_KEY = "f09191e9529ac5c8524214e0fe7f5a79dbf754f912330921b57829c6b2fc6ff5"

def domain_matches(domain: str, link: str) -> bool:
    try:
        parsed = urlparse(link)
        link_domain = parsed.netloc.lower().replace("www.", "")
        target_domain = domain.lower().replace("www.", "")
        return link_domain == target_domain
    except Exception:
        return False

@app.route("/", methods=["POST"])
def check_ranking():
    data = request.get_json()
    keyword = data.get("keyword")
    domain = data.get("domain")

    if not keyword or not domain:
        return jsonify({"error": "Missing 'keyword' or 'domain'"}), 400

    try:
        params = {
            "engine": "google",
            "q": keyword,
            "google_domain": "google.co.il",
            "gl": "il",
            "hl": "he",
            "num": 100,
            "api_key": SERPAPI_KEY
        }

        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json()

        position = -1
        found_url = "N/A"

        for idx, result in enumerate(results.get("organic_results", []), start=1):
            link = result.get("link", "")
            if domain_matches(domain, link):
                position = idx
                found_url = link
                break

        return jsonify({
            "keyword": keyword,
            "domain": domain,
            "position": position,
            "url": found_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
