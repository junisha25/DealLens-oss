import requests


HEADERS = {
    "User-Agent": "DealLens research project"
}


def get_company_submissions(cik: str):
    cik = str(cik).zfill(10)

    url = (
        f"https://data.sec.gov/submissions/"
        f"CIK{cik}.json"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.json()
