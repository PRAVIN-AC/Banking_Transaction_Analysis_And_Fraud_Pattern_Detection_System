import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR BETTER UI ---
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    h1, h2, h3 {color: #fafafa;}
    .stMetric {background-color: #262730; padding: 15px; border-radius: 10px;}
    .perk-box {background-color: #1e2129; padding: 10px; border-radius: 8px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    else:
        # Generate dummy data if no file is uploaded
        np.random.seed(42)
        n_samples = 5000
        card_ids = [f"CARD-{np.random.randint(1000, 9999)}" for _ in range(20)]
        
        # Explicitly make 10 cards completely clean, and 10 cards compromised
        clean_cards = set(card_ids[:10])
        
        assigned_cards = np.random.choice(card_ids, size=n_samples)
        classes = np.zeros(n_samples, dtype=int)
        
        for i in range(n_samples):
            if assigned_cards[i] not in clean_cards:
                # 4% fraud rate on the compromised cards to maintain overall ~2% average
                if np.random.rand() < 0.04:
                    classes[i] = 1
        
        data = {
            'Card_ID': assigned_cards, 
            'Time': np.random.randint(0, 100000, n_samples),
            'Amount': np.random.exponential(scale=50, size=n_samples),
            'Class': classes 
        }
        
        fraud_indices = np.where(data['Class'] == 1)[0]
        data['Amount'][fraud_indices] = data['Amount'][fraud_indices] * 10
        return pd.DataFrame(data)

# Load data
uploaded_file = st.sidebar.file_uploader("Upload Transaction Data (CSV)", type="csv")
df = load_data(uploaded_file)

# Standardize column names
if 'Class' in df.columns:
    df.rename(columns={'Class': 'Is_Fraud'}, inplace=True)

# --- SIDEBAR UI ---
st.sidebar.title("🛡️ System Controls")
st.sidebar.markdown("Upload the Kaggle `creditcard.csv` dataset to begin.")

# --- NEW SUGGESTION: Particular Credit Card Lookup ---
st.sidebar.markdown("---")
st.sidebar.subheader("📇 Cardholder Investigation")
if 'Card_ID' in df.columns:
    unique_cards = df['Card_ID'].unique()
    selected_card = st.sidebar.selectbox("Select a Specific Card ID", unique_cards)
    card_data = df[df['Card_ID'] == selected_card]
else:
    st.sidebar.info("Upload data with 'Card_ID' to enable card-specific lookup.")
    card_data = df # Fallback

st.sidebar.markdown("---")
st.sidebar.subheader("Filter Data")
amount_filter = st.sidebar.slider("Minimum Transaction Amount ($)", int(df['Amount'].min()), int(df['Amount'].max()), 0)

# Apply filters
filtered_df = df[df['Amount'] >= amount_filter]

# --- MAIN DASHBOARD UI ---
st.title("Banking Transaction Analysis & Fraud Pattern Detection System")
st.markdown("Developed by: A.C.Pravin Kumar | RAJA | SHAM | PERARASU | VIGNESH | TAMIL | NIRANJAN KUMAR")
st.markdown("---")

# --- TOP METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)
total_transactions = len(filtered_df)
fraud_transactions = len(filtered_df[filtered_df['Is_Fraud'] == 1])
fraud_percentage = (fraud_transactions / total_transactions) * 100 if total_transactions > 0 else 0
total_value = filtered_df['Amount'].sum()

col1.metric("Total Transactions", f"{total_transactions:,}")
col2.metric("Fraudulent Transactions", f"{fraud_transactions:,}", "Flagged", delta_color="inverse")
col3.metric("Fraud Rate", f"{fraud_percentage:.2f}%")
col4.metric("Total Processed Value", f"${total_value:,.2f}")

st.markdown("---")

# --- NEW SUGGESTION: Detailed Card Info & Fraud Amount Graph ---
col_card, col_fraud_val = st.columns([1, 2])

with col_card:
    st.subheader(f"Details for {selected_card if 'Card_ID' in df.columns else 'Dataset'}")
    c_total = len(card_data)
    c_fraud = len(card_data[card_data['Is_Fraud'] == 1])
    st.write(f"**Total Swipes:** {c_total}")
    st.write(f"**Fraudulent Activity:** {c_fraud}")
    st.write(f"**Average Transaction:** ${card_data['Amount'].mean():.2f}")
    if c_fraud > 0:
        st.error("⚠️ HIGH RISK: This card has flagged transactions.")
    else:
        st.success("✅ LOW RISK: No fraud detected for this card.")

    # --- ADDED: CREDIT CARD FEATURES & PERKS (ALIGNED) ---
    if 'Card_ID' in df.columns and selected_card:
        st.markdown("---")
        st.markdown("#### 🎁 Card Perks & Features")
        
        # Use the numbers in the Card ID as a seed so the perks stay consistent for each card
        seed_str = re.sub(r'\D', '', str(selected_card))
        seed_val = int(seed_str) if seed_str else 42
        np.random.seed(seed_val)
        
        tier = np.random.choice(['Silver', 'Gold', 'Platinum', 'Infinite Signature'])
        multiplier = np.random.choice([1.0, 1.5, 2.0, 3.0, 5.0])
        miles = np.random.randint(2000, 150000)
        lounge = "Unlimited" if tier in ['Platinum', 'Infinite Signature'] else ("2/Year" if tier == 'Gold' else "None")
        
        # Aligning the core stats in two neat columns
        perk_col1, perk_col2 = st.columns(2)
        with perk_col1:
            st.markdown(f"<div class='perk-box'><b>💳 Tier:</b><br>{tier}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='perk-box'><b>✈️ Miles:</b><br>{miles:,}</div>", unsafe_allow_html=True)
        with perk_col2:
            st.markdown(f"<div class='perk-box'><b>🎯 Points:</b><br>{multiplier}x</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='perk-box'><b>🛋️ Lounge:</b><br>{lounge}</div>", unsafe_allow_html=True)
        
        st.markdown("**Active Discounts:**")
        possible_discounts = [
            "☕ 10% off at Starbucks", 
            "🛒 5% Cashback on Groceries", 
            "✈️ 15% off Flight Bookings", 
            "🛡️ Free Travel Insurance", 
            "🎮 15% off Steam (AAA Titles)",
            "🚆 5% Cashback on IRCTC Bookings"
        ]
        # Pick 2 or 3 random discounts
        selected_discounts = np.random.choice(possible_discounts, size=np.random.randint(2, 4), replace=False)
        for d in selected_discounts:
            st.markdown(f"- {d}")
            
        # Reset seed so it doesn't affect other random operations in the app
        np.random.seed()
    # ------------------------------------------

with col_fraud_val:
    st.subheader("Analysis of Fraudulent Amounts")
    # Histogram specifically for the value of fraud vs legitimate to see impact
    fig_fraud_val = px.box(
        filtered_df, 
        x="Is_Fraud", 
        y="Amount", 
        color="Is_Fraud",
        points="all",
        title="Range & Outliers of Fraudulent Amounts",
        color_discrete_map={0: '#00cc96', 1: '#ef553b'}
    )
    st.plotly_chart(fig_fraud_val, use_container_width=True)

st.markdown("---")

# --- VISUALIZATIONS ROW 1 ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Transaction Amount Distribution")
    fig_hist = px.histogram(
        filtered_df, 
        x="Amount", 
        color="Is_Fraud", 
        nbins=50,
        color_discrete_map={0: '#00cc96', 1: '#ef553b'},
        title="Volume by Amount (Normal vs Fraud)",
        log_y=True 
    )
    fig_hist.update_layout(barmode='overlay')
    fig_hist.update_traces(opacity=0.75)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    st.subheader("Fraud Class Balance")
    fig_pie = px.pie(
        values=[total_transactions - fraud_transactions, fraud_transactions], 
        names=['Normal (0)', 'Fraud (1)'],
        hole=0.4,
        color_discrete_sequence=['#00cc96', '#ef553b']
    )
    fig_pie.update_layout(title_text="Dataset Class Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- VISUALIZATIONS ROW 2 ---
st.subheader("Time Series: Amount vs. Time of Transaction")
fig_scatter = px.scatter(
    filtered_df, 
    x="Time", 
    y="Amount", 
    color="Is_Fraud",
    color_discrete_map={0: '#636efa', 1: '#ef553b'},
    opacity=0.6,
    hover_data=['Amount', 'Time']
)
fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Amount ($)", xaxis_title="Time (Seconds from start)")
st.plotly_chart(fig_scatter, use_container_width=True)

# --- DATA TABLE ---
st.markdown("---")
st.subheader("Raw Flagged Transactions")
st.dataframe(filtered_df[filtered_df['Is_Fraud'] == 1].sort_values(by='Amount', ascending=False), use_container_width=True)