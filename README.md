# NHL Draft Archetypes: A Value-Over-Expected Analysis

An end-to-end data engineering and analytics project that identifies scouting philosophies in the NHL (2005–2017) and evaluates their correlation with championship success.

## 📊 Project Overview
This project builds a custom analytics pipeline to quantify NHL scouting efficiency through a **Value-Over-Expected (VOE)** framework. By normalizing player outcomes against historical draft-position benchmarks, the system identifies how different franchises extract value across the seven-round draft landscape.

The core of the project is a **Strategic Segmentation** model that clusters all 31 franchises into six distinct "Scouting Archetypes." This segmentation provides a structured framework to explore the statistical relationship between drafting efficiency and postseason outcomes, ultimately highlighting the high variance between scouting success and championship hardware.

### **The Stack**
*   **Data Collection:** Python (Scrapy, BeautifulSoup)
*   **Analysis:** Pandas, NumPy, Scipy (Linear Regression)
*   **Machine Learning:** Scikit-learn (K-Means Clustering)
*   **Visualization:** Matplotlib, Seaborn, Tableau

---

## 🏗 Project Architecture
The project is structured as a sequential pipeline to ensure reproducibility and modularity:
```text
├── data/
│   ├── nhl_drafts_raw.db           # Initial scraped SQLite database
│   ├── nhl_drafts_clean.db          # Cleaned data post-EDA
│   ├── nhl_performance.csv          # Historical team/playoff outcomes
│   └── outputs/                     # Final CSVs feeding the Tableau Dashboard
│       ├── players.csv              # Individual draft outcomes with VOE scores
│       ├── team_by_round.csv        # Round-level averages and league percentiles
│       ├── team_by_year.csv         # Yearly draft performance trends
│       ├── team_rankings.csv        # Comprehensive 7-round efficiency rankings
│       └── team_rankings_early.csv  # High-leverage rankings (Rounds 1-3 only)
├── notebooks/
│   ├── eda.ipynb                    # Initial data cleaning & exploration
│   ├── 01_formula.ipynb             # Deriving the VOE performance score
│   ├── 02_methodology.ipynb         # Data preparation for clustering & dashboard
│   └── 03_findings.ipynb            # Final investigation & statistical analysis
├── scripts/
│   ├── scrape_draft_outcomes.py     # Scraper for draft history
│   └── scrape_team_performance.py   # Scraper for hockey-reference data
├── venv/                            # Virtual environment (local only)
├── requirements.txt                 # Project dependencies
└── .gitignore
```

---

## 🚀 Getting Started

### **1. Environment Setup**
Ensure you have Python 3.x installed. Clone the repository and set up the virtual environment:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Running the Pipeline**
The project is designed to be run sequentially to maintain data integrity:

1.  **Scraping:** Run the scripts in `/scripts` to refresh the raw data from the source.
2.  **Analysis:** Open Jupyter Notebook and execute the notebooks in order:
    *   `01_formula.ipynb`: Generates the performance weights and VOE logic.
    *   `02_methodology.ipynb`: Handles clustering and exports the final CSVs to `/data/outputs`.
    *   `03_findings.ipynb`: Conducts the final statistical investigations and visualizations.

> **Note:** Ensure your Jupyter Notebook kernel is set to the `.venv` created in Step 1 to ensure all dependencies are recognized.

---

## 💡 Key Findings

*   **The Parity Paradox:** Five different drafting archetypes are represented in the Top 6 most successful playoff teams, proving there is no "one true way" to build a contender in the NHL.
*   **The 3.5% Reality:** Statistical regression ($R^2 = 0.035$) reveals that while drafting provides a competitive "floor," championship "ceilings" are driven by high-impact outliers (Lottery Luck) and external variables like goaltending variance.
*   **Efficiency of Chaos:** Teams like the **LA Kings** demonstrated that "opportune" success can outweigh sheer volume, winning two championships with significantly fewer total series wins than their peers.

**Dashboard:** [View the interactive Tableau dashboard here](https://public.tableau.com/app/profile/van.brantley/viz/NHLDraftEfficiencyAnalysis2005-2017/Dashboard1?publish=yes)

---

## 🛠 Author

**Van Brantley**  
*Data Analyst | Analytics Engineering*

*   **Portfolio:** [vanbrantley.com](https://vanbrantley.com)

---
*This project was completed as part of a professional data portfolio to demonstrate end-to-end pipeline construction, from web scraping to statistical investigation.*

