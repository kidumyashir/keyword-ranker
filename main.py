from flask import Flask, request, jsonify
import requests
import os
from urllib.parse import urlparse

app = Flask(__name__)

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "your_serpapi_key_here")

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
            "api_key": SERPAPI_KEY
        }

        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json()

        position = -1
        found_url = "N/A"
        clean_domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").strip("/")

        for idx, result in enumerate(results.get("organic_results", []), start=1):
            link = result.get("link", "")
            parsed_link = urlparse(link).netloc.replace("www.", "")
            if clean_domain in parsed_link:
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
