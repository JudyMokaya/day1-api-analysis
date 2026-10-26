
"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR = Path("output")


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        customers = response.json()

        if not isinstance(customers, list):
            print("Request succeeded, but the response was not a list of customers.")
            return []

        return customers

    except (requests.exceptions.RequestException, json.JSONDecodeError) as error:
        print(f"Could not retrieve customer data: {error}")
        return []


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    if isinstance(record, dict):
        for key, value in record.items():
            print(" " * indent + f"{key}: {type(value).__name__}")
            if isinstance(value, (dict, list)):
                explore(value, indent + 4)

    elif isinstance(record, list):
        for index, value in enumerate(record):
            print(" " * indent + f"[{index}]: {type(value).__name__}")
            if isinstance(value, (dict, list)):
                explore(value, indent + 4)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = []

    for customer in customers:
        address = customer.get("address", {})
        geo = address.get("geo", {})
        company = customer.get("company", {})
        email = customer.get("email", "")
        email_domain = email.rsplit("@", 1)[-1] if "@" in email else ""

        latitude = geo.get("lat")
        longitude = geo.get("lng")

        try:
            latitude = float(latitude) if latitude not in (None, "") else None
        except (TypeError, ValueError):
            latitude = None

        try:
            longitude = float(longitude) if longitude not in (None, "") else None
        except (TypeError, ValueError):
            longitude = None

        row = {
            "id": customer.get("id"),
            "name": customer.get("name"),
            "username": customer.get("username"),
            "email": email,
            "email_domain": email_domain,
            "phone": customer.get("phone"),
            "city": address.get("city"),
            "zipcode": address.get("zipcode"),
            "latitude": latitude,
            "longitude": longitude,
            "company": company.get("name"),
            "website": customer.get("website"),
        }

        rows.append(row)

    return rows


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {
        customer.get("address", {}).get("city")
        for customer in customers
        if customer.get("address", {}).get("city")
    }


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop (no Counter or pandas)."""
    counts = {}

    for customer in customers:
        city = customer.get("address", {}).get("city")

        if city:
            counts[city] = counts.get(city, 0) + 1

    return counts


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    domains = []

    for customer in customers:
        email = customer.get("email", "")

        if "@" not in email:
            continue

        domain = email.rsplit("@", 1)[-1]

        if "." in domain:
            top_level_domain = domain.rsplit(".", 1)[-1].lower()
            domains.append(top_level_domain)

    return {
        domain: domains.count(domain)
        for domain in set(domains)
    }


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert extracted customer rows into a Pandas DataFrame."""
    return pd.DataFrame(rows)


def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    if not counts:
        print(f"No data available to plot: {path}")
        return

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    sorted_counts = dict(
        sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(sorted_counts.keys(), sorted_counts.values())

    if "domain" in path.stem.lower():
        ax.set_title("Customer Distribution by Email Top-Level Domain")
        ax.set_xlabel("Email Top-Level Domain")
    else:
        ax.set_title("Customer Distribution by City")
        ax.set_xlabel("City")

    ax.set_ylabel("Number of Customer Records")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved to {path}")


plot_distribution(
    counts,
    "output/customer_distribution.png"
)

plot_distribution(
    domain_counts,
    "output/email_domain_distribution.png"
)









customers = get_customers(API_URL)
# sec3
# rows = extract_attributes(customers)

# print(rows[0])
# print(len(rows))
# print(rows[0]["latitude"], type(rows[0]["latitude"]))
# print(len(rows[0]))
# print(rows[0].keys())

# sec 2
# if customers:
#     explore(customers[0])


# sec1
# print(type(customers))
# print(len(customers))
# print(customers[0])


# sample = {
#     "name": "Leanne",
#     "address": {
#         "city": "Gwenborough",
#         "geo": {
#             "lat": "-37.3159"
#         }
#     }
# }

# explore(sample)
