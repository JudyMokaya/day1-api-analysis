import os
import requests      #gives us access to Python's Requests library for making HTTP requests.
import pandas as pd 
import matplotlib.pyplot as plt

# section 1: Retrieve customer data with Requests
# API_URL stores the API address in a variable so we can reuse it without typing the URL repeatedly.
API_URL = "https://jsonplaceholder.typicode.com/users"

def get_customers(url):
    try:
        response = requests.get(url, timeout=10)    #requests.get() sends an HTTP GET request to the supplied URL.
        response.raise_for_status()    #This raises an exception if the server responds with an unsuccessful HTTP status, such as 404 or 500.
        customers = response.json()    # converts the response to python objects
        return customers

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")
        return []   #return an empty list if the request fails, allowing the calling code to recognise that no records were retrieved.


# Section 2: Explore nested dictionaries and lists
def explore(record, indent=0):
    if isinstance(record, dict):    #Checks whether the current object is a dictionary.
        for key, value in record.items():        #record.items()- Iterates over its key-value pairs.
            print(" " * indent + f"{key}: {type(value).__name__}")     #type(value).__name__ - Gets the readable Python type name

            if isinstance(value, (dict, list)):   #Checks whether the value needs further exploration
                explore(value, indent + 4)        #Calls the function again, increasing indentation by four spaces.

    elif isinstance(record, list):
        for index, value in enumerate(record):    #Provides both the list index and its value
            print(" " * indent + f"[{index}]: {type(value).__name__}")

            if isinstance(value, (dict, list)):
                explore(value, indent + 4)


# # Section 3: Extract customer attributes
def extract_attributes(customers):
    rows = []    #to return one flat dictionary for every customer

    # Loop through each customer
    for customer in customers:
        # Access the nested dictionaries
        address = customer.get("address", {})   #.get() with {} as the default also helps avoid a KeyError if a nested dictionary is missing
        geo = address.get("geo", {})
        company = customer.get("company", {})

        # extract email domain from email
        email = customer.get("email", "")   #returns an empty string if the key is missing

        email_domain = (email.rsplit("@", 1)[-1] if "@" in email else "")

        latitude = geo.get("lat")
        longitude = geo.get("lng")

        # Construct the flat dictionary
        row = {
            "id": customer.get("id"),
            "name": customer.get("name"),
            "username": customer.get("username"),
            "email": customer.get("email"),
            "email_domain": email_domain,
            "phone": customer.get("phone"),
            "city": address.get("city"),
            "zipcode": address.get("zipcode"),
            "latitude": float(geo["lat"]) if latitude else None,     # convert coordinates to float
            "longitude": float(geo["lng"]) if longitude else None,    # convert coordinates to float
            "company": company.get("name"),
            "website": customer.get("website")
}
        rows.append(row)    #adds the new dictionary to the list

    return rows


# # Section 4: Use sets to find unique cities
# # How many different cities are represented in the customer data?
def unique_cities(customers):
    cities = {
        customer.get("address", {}).get("city")
        for customer in customers
        # The .get() method also helps avoid an error if an address is missing.
        if customer.get("address", {}).get("city")   #It excludes missing or empty city values. 
    }

    return cities

# Count and compare
customers = get_customers(API_URL)
cities = unique_cities(customers)

# print(f"Total customers: {len(customers)}")
# print(f"Unique cities: {len(cities)}")

# if cities:
#     print(f"Customers per unique city: {len(customers) / len(cities):.2f}")


# # Section 5: Count customers by city and email domain
# # Part A — Count customers by city using loops
def city_counts(customers):
    counts = {}    #creates an empty dictionary for the results

    for customer in customers:      #processes every customer record.
        city = customer.get("address", {}).get("city")      #extracts the city from the nested address dictionary.

        if city:    #skips missing or empty city values
            counts[city] = counts.get(city, 0) + 1    #increases the count by 1

    return counts    #returns the completed dictionary

counts = city_counts(customers)
# print(counts)

sorted_cities = dict(
    sorted(
        counts.items(),    #gives each city and its count
        key=lambda item: (-item[1], item[0])   #sorts by count from highest to lowest, then alphabetically to break ties.

    )   #orders the entries
)    #converts the sorted entries back into a dictionary

# print(sorted_cities)


# # Part B — Count customers by email domain using a dictionary comprehension
def email_domain_counts(customers):
    domains = [
        customer.get("email", "").rsplit("@", 1)[-1]
        for customer in customers
        if "@" in customer.get("email", "")
    ]   # extracts email domain from email

    counts = {
        domain: domains.count(domain)
        for domain in set(domains)
    }   # counts each domain

    return counts   #returns the total count of each domain

# Print sorted email-domain counts
domain_counts = email_domain_counts(customers)

sorted_domains = dict(
    sorted(
        domain_counts.items(),
        key=lambda item: (-item[1], item[0])
    )
)

# print(sorted_domains)

# # Part C — Run both analyses together
counts = city_counts(customers)
domain_counts = email_domain_counts(customers)

# print("\nCustomers by city:")
# print(dict(sorted(
#     counts.items(),
#     key=lambda item: (-item[1], item[0])
# )))

# print("\nCustomers by email domain:")
# print(dict(sorted(
#     domain_counts.items(),
#     key=lambda item: (-item[1], item[0])
# )))


# # Section 6: Convert the data into a pandas DataFrame
def to_dataframe(rows):
    return pd.DataFrame(rows)

rows = extract_attributes(customers)

df = to_dataframe(rows)

# print("DataFrame shape:", df.shape)
# print("\nData types:")
# print(df.dtypes)

# print("\nCity counts using pandas:")
# print(df["city"].value_counts())

# manual_counts = city_counts(customers)
# pandas_counts = df["city"].value_counts().to_dict()

# print("\nDo the city counts agree?",
#     manual_counts == pandas_counts)


# # Section 7: Export the results to CSV
# Create the output directory if necessary
os.makedirs("output", exist_ok=True)

# Export customers.csv
df.to_csv("output/customers.csv", index=False)   #index=False means don't export the pandas row index

# Calculate city counts
counts = city_counts(customers)

# Convert counts into a DataFrame
city_df = pd.DataFrame(
    list(counts.items()),
    columns=["city", "customer_count"]
)

# Sort by count descending, then city alphabetically
city_df = city_df.sort_values(
    by=["customer_count", "city"],
    ascending=[False, True]
)

# Export the city summary without the index
city_df.to_csv("output/city_counts.csv", index=False)

# print("Customer data saved to output/customers.csv")
# print("City counts saved to output/city_counts.csv")


# print(pd.read_csv("output/customers.csv").shape)
# print(pd.read_csv("output/city_counts.csv").head())

# print(pd.read_csv("output/customers.csv").columns.tolist())
# print(pd.read_csv("output/city_counts.csv").columns.tolist())


# # Section 8: Visualise customer distribution with Matplotlib
def plot_distribution(counts, path):
    if not counts:
        print("No data available to plot.")
        return

    # Create the output directory if needed
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    # Sort from most common to least common
    sorted_counts = dict(
        sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0])
        )
    )


# Create the chart
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(sorted_counts.keys(), sorted_counts.values())

    # Choose a title based on the output filename
    if "domain" in path.lower():
        title = "Customer Distribution by Email Domain"
        xlabel = "Email Domain"
    else:
        title = "Customer Distribution by City"
        xlabel = "City"

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of Customer Records")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()

    # Save and release the figure
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
