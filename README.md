# Pesa Pulse API Analysis Project

## Project Overview

This project focuses on retrieving customer data from an API and analysing it using Python.

The data comes from JSONPlaceholder, an API that provides sample user records for practice.

**API URL:** https://jsonplaceholder.typicode.com/users

The project covers eight sections, from retrieving the data to creating charts. I used Python, Requests, Pandas, Matplotlib, and basic Python concepts such as loops, dictionaries, sets, and functions.

## Section 1: Retrieve Customer Data Using Requests

### What I did

I created a function called `get_customers(url)` to retrieve customer records from the API.

I stored the API URL in a variable so that I could reuse it instead of writing the URL repeatedly.

### Why I used Requests

Requests allows Python to communicate with an API and retrieve data.

- `requests.get()` sends a request to the API.
- `timeout=10` prevents the program from waiting too long.
- `raise_for_status()` checks whether the request was successful.
- `response.json()` converts the response into Python objects.
- `try` and `except` handle request errors.

### Simple example

```python
response = requests.get(url, timeout=10)
response.raise_for_status()
customers = response.json()
```

The API sends data in JSON format. After converting it using `.json()`, I can work with the records using Python.

### Findings

The results from the API request were:

- Data type: `list`
- Total records: 10
- First record: Successfully retrieved

The API request was successful, and the returned data was ready for further analysis.

**What I learned:** How to retrieve data from an API and handle request errors.

---

## Section 2: Explore Nested Dictionaries and Lists

### What I did

I created a recursive function called `explore(record, indent=0)` to understand how the API data is organised.

The function prints the keys and their data types. If a value contains another dictionary or list, the function explores it further.

### Why I used recursion

Recursion means a function calls itself.

I used it because some customer information is stored inside other dictionaries. Instead of manually checking every level, the function keeps exploring until it reaches the values.

### Simple example: Finding latitude

Consider this structure:

```python
customer = {
    "address": {
        "geo": {
            "lat": "-37.3159"
        }
    }
}
```

To reach the latitude, I follow this path:

- `customer` contains `address`.
- `address` contains `geo`.
- `geo` contains `lat`.

The code to access it is:

```python
customer["address"]["geo"]["lat"]
```

This returns `"-37.3159"`.

I used the `explore()` function to inspect this structure automatically rather than manually following every path.

### Findings

The first customer record contained:

- Integer: `id`
- Strings: `name`, `email`, `phone`
- Dictionaries: `address`, `geo`, `company`
- Nested coordinates: `address → geo → lat/lng`

The function successfully explored the nested structure and displayed the data types.

**What I learned:** How to navigate nested dictionaries and use recursion to explore data at different levels.

---

## Section 3: Extract Customer Attributes

### What I did

I created `extract_attributes(customers)` to extract the information needed for analysis.

The original records contain nested information. I wanted to place the important fields into one flat dictionary for each customer.

The 12 fields extracted are:

`id`, `name`, `username`, `email`, `email_domain`, `phone`, `city`, `zipcode`, `latitude`, `longitude`, `company`, and `website`.

### Why I used `.get()`

The `.get()` method retrieves a value from a dictionary. If the key does not exist, it can return a default value instead of immediately raising a `KeyError`.

### Simple example: Extracting a city

```python
address = customer.get("address", {})
city = address.get("city")
```

First, I access the customer's address. Then I access the city inside that address.

### Simple example: Extracting an email domain

```python
email = "example@example.com"
email_domain = email.rsplit("@", 1)[-1]
```

The result is:

```text
example.com
```

I also converted latitude and longitude from strings into floating-point numbers using `float()`.

For example:

```python
float("-37.3159")
```

This produces a numeric value that can be used for calculations.

### Findings

The results from the extraction were:

- Total records: 10
- Attributes per record: 12
- Latitude data type: `float`

The nested customer data was successfully converted into flat dictionaries containing the required attributes.

**What I learned:** How to extract information from nested dictionaries, create new fields, and convert values into suitable data types.

---

## Section 4: Find Unique Cities Using Sets

### What I did

