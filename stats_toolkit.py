"""
Day 3 - Statistical Analysis Toolkit
Squad Python Specialization - Data Science, AI & Analytics

RULE: implement every calculation yourself with plain Python.
NumPy may be imported ONLY in compare_with_numpy(), to verify your results.
Do not use the statistics module.
"""
import csv
import math
from pathlib import Path

DATA_PATH = Path("data") / "agent_deposits.csv"


def load_column(path: Path, column: str) -> tuple[list[float], list[tuple[int, str]]]:
    """Return (valid_values, rejected) where rejected holds (row_number, raw_value) pairs."""
    valid_values = []
    rejected = []

    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Check the requested column
        if column not in (reader.fieldnames or []):
            raise ValueError(f"Column '{column}' not found in CSV")

        # Track the row number
        for row_number, row in enumerate(reader, start=2):
            raw_value = row[column]

            # Handle missing values
            if raw_value is None or raw_value.strip() == "":
                rejected.append((row_number, raw_value, "Missing value"))
                continue

            # Repair and convert numeric values
            try:
                cleaned_value = raw_value.replace(",", "").strip()
                value = float(cleaned_value)
                
            except (ValueError, TypeError):
                rejected.append((row_number, raw_value, "Invalid numeric value"))
                continue

            # Reject non-finite numbers
            if not math.isfinite(value):
                rejected.append((row_number, raw_value, "Non-finite numeric value"))
                continue

            valid_values.append(value)

    return valid_values, rejected





def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot calculate mean of an empty list")

    total = 0

    for value in values:
        total += value

    return total/len(values)


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot calculate median of an empty list")

    # order the values in ascending order
    ordered = sorted(values)
    middle = len(ordered) // 2

    if len(ordered) % 2 == 1:
        return ordered[middle]

    return (ordered[middle - 1] + ordered[middle]) / 2


def mode(values: list[float]) -> list[float]:
    """Return every value that occurs most often (a list, because there can be ties or none)."""
    if not values:
        raise ValueError("Cannot calculate mode of an empty list")

    frequencies = {}

    for value in values:
        if value in frequencies:
            frequencies[value] += 1

        else:
            frequencies[value] = 1

    high_frequencies = max(frequencies.values())

    if high_frequencies == 1:
        return []

    return sorted(
        value for value, count in frequencies.items()
        if count == high_frequencies
    )


def variance(values: list[float], sample: bool = True) -> float:
    """Sample variance (n - 1) by default; population variance (n) when sample is False."""
    if not values:
        raise ValueError("Cannot calculate variance of an empty list")

    if sample and len(values) < 2:
        raise ValueError("Sample variance requires at least two values")

    average = mean(values)
    squared_differences = []

    for value in values:
        difference = value - average
        squared_differences.append(difference ** 2)

    denominator = len(values) - 1 if sample else len(values)

    return sum(squared_differences) / denominator


def std_dev(values: list[float], sample: bool = True) -> float:
    return math.sqrt(variance(values, sample))


