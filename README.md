 # 🛡️ Banking Transaction Analysis & Fraud Pattern Detection System

> An interactive Streamlit-powered web dashboard that visually exposes credit card fraud patterns using Plotly charts, live KPI metrics, per-card investigation tools, and analyst-ready filtered tables — no ML model required.

**Developed by:** A.C. Pravin Kumar • Raja • Sham • Perarasu • Vignesh • Tamil • Niranjan Kumar  
**Programme:** B.E CSE (AIML-B) | KPRIET

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Our Solution](#our-solution)
- [Tech Stack](#tech-stack)
- [Dataset Details](#dataset-details)
- [Features](#features)
- [Dashboard Walkthrough](#dashboard-walkthrough)
- [Data Flow](#data-flow)
- [Cardholder Investigation (v2)](#cardholder-investigation-v2)
- [Card Perks & Features (v3)](#card-perks--features-v3)
- [Key Code Snippets](#key-code-snippets)
- [Challenges & Learnings](#challenges--learnings)
- [Installation & Running](#installation--running)
- [Future Scope](#future-scope)
- [Version History](#version-history)

---

## ❗ Problem Statement

Credit card fraud causes **billions in annual losses** globally. Traditional rule-based detection systems struggle with sophisticated, evolving fraud patterns in high-volume, real-time transaction data. Analysts lack quick, visual tools to triage and investigate suspicious activity at the individual card level.

---

## ✅ Our Solution

An interactive Streamlit web dashboard that:
- Visually exposes fraud patterns through 4 rich, interactive Plotly charts
- Delivers live KPI metrics updated dynamically on every filter change
- Supports per-card drill-down investigation with risk classification
- Displays enriched cardholder profiles (tier, miles, rewards, discounts)
- Works fully out of the box with synthetic demo data — no CSV upload required

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.x | Core language for data processing and application logic |
| **Framework** | Streamlit | Web framework to build, layout, and serve the interactive dashboard |
| **Data** | Pandas | DataFrame manipulation, filtering, renaming, and CSV loading |
| **Compute** | NumPy | Numerical computation and synthetic demo data generation |
| **Visualisation** | Plotly Express | Interactive histograms, pie/donut charts, scatter plots, and box plots |
| **Data Source** | Kaggle ULB Dataset | 284K real credit card transactions with fraud labels |

---

## 📊 Dataset Details

| Metric | Value |
|---|---|
| Total Transactions | 284,807 |
| Fraud Cases | 492 |
| Fraud Rate | 0.17% |
| Feature Columns | 31 |

### Feature Descriptions

| Feature | Description |
|---|---|
| `Time` | Seconds elapsed since the first transaction in the dataset |
| `Amount` | Transaction value in USD |
| `V1 – V28` | PCA-transformed, anonymised features (identity protected) |
| `Class` / `Is_Fraud` | Target label — `0` = Normal Transaction, `1` = Fraudulent |
| `Card_ID` | Unique card identifier added in v2 for per-card investigation |

> **Demo Mode:** If no CSV is uploaded, the app auto-generates **5,000 synthetic transactions** with a ~2% fraud injection rate — fully functional out of the box.

---

## ✨ Features

### Core Dashboard (v1)

| # | Feature | Description |
|---|---|---|
| 01 | **CSV Upload & Demo Mode** | Upload `creditcard.csv` or run instantly on auto-generated synthetic data. `@st.cache_data` prevents re-loading on every interaction. |
| 02 | **Live KPI Metrics Row** | 4 real-time metric cards: Total Transactions, Fraud Count, Fraud Rate %, and Total Processed Value — updated dynamically per filter. |
| 03 | **Amount Distribution Chart** | Log-scale histogram overlaying Normal vs Fraud amounts. Red bars reveal high-value fraud concentration at the tail end of the distribution. |
| 04 | **Class Imbalance Pie Chart** | Donut chart exposing the 98:2 split between normal and fraud transactions — the fundamental challenge in real-world fraud ML modelling. |
| 05 | **Time vs Amount Scatter** | Interactive scatter mapping timing to amount. Hover tooltips let analysts inspect individual flagged events directly on the chart. |
| 06 | **Flagged Transactions Table** | Filtered, sortable table of all `Is_Fraud == 1` rows sorted by descending amount. Analyst-ready for instant fraud investigation. |

### Cardholder Investigation (v2)

| Feature | Description |
|---|---|
| **Card ID Lookup** | Sidebar dropdown to select any `Card_ID` and instantly view its stats. |
| **Per-Card Risk Badge** | `⚠️ HIGH RISK` or `✅ LOW RISK` label based on fraud activity on the card. |
| **Box-Plot Visualisation** | Amount range and outliers split by Normal vs Fraud — highlights high-value anomaly patterns clearly. |

### Card Perks & Features (v3)

| Feature | Description |
|---|---|
| **Card Tier** | Silver, Gold, Platinum, or Infinite Signature — seeded consistently per Card ID. |
| **Reward Points Multiplier** | 1×, 1.5×, 2×, 3×, or 5× — assigned per card and displayed in the perk panel. |
| **Air Miles** | 2,000–150,000 accumulated miles shown per selected card. |
| **Lounge Access** | None (Silver), 2/Year (Gold), Unlimited (Platinum & Infinite). |
| **Active Discounts** | 2–3 randomly seeded discounts from a pool of 6 offers, consistent per card. |

---

## 🖥️ Dashboard Walkthrough

```
┌─────────────────────────────────────────────────────────────────┐
│  🛡️ Banking Transaction Analysis & Fraud Pattern Detection      │
├──────────────┬──────────────────────────────────────────────────┤
│   SIDEBAR    │  KPI Row: [Total Txns] [Fraud Count] [Rate] [$]  │
│              ├──────────────────────────────────────────────────┤
│  Upload CSV  │  Card Details Panel    │  Box Plot (Fraud Amt)   │
│  Card Lookup ├──────────────────────────────────────────────────┤
│  Amt Filter  │  Histogram (log-scale) │  Donut Chart            │
│              ├──────────────────────────────────────────────────┤
│              │  Scatter Plot (Time vs Amount)                   │
│              ├──────────────────────────────────────────────────┤
│              │  Flagged Transactions Table (sorted by Amount)   │
└──────────────┴──────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

```
1. Upload / Generate
   └── User uploads Kaggle CSV OR app auto-generates 5,000 synthetic
       transactions with 2% fraud injection via NumPy random seeding.

2. Cache & Clean
   └── @st.cache_data stores the DataFrame. 'Class' column renamed to
       'Is_Fraud'. Card_ID assigned per transaction.

3. Filter & Slice
   └── Sidebar Amount slider filters the DataFrame. All charts, KPI
       metrics, and the flagged table update dynamically in real time.

4. Visualise & Explore
   └── Plotly renders interactive charts highlighting Normal (green/blue)
       vs Fraud (red) with hover, zoom, and pan controls.

5. Inspect Flagged Rows
   └── st.dataframe shows only Is_Fraud == 1 rows, sorted by Amount
       descending — enabling immediate analyst-level investigation.
```

---

## 🪪 Cardholder Investigation (v2)

The sidebar **Cardholder Investigation** panel allows selecting any `Card_ID` to drill into:

- **Total Swipes** — total number of transactions on the card
- **Fraudulent Activity count** — number of flagged transactions
- **Average Transaction Amount** — mean spend per swipe
- **Risk Badge** — instant `HIGH RISK` / `LOW RISK` classification

> Real-world fraud investigation is card-specific. This panel mimics how bank analysts actually triage suspicious activity — by isolating a single card rather than scanning the full dataset.

---

## 🎁 Card Perks & Features (v3)

Each card has a consistent, seeded profile generated from its `Card_ID` digits:

```python
seed_str = re.sub(r'\D', '', str(selected_card))  # Extract digits from Card ID
seed_val = int(seed_str) if seed_str else 42
np.random.seed(seed_val)                           # Seed for consistency
```

This ensures the same card always displays the same tier, miles, points, and discounts across sessions. The seed is reset with `np.random.seed()` afterward to avoid side-effects on other charts.

### Discount Pool

| Discount | Offer |
|---|---|
| ☕ Starbucks | 10% off |
| 🛒 Groceries | 5% Cashback |
| ✈️ Flight Bookings | 15% off |
| 🛡️ Travel Insurance | Free |
| 🎮 Steam (AAA Titles) | 15% off |
| 🚆 IRCTC Bookings | 5% Cashback |

---

## 💻 Key Code Snippets

### 1. Data Loading & Caching

```python
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    else:
        # Auto-generate 5,000 synthetic transactions with ~2% fraud rate
        np.random.seed(42)
        n_samples = 5000
        ...
        return pd.DataFrame(data)
```

> `@st.cache_data` prevents the data from reloading on every UI interaction, keeping the dashboard responsive.

### 2. Sidebar Filter Logic

```python
amount_filter = st.sidebar.slider("Minimum Transaction Amount ($)", 
                                   int(df['Amount'].min()), 
                                   int(df['Amount'].max()), 0)
filtered_df = df[df['Amount'] >= amount_filter]
```

> Reactive — all 4 charts, KPI metrics, and the flagged table update live.

### 3. Histogram — Normal vs Fraud (log scale)

```python
fig_hist = px.histogram(
    filtered_df, x="Amount", color="Is_Fraud",
    nbins=50, log_y=True,
    color_discrete_map={0: '#00cc96', 1: '#ef553b'}
)
fig_hist.update_layout(barmode='overlay')
fig_hist.update_traces(opacity=0.75)
```

> `log_y=True` is critical — fraud is ~100× rarer than normal transactions, so a linear Y-axis makes fraud bars invisible.

### 4. Box Plot — Fraud Amount Analysis

```python
fig_fraud_val = px.box(
    filtered_df, x="Is_Fraud", y="Amount",
    color="Is_Fraud", points="all",
    color_discrete_map={0: '#00cc96', 1: '#ef553b'}
)
```

> Reveals the high-value outlier pattern in fraudulent transactions clearly — far more informative than a histogram alone.

### 5. Scatter — Time vs Amount

```python
fig_scatter = px.scatter(
    filtered_df, x="Time", y="Amount",
    color="Is_Fraud", opacity=0.6,
    color_discrete_map={0: '#636efa', 1: '#ef553b'}
)
```

### 6. Donut — Class Balance

```python
fig_pie = px.pie(
    values=[total_transactions - fraud_transactions, fraud_transactions],
    names=['Normal (0)', 'Fraud (1)'],
    hole=0.4,
    color_discrete_sequence=['#00cc96', '#ef553b']
)
```

### 7. KPI Metrics Row

```python
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{total_transactions:,}")
col2.metric("Fraudulent Transactions", f"{fraud_transactions:,}", 
            "Flagged", delta_color="inverse")
col3.metric("Fraud Rate", f"{fraud_percentage:.2f}%")
col4.metric("Total Processed Value", f"${total_value:,.2f}")
```

---

## ⚠️ Challenges & Learnings

### Challenges Faced

| # | Challenge |
|---|---|
| 1 | Extreme class imbalance (0.17% fraud) made visual analysis tricky without a log-scale Y-axis |
| 2 | NumPy array mutation bug when injecting fraud amounts into dict-based synthetic data |
| 3 | Plotly color maps required string keys (`'0'`, `'1'`) rather than integer keys for `Is_Fraud` |
| 4 | A stray character at the end of the file caused a silent syntax error crashing the whole app |
| 5 | `@st.cache_data` needed careful state handling for Streamlit file uploader input changes |

### Key Learnings

| # | Learning |
|---|---|
| 1 | Building production-grade data pipelines with Pandas and NumPy for real fraud datasets |
| 2 | Creating multi-chart dashboards with Streamlit layout columns and sidebar filter controls |
| 3 | Understanding class imbalance — a core challenge in real-world fraud and anomaly detection |
| 4 | Data type consistency between processing code and visualisation libraries is critical |
| 5 | Agile team debugging: identifying and fixing issues collaboratively in a shared codebase |

---

## 🚀 Installation & Running

### Prerequisites

```bash
pip install streamlit pandas numpy plotly
```

### Run the App

```bash
streamlit run newproz3.py
```

The dashboard will open at `http://localhost:8501` in your browser.

### Using Your Own Data

1. Download the [Kaggle ULB Credit Card Fraud dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
2. Upload `creditcard.csv` via the sidebar file uploader
3. All charts and metrics will update automatically

> If no file is uploaded, the app runs on 5,000 auto-generated synthetic transactions with ~2% fraud rate — no setup needed.

---

## 🔭 Future Scope

| Tag | Feature | Description |
|---|---|---|
| **ML** | ML Model Integration | Plug in Isolation Forest, Random Forest, or XGBoost to auto-flag transactions with confidence scores |
| **RT** | Real-Time Streaming | Connect to live transaction APIs using Kafka + Streamlit auto-rerun for live fraud alerting |
| **XP** | Advanced Analytics | Add SHAP explainability charts, confusion matrices, ROC curves, and feature importance plots |
| **AL** | Alert System | Email / SMS notifications via Twilio or SendGrid when high-confidence fraud is detected |

---

## 📌 Version History

| Version | Changes |
|---|---|
| **v1** | Core dashboard — histogram, pie chart, scatter plot, KPI metrics, flagged table, CSV upload & demo mode |
| **v2** | Added `Card_ID` feature, sidebar cardholder investigation panel, per-card risk badge, and box-plot visualisation |
| **v3** | Added card perks panel — tier, reward points multiplier, air miles, lounge access, and live seeded discounts |

---

## 👨‍💻 Team

| Name | Role |
|---|---|
| A.C. Pravin Kumar | Lead Developer |
| Raja | Developer |
| Sham | Developer |
| Perarasu | Developer |
| Vignesh | Developer |
| Tamil | Developer |
| Niranjan Kumar | Developer |

**Institution:** KPRIET — B.E CSE (AIML-B)

---

*Built with ❤️ using Streamlit, Pandas, NumPy, and Plotly.*