I created `unique_cities(customers)` to identify all the different cities in the customer records.

### Why I used a set

A set stores unique values. If the same city appears several times, it only appears once in the set.

### Simple example

```python
cities = {"Nairobi", "Mombasa", "Nairobi"}
print(cities)
```

The set contains only two unique cities: Nairobi and Mombasa.

In my project, I used a set comprehension to collect city names directly from the customer records.

### Findings

The results previously obtained from the sample API data were:

- Total records: 10
- Unique cities: 10
- Average records per unique city: 1.00

The average was calculated by dividing the total number of records by the number of unique cities.

```python
len(customers) / len(cities)
```

### Marketing interpretation

In a real customer dataset, identifying unique cities could help a business understand where its customers are located. However, these results come from sample data, not actual Pesa Pulse customers.

**What I learned:** How sets remove duplicates and help identify unique values.

---

## Section 5: Count Customers by City and Email Domain

### Part A: Count customers by city

#### What I did

I created `city_counts(customers)` to count how many customer records belong to each city.

I used a dictionary to store the city names and their counts.

#### Why I used a loop and dictionary

A loop processes each customer one at a time. A dictionary stores the count for each city.

#### Simple example

```python
counts = {}

city = "Nairobi"
counts[city] = counts.get(city, 0) + 1
```

If Nairobi is not already in the dictionary, `.get(city, 0)` returns zero. Adding one gives Nairobi a count of one.

If another record belongs to Nairobi, the count increases to two.

### Part B: Count customers by email domain

#### What I did

I created `email_domain_counts(customers)` to count how often each email domain appears.

First, I extracted the email domains into a list. Then I used a dictionary comprehension to count the occurrences of each unique domain.

#### Why I used a dictionary comprehension

A dictionary comprehension allows me to create a dictionary in a compact way.

#### Simple example

```python
domains = ["gmail.com", "yahoo.com", "gmail.com"]

counts = {
    domain: domains.count(domain)
    for domain in set(domains)
}
```

The resulting counts are:

```python
{
    "gmail.com": 2,
    "yahoo.com": 1
}
```

### Sorting the results

I sorted the counts from highest to lowest. When two cities or domains have the same count, the names are arranged alphabetically.

```python
key=lambda item: (-item[1], item[0])
```

Here, `item[1]` represents the count and `item[0]` represents the city or domain name.

### Findings

The results from the sample API data were:

- Total records: 10
- Unique cities: 10
- Unique email domains: 10
- Count per city and email domain: 1 each

All records had different cities and email domains. The counts were sorted by frequency and alphabetically when counts were equal.

**What I learned:** How to count repeated values using dictionaries, use comprehensions, and sort results for easier interpretation.

---

## Section 6: Convert the Data into a Pandas DataFrame

### What I did

I created `to_dataframe(rows)` to convert the extracted customer records into a Pandas DataFrame.

A DataFrame organises information into rows and columns, similar to a spreadsheet.

### Why I used Pandas

Pandas makes it easier to inspect and analyse structured data.

- `.shape` shows the number of rows and columns.
- `.dtypes` shows the data type of each column.
- `.value_counts()` counts how often each value appears.

### Simple example

```python
df = pd.DataFrame(rows)
print(df.shape)
```

If a DataFrame contains 10 rows and 12 columns, its shape is:

```text
(10, 12)
```

I also used Pandas to count the cities and compare its results with the counts from my own `city_counts()` function.

### Why I compared the counts

If both methods return the same city counts, it provides a useful check that the manual counting logic is working correctly.

### Findings

The DataFrame results were:

- Rows: 10
- Columns: 12
- Latitude and longitude: `float64`
- City counts comparison: `True`

The DataFrame contained 10 customer records and 12 columns. The city counts from Pandas matched the counts calculated using my own function.

**What I learned:** How to organise data in a DataFrame, inspect its structure, and validate calculations using Pandas.

---

## Section 7: Export the Results to CSV

### What I did

I exported two files:

- `customers.csv` contains the extracted customer information.
- `city_counts.csv` contains each city and its customer count.

I converted the city-count dictionary into a DataFrame before exporting it.