def quartiles(values: list[float]) -> tuple[float, float, float]:
    """Return (Q1, Q2, Q3). Document which quartile method you chose."""
    if not values:
        raise ValueError("Cannot calculate quartiles of an empty list")

    ordered = sorted(values)
    n = len(values)

    # find the median of the whole dataset
    q2 = median(values)

    # handle single value
    if n == 1:
        return ordered[0], q2, ordered[0]

    # split data into 2 halves
    if n % 2 == 0:
        lower_half = ordered[:n // 2]
        upper_half = ordered[n // 2:]
    else:
        lower_half = ordered[:n // 2]
        upper_half = ordered[n // 2 + 1:]

    # calculate Q1 & Q3
    q1 = median(lower_half)
    q3 = median(upper_half)

    return q1, q2, q3



def iqr_outliers(values: list[float], k: float = 1.5) -> dict:
    """Return the IQR, the lower and upper fences, and the values outside them."""
    # Get the quartiles
    q1, q2, q3 = quartiles(values)

    # Calculate the IQR
    iqr = q3 - q1

    # Calculate the fences
    # The default k is 1.5, as required by the IQR method.
    lower_fence = q1 - (1.5 * iqr)
    upper_fence = q3 + (1.5 * iqr)

    # Find the outliers
    outliers = [
        value for value in values
        if value < lower_fence or value > upper_fence
    ]

    # We return a dictionary so the rest of the program can easily access each result by its name.
    return {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "iqr": iqr,
        "lower_fence": lower_fence,
        "upper_fence": upper_fence,
        "outliers": outliers
    }
    


class StatisticsAnalyzer:
    """Wraps one numeric column and exposes every statistic above as a method."""

    def __init__(self, values: list[float], name: str = "values") -> None:
        if not values:
            raise ValueError("Cannot analyze an empty list")

        self.values = list(values)
        self.name = name
        self.sorted_values = sorted(values)
        self.count = len(values)
        self.rejected = []


    @classmethod
    def from_csv(cls, path: Path, column: str) -> "StatisticsAnalyzer":
        values, rejected = load_column(path, column)

        analyzer = cls(values, name=column)    #creates an instance of class
        analyzer.rejected = rejected           #stores rejected rows
        analyzer.source_path = path            #remembers which csv was loaded
        analyzer.column = column               #gives the completed object back to the caller

        return analyzer
    

    def summary(self) -> dict:
        result = iqr_outliers(self.values)

        return {
            "name": self.name,
            "count": self.count,
            "mean": mean(self.values),
            "median": median(self.values),
            "mode": mode(self.values),
            "variance": variance(self.values, sample=True),
            "std_dev": std_dev(self.values, sample=True),
            "min": self.sorted_values[0],
            "max": self.sorted_values[-1],
            "q1": result["q1"],
            "q2": result["q2"],
            "q3": result["q3"],
            "iqr": result["iqr"],
            "lower_fence": result["lower_fence"],
            "upper_fence": result["upper_fence"],
            "outliers": result["outliers"]
        }

    def without_outliers(self) -> "StatisticsAnalyzer":
        # Get IQR fences
        result = iqr_outliers(self.values)
        lower_fence = result["lower_fence"]
        upper_fence = result["upper_fence"]

        # Keep values inside the fences
        filtered_values = [
                value for value in self.values
                if lower_fence <= value <= upper_fence
            ]

        # Create a new analyzer
        analyzer = StatisticsAnalyzer(filtered_values, name=self.name)
        analyzer.rejected = self.rejected
        analyzer.source_path = getattr(self, "source_path", None)
        analyzer.column = getattr(self, "column", self.name)

        return analyzer

    def report(self) -> str:
        # get the summary
        stats = self.summary()

        lines = [
            f"Statistics report: {self.name}",
            f"Count: {stats['count']}",
            f"Mean: {stats['mean']:.2f}",
            f"Median: {stats['median']:.2f}",
            f"Mode: {stats['mode'] if stats['mode'] else 'none'}",
            f"Variance (sample): {stats['variance']:.2f}",
            f"Standard deviation (sample): {stats['std_dev']:.2f}",
            f"Minimum: {stats['min']:.2f}",
            f"Maximum: {stats['max']:.2f}",
            f"Q1: {stats['q1']:.2f}",
            f"Q2: {stats['q2']:.2f}",
            f"Q3: {stats['q3']:.2f}",
            f"IQR: {stats['iqr']:.2f}",
            f"Lower fence: {stats['lower_fence']:.2f}",
            f"Upper fence: {stats['upper_fence']:.2f}",
            f"Outliers: {stats['outliers']}",
        ]

        return "\n".join(lines)


def compare_with_numpy(analyzer: StatisticsAnalyzer) -> dict[str, bool]:
    """Import numpy HERE, recompute each statistic and return {name: matches}."""
    raise NotImplementedError


if __name__ == "__main__":
    # TODO
    pass
