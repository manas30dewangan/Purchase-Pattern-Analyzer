# ==============================================================
# PS 74 : Customer Purchase Pattern Analyzer
# --------------------------------------------------------------
# What this program does:
#   1. Reads a CSV file of orders (default: orders.csv)
#   2. Skips rows whose Amount is not a number or is negative
#   3. Menu 1 -> monthly spending, total, best month, bar chart
#   4. Menu 2 -> number of orders, mean, median, best month
#   5. Menu 3 -> category percentage share, mean, median, pie chart
# ==============================================================

# ---------- STEP 1: Import libraries ----------
import pandas as pd              # pandas  : reads CSV and handles tables
import numpy as np               # numpy   : gives mean and median
import matplotlib.pyplot as plt  # matplotlib : draws charts


# ---------- STEP 2: Helper function to print money nicely ----------
def money(value):
    # 5000.0 should print as 5000, but 4250.5 should print as 4250.50
    if value == int(value):
        return str(int(value))
    return f"{value:.2f}"


# ---------- STEP 3: Load the file and remove invalid rows ----------
def load_data(file_name):
    # try / except: if the file is missing we show a message instead of crashing
    try:
        # utf-8-sig removes a hidden character that some editors add at the start
        table = pd.read_csv(file_name, encoding="utf-8-sig")
    except FileNotFoundError:
        print("Error: file '" + file_name + "' not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: file '" + file_name + "' is empty.")
        return None

    # Remove spaces around column names (" Amount " -> "Amount")
    table.columns = table.columns.str.strip()

    # Check that all 4 columns exist
    for column in ["OrderID", "Month", "Category", "Amount"]:
        if column not in table.columns:
            print("Error: column '" + column + "' is missing.")
            print("First line of the file must be: OrderID,Month,Category,Amount")
            return None

    valid_rows = []   # list that will store only the good rows
    skipped = 0       # counts how many rows we skipped

    # Visit every row. 'index' starts at 0, so row number = index + 1
    for index, row in table.iterrows():
        row_number = index + 1

        # Try to convert Amount to a number. "N/A" becomes NaN (not a number).
        amount = pd.to_numeric(row["Amount"], errors="coerce")

        if pd.isna(amount):
            print("Warning: Row " + str(row_number) + " skipped - Amount must be a number.")
            skipped = skipped + 1
        elif amount < 0:
            print("Warning: Row " + str(row_number) + " skipped - Amount cannot be negative.")
            skipped = skipped + 1
        else:
            # Row is fine, keep it
            valid_rows.append({
                "OrderID": row["OrderID"],
                "Month": str(row["Month"]).strip(),
                "Category": str(row["Category"]).strip(),
                "Amount": float(amount),
            })

    # Build a clean table from the valid rows
    clean = pd.DataFrame(valid_rows, columns=["OrderID", "Month", "Category", "Amount"])

    # Only print this line when something was skipped (Test Case 3)
    if skipped > 0:
        print("Valid orders analysed: " + str(len(clean)))

    return clean


# ---------- STEP 4: Monthly totals (used by menu 1 and menu 2) ----------
def get_monthly_totals(data):
    # groupby puts rows of the same month together, sum() adds their amounts.
    # sort=False keeps the months in file order (Jan, Feb, Mar, Apr)
    return data.groupby("Month", sort=False)["Amount"].sum()


# ---------- STEP 5: Menu 1 - Monthly spending ----------
def monthly_spending(data):
    monthly = get_monthly_totals(data)

    print("")
    for month in monthly.index:                   # loop over month names
        print(month + " : Rs. " + money(monthly[month]))

    print("Total: Rs. " + money(monthly.sum()))

    best = monthly.idxmax()                       # month with the highest total
    print("Best month: " + best + " (Rs. " + money(monthly[best]) + ")")

    # Draw the bar chart
    plt.bar(monthly.index, monthly.values)
    plt.title("Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Amount (Rs.)")
    print("(bar chart is displayed)")
    plt.show()                                    # opens the chart window


# ---------- STEP 6: Menu 2 - Order statistics ----------
def order_statistics(data):
    amounts = data["Amount"].values               # all amounts as a numpy array
    monthly = get_monthly_totals(data)
    best = monthly.idxmax()

    print("")
    print("Orders analysed: " + str(len(amounts)))
    print("Mean order value: Rs. " + f"{np.mean(amounts):.2f}")
    print("Median order value: Rs. " + f"{np.median(amounts):.2f}")
    print("Best month: " + best + " (Rs. " + money(monthly[best]) + ")")


# ---------- STEP 7: Menu 3 - Category share and statistics ----------
def category_share(data):
    # Total of each category, biggest first
    by_category = data.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    total = by_category.sum()
    amounts = data["Amount"].values

    print("")
    for category in by_category.index:
        percent = by_category[category] / total * 100     # part / whole * 100
        print(category + " : Rs. " + money(by_category[category]) + " (" + f"{percent:.2f}" + "%)")

    print("Mean order value: Rs. " + f"{np.mean(amounts):.2f}")
    print("Median order value: Rs. " + f"{np.median(amounts):.2f}")

    # Draw the pie chart
    plt.pie(by_category.values, labels=by_category.index, autopct="%1.2f%%")
    plt.title("Category Share")
    plt.show()


# ---------- STEP 8: Main program ----------
def main():
    # Ask for the file name. Pressing Enter alone uses orders.csv
    name = input("Enter CSV file name (press Enter for orders.csv): ").strip()
    if name == "":
        name = "orders.csv"

    data = load_data(name)

    # Stop if the file was missing/wrong, or no valid row is left
    if data is None:
        return
    if len(data) == 0:
        print("No valid orders to analyse.")
        return

    # Menu loop: repeats until the user chooses 4
    while True:
        print("")
        print("===== Customer Purchase Pattern Analyzer =====")
        print("1. Monthly spending")
        print("2. Order statistics")
        print("3. Category share and statistics")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            monthly_spending(data)
        elif choice == "2":
            order_statistics(data)
        elif choice == "3":
            category_share(data)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")


# Run main() only when this file is run directly
if __name__ == "__main__":
    main()