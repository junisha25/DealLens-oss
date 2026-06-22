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


def get_recent_filings(cik: str):
    data = get_company_submissions(cik)

    recent = data["filings"]["recent"]

    filings = []

    for i in range(len(recent["form"])):
        filings.append({
            "form_type": recent["form"][i],
            "filing_date": recent["filingDate"][i],
            "accession_number": recent["accessionNumber"][i]
        })

    return filings
