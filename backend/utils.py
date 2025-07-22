# Performs a case-insensitive search for the keyword in the vendor field of receipts.
def linear_search(receipts, keyword):
    return [r for r in receipts if keyword.lower() in r[1].lower()]

# Returns the list of receipts sorted by amount in descending order.
def sort_by_amount(receipts):
    return sorted(receipts, key=lambda x: x[3], reverse=True)

# Aggregates total amount spent per vendor across all receipts.
def aggregate_by_vendor(receipts):

    agg = {}

    for r in receipts:
        vendor = r[1]
        # Sum the amount per vendor
        agg[vendor] = agg.get(vendor, 0) + r[3]

    return agg

from statistics import mean, median, mode

# Computes sum, mean, median, and mode for the amount field of all receipts.
def calculate_aggregates(receipts):

    # Extract all amounts from receipt records
    amounts = [r[3] for r in receipts]
    return {
        "sum": sum(amounts),
        "mean": mean(amounts),
        "median": median(amounts),
        "mode": mode(amounts)
    }
