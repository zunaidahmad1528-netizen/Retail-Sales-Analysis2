# Retail Sales Analysis

This project turns a retail sales CSV into useful business metrics and charts. I built it to practise a complete data-analysis workflow in Python: load a source file, clean the records, calculate revenue, and make the results easy to review.

The included dataset is synthetic, so its numbers are for demonstration only. You can run the project as-is or provide your own CSV file.

---

## What this project answers

A sales team usually wants quick answers to questions like these:

- How much revenue did we make, and from how many orders?
- What is the average value of an order?
- Which product categories bring in the most money?
- Which regions perform best, and which are falling behind?
- How does revenue change from month to month?

This pipeline answers all of them automatically, and saves the results as charts you can drop into a report or presentation.

---

## How it works

The script follows the same order a person would use when exploring a new dataset:

1. **Load.** Reads a CSV file, standardizes column names, and checks for the five required columns. It stops with a clear error if the file or a required column is missing.
2. **Clean.** Removes exact duplicate rows, converts dates and numbers, and drops rows with invalid dates or numeric values, or with a quantity or price at or below zero. It adds `revenue` (`quantity * unit_price`) and `month` for later analysis.
3. **Analyze.** Reports total revenue, row count, average revenue per row, and the category with the highest revenue. It also groups revenue by category and region.
4. **Visualize.** Saves charts for revenue by category, revenue by region, and monthly revenue to `outputs/`.

Every step writes a short log message, so you can see exactly how many rows were loaded, how many were removed during cleaning, and where each chart was saved.

---

## Project structure

```text
Retail-Sales-Analysis2/
├── data/
│   └── sample_sales.csv
├── src/
│   └── analysis.py
├── outputs/
│   ├── monthly_trend.png
│   ├── revenue_by_category.png
│   └── revenue_by_region.png
├── tests/
│   └── test_analysis.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Getting started

Python 3.14 was used to test this project.

**1. Clone the repository**

```bash
git clone https://github.com/zunaidahmad1528-netizen/Retail-Sales-Analysis2.git
cd Retail-Sales-Analysis2
```

**2. (Optional) Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
```

**3. Install the dependencies**

```bash
python -m pip install -r requirements.txt
```

**4. Run the analysis**

```bash
python src/analysis.py
```

By default it reads `data/sample_sales.csv` and writes charts to `outputs/`. To use your own data or choose a different output folder:

```bash
python src/analysis.py --input data/my_sales.csv --output my_results
```

---

## Using your own data

Your CSV needs these five columns. Their order does not matter, and extra columns are allowed. Column names are trimmed, lowercased, and spaces are replaced with underscores when the file is loaded.

| Column | Description | Example |
|---|---|---|
| `order_date` | Date of the order | `2025-03-14` |
| `category` | Product category | `Electronics` |
| `region` | Sales region | `North` |
| `quantity` | Units sold | `3` |
| `unit_price` | Price per unit | `249.99` |

One important assumption: each valid row is treated as one order. So `total_orders` is the number of rows left after cleaning, and `avg_order_value` is average revenue per row. If an order can contain multiple rows, include an order ID and calculate order-level metrics using that ID.

---

## Sample output

The charts below were generated from the included 400-row synthetic dataset. On this sample, the script reports total revenue of `208092.31`, average revenue per row of `520.23`, and `Electronics` as the top category. These are demonstration figures, not real business results; the values use the same units as the sample prices.

### Revenue by category

![Revenue by category](outputs/revenue_by_category.png)

### Revenue by region

![Revenue by region](outputs/revenue_by_region.png)

### Monthly revenue trend

![Monthly revenue trend](outputs/monthly_trend.png)

---

## Key findings

The included figures are only a walkthrough of the pipeline. When you run the script on real sales data, review the category, region, and monthly charts before drawing business conclusions.

---

## Running the tests

The project includes automated tests that check the cleaning logic and the KPI calculations.

```bash
python -m pytest
```

The tests check that duplicate and invalid rows are removed, KPI values are calculated as expected, and grouped revenue is sorted from highest to lowest.

---

## Design decisions

- **Functions over one long script.** Each step (load, clean, analyze, plot) is its own function, which makes the code easier to test and reuse.
- **Fail early with clear messages.** Missing files and missing columns raise specific errors right at the start.
- **Safe type conversion.** Dates and numbers are converted with `errors="coerce"`, so invalid values can be identified and removed during cleaning.
- **Logging instead of print statements.** Log messages show what the pipeline is doing and are easy to filter or redirect later.
- **Command-line arguments.** Input and output paths can be changed without editing the code.

---

## Limitations and next steps

- Profit cannot be calculated until the input includes product costs.
- Customer behavior cannot be analyzed until the input includes a customer ID.
- If one order spans multiple rows, an order ID is needed for accurate order counts and average order value.
- Further improvements could include handling empty cleaned datasets, adding more input-validation tests, or building a dashboard.

---

## Tech stack

The exact package versions are listed in [requirements.txt](requirements.txt).

- [pandas documentation](https://pandas.pydata.org/docs/)
- [Matplotlib documentation](https://matplotlib.org/stable/)
- [pytest documentation](https://docs.pytest.org/en/stable/)

---

## About me

I'm Zunaid, a Computer Science student building my skills in Python, SQL, Excel, and Power BI as I work toward a career in data analytics. Feedback and suggestions are welcome.

- [LinkedIn](https://www.linkedin.com/in/mohd-zunaid-23069a297/)
- [GitHub](https://github.com/zunaidahmad1528-netizen)
