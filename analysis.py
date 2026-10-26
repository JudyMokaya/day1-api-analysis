
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


def main() -> None:
    """Run the analysis steps and print a short findings summary."""
    customers = get_customers()

    if not customers:
        print("Analysis stopped because no customer records were retrieved.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Section 1: Retrieve customer data
    print("--- Section 1: Retrieve customer data ---")
    print(f"Total records retrieved: {len(customers)}")
    print(f"Response type: {type(customers).__name__}")

    # Section 2: Explore nested data
    print("\n--- Section 2: Explore the first customer ---")
    explore(customers[0])

    # Section 3: Extract attributes
    print("\n--- Section 3: Extract customer attributes ---")
    rows = extract_attributes(customers)
    df = to_dataframe(rows)
    print(f"Extracted records: {len(rows)}")
    print(f"Attributes per record: {len(rows[0]) if rows else 0}")

    if rows:
        print(f"Latitude data type: {type(rows[0]['latitude']).__name__}")

    # Section 4: Unique cities
    print("\n--- Section 4: Unique cities ---")
    cities = unique_cities(customers)
    print(f"Total records: {len(customers)}")
    print(f"Unique cities: {len(cities)}")

    if cities:
        print(
            "Average records per unique city: "
            f"{len(customers) / len(cities):.2f}"
        )

    # Section 5: Count customers by city and top-level email domain
    print("\n--- Section 5: Count customers ---")
    city_summary = city_counts(customers)
    domain_summary = email_domain_counts(customers)

    sorted_cities = dict(
        sorted(city_summary.items(), key=lambda item: (-item[1], item[0]))
    )
    sorted_domains = dict(
        sorted(domain_summary.items(), key=lambda item: (-item[1], item[0]))
    )

    print("Customers by city:", sorted_cities)
    print("\nCustomers by email top-level domain:", sorted_domains)

    # Section 6: DataFrame validation
    print("\n--- Section 6: DataFrame validation ---")
    print("DataFrame shape:", df.shape)
    print("Data types:")
    print(df.dtypes)

    pandas_city_counts = df["city"].value_counts().to_dict()
    print(
        "Manual city counts match Pandas:",
        city_summary == pandas_city_counts
    )

    # Section 7: Export CSV files
    print("\n--- Section 7: Export CSV files ---")
    df.to_csv(OUTPUT_DIR / "customers.csv", index=False)

    city_df = pd.DataFrame(
        list(city_summary.items()),
        columns=["city", "customer_count"],
    ).sort_values(
        by=["customer_count", "city"],
        ascending=[False, True],
    )

    city_df.to_csv(OUTPUT_DIR / "city_counts.csv", index=False)

    print(f"Customer data saved to {OUTPUT_DIR / 'customers.csv'}")
    print(f"City counts saved to {OUTPUT_DIR / 'city_counts.csv'}")

    # Section 8: Create charts
    print("\n--- Section 8: Create charts ---")
    plot_distribution(
        city_summary,
        OUTPUT_DIR / "customer_distribution.png",
    )
    plot_distribution(
        domain_summary,
        OUTPUT_DIR / "email_domain_distribution.png",
    )


if __name__ == "__main__":
    main()
