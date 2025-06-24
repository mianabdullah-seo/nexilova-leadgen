import requests
import pandas as pd

SERP_API_KEY = "your_serpapi_key_here"  # Replace this with your actual SerpAPI Key

def scrape_gmb(category, location):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_maps",
        "q": f"{category} in {location}",
        "api_key": SERP_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []

    for business in data.get("local_results", []):
        name = business.get("title")
        phone = business.get("phone")
        address = business.get("address")
        website = business.get("website")

        # Optional: Try to extract email/social from website content
        email, socials = None, []
        if website:
            try:
                site_data = requests.get(website, timeout=5).text
                if "@" in site_data:
                    start = site_data.find("@")
                    email = site_data[start-30:start+30].split()[0]
                for social in ["facebook", "instagram", "linkedin", "twitter"]:
                    if social in site_data:
                        socials.append(social)
            except:
                pass

        results.append({
            "Name": name,
            "Phone": phone,
            "Address": address,
            "Website": website,
            "Email": email,
            "Socials": ", ".join(socials)
        })

    df = pd.DataFrame(results)
    df.to_csv("leads.csv", index=False)
    return df