### Why I used these methods

- `os.makedirs()` creates the output directory if it does not exist.
- `pd.DataFrame()` organises the city counts into columns.
- `.sort_values()` sorts the city counts.
- `.to_csv()` saves the DataFrame as a CSV file.
- `index=False` prevents Pandas from adding an extra index column to the exported file.

### Simple example

```python
df.to_csv("output/customers.csv", index=False)
```

This saves the DataFrame as a CSV file that can be opened in Excel or another data-analysis tool.

For the city summary, I specified the column names:

```python
city_df = pd.DataFrame(
    list(counts.items()),
    columns=["city", "customer_count"]
)
```

This ensures that the summary has a column for the city and another for its count.

### Findings

The exported files were successfully created and read back using Pandas.

- `customers.csv`: 10 rows, 12 columns
- `city_counts.csv`: 2 columns — `city` and `customer_count`
- CSV index: Excluded using `index=False`

The exported files retained the expected columns and data, making them ready for further analysis.

**What I learned:** How to export analysed data into files that can be shared, inspected, and reused.

---

## Section 8: Visualise Customer Distribution with Matplotlib

### What I did

I created `plot_distribution(counts, path)` to display customer counts using bar charts.

I used the same function to create two charts:

- `customer_distribution.png` shows the number of records per city.
- `email_domain_distribution.png` shows the number of records per email domain.

### Why I used Matplotlib

Matplotlib helps present numerical results visually.

- `plt.subplots()` creates the chart area.
- `ax.bar()` draws the bars.
- `set_title()` adds a chart title.
- `set_xlabel()` and `set_ylabel()` label the axes.
- `tick_params()` rotates category labels.
- `tight_layout()` helps prevent labels from overlapping.
- `savefig()` saves the chart as an image.
- `plt.close()` closes the figure after saving it.

### Simple example

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(
    sorted_counts.keys(),
    sorted_counts.values()
)

ax.set_title(title)
ax.set_xlabel(xlabel)
ax.set_ylabel("Number of Customer Records")

fig.tight_layout()
fig.savefig(path)
plt.close(fig)
```

The dictionary keys provide the categories, such as city names, while the values provide the counts.

### Findings

The following charts were successfully generated:

- `customer_distribution.png`
- `email_domain_distribution.png`

Both charts were saved in the output folder using Matplotlib. Each chart visualises the frequency counts for its respective category.

Since every city and email domain appears once, both charts show equal counts across all categories.

### Which chart is more useful?

The city chart helps show how records are distributed across cities. In this sample, every city has one record, so no city has a higher count than another.

The email-domain chart helps show which email domains occur most often. If multiple records share a domain, this chart makes that pattern easier to see.

For a real business dataset, the more useful chart would depend on the question being investigated.

**What I learned:** How to turn frequency counts into bar charts and save the visual results as image files.

---

## Project Structure

The intended project structure is:

```text
day1-api-analysis/
├── analysis.py
├── output/
│   ├── customers.csv
│   ├── city_counts.csv
│   ├── customer_distribution.png
│   └── email_domain_distribution.png
├── requirements.txt
└── README.md
```

## Tools and Libraries Used

| Tool | Purpose |
|---|---|
| Python | Main programming language |
| Requests | Retrieve data from the API |
| Pandas | Organise and analyse data |
| Matplotlib | Create charts |
| OS module | Manage output directories |
| CSV | Save data in a reusable format |

Python concepts used include functions, loops, dictionaries, sets, comprehensions, recursion, exception handling, and data-type conversion.

## Conclusion

This project helped me practise the process of retrieving data from an API, understanding nested structures, extracting useful fields, calculating counts, validating results, exporting files, and creating charts.

The results are based on 10 sample user records from JSONPlaceholder. They demonstrate the analysis process but do not represent actual Pesa Pulse customers.

## How to Run the Project

1. Download or clone the repository.
2. Install the required libraries.
3. Run the Python script from the project directory.
4. Open the generated CSV files and charts in the output directory.

```bash
pip install -r requirements.txt
python analysis.py
```

