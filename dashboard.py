import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Intelligent Customer Service",
    page_icon="🏦",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("🏦 Intelligent Customer Service Operations")
st.caption("AI-supported customer service operations dashboard")

# =========================
# LOAD DATA
# =========================

df = pd.read_excel("tickets.xlsx")

# =========================
# KPI
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tickets", len(df))

with col2:
    if "is_urgent" in df.columns:
        urgent_count = df["is_urgent"].astype(str).str.lower().isin(
            ["true", "1", "yes", "urgent"]
        ).sum()
    else:
        urgent_count = 0

    st.metric("Urgent Tickets", urgent_count)

with col3:
    if "category" in df.columns:
        category_count = df["category"].nunique()
    else:
        category_count = 0

    st.metric("Categories", category_count)

# =========================
# TICKET LIST
# =========================

st.divider()

st.subheader("🔎 Ticket Filters")

col1, col2 = st.columns(2)

with col1:
    if "category" in df.columns:
        category_options = ["All"] + sorted(
            df["category"].dropna().astype(str).unique().tolist()
        )
        selected_category = st.selectbox(
            "Filter by Category",
            category_options
        )
    else:
        selected_category = "All"

with col2:
    if "ticket_type" in df.columns:
        ticket_type_options = ["All"] + sorted(
            df["ticket_type"].dropna().astype(str).unique().tolist()
        )
        selected_ticket_type = st.selectbox(
            "Filter by Ticket Type",
            ticket_type_options
        )
    else:
        selected_ticket_type = "All"

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"].astype(str) == selected_category
    ]

if selected_ticket_type != "All":
    filtered_df = filtered_df[
        filtered_df["ticket_type"].astype(str) == selected_ticket_type
    ]

st.subheader("📋 Customer Ticket List")
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)
# =========================
# TICKET DETAIL
# =========================

st.divider()

st.subheader("🔎 Ticket Detail")

# Tạo danh sách ticket ID
ticket_ids = df["ticket_id"].astype(str).tolist()

selected_ticket = st.selectbox(
    "Select a ticket",
    ticket_ids
)

# Lấy ticket được chọn
selected_row = df[
    df["ticket_id"].astype(str) == selected_ticket
].iloc[0]

# =========================
# CUSTOMER MESSAGE
# =========================

st.markdown("### 💬 Customer Message")

st.info(selected_row["customer_message"])

# =========================
# BASIC INFORMATION
# =========================

st.markdown("### 📌 Ticket Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Ticket ID**")
    st.write(selected_row["ticket_id"])

with col2:
    st.write("**Category**")
    st.write(selected_row["category"])

with col3:
    st.write("**Ticket Type**")
    st.write(selected_row["ticket_type"])

# =========================
# URGENCY
# =========================

st.markdown("### 🚨 Urgency")

st.write(selected_row["is_urgent"])
# =========================
# AI ANALYSIS
# =========================

st.divider()

st.subheader("🤖 AI Analysis")

col1, col2 = st.columns(2)

with col1:
    st.write("**Intent**")
    st.info("Not processed yet")

    st.write("**Topic**")
    st.info("Not processed yet")

    st.write("**Product**")
    st.info("Not processed yet")

    st.write("**Amount**")
    st.info("Not processed yet")

    st.write("**Channel**")
    st.info("Not processed yet")

with col2:
    st.write("**Transaction Time**")
    st.info("Not processed yet")

    st.write("**Transaction ID**")
    st.info("Not processed yet")

    st.write("**Sentiment**")
    st.info("Not processed yet")

    st.write("**Missing Information**")
    st.info("Not processed yet")
# =========================
# PRIORITY & ROUTING
# =========================

st.divider()

st.subheader("🚦 Priority & Routing")

col1, col2 = st.columns(2)

with col1:
    st.write("**Urgency**")
    st.warning("Not processed yet")

    st.write("**Priority**")
    st.warning("Not processed yet")

with col2:
    st.write("**Department**")
    st.info("Not processed yet")

    st.write("**Routing Reason**")
    st.info("Not processed yet")
# =========================
# KNOWLEDGE BASE & RESPONSE
# =========================

st.divider()

st.subheader("📚 Knowledge Base")

col1, col2 = st.columns(2)

with col1:
    st.write("**KB Found**")
    st.info("Not processed yet")

    st.write("**Source**")
    st.info("Not processed yet")

with col2:
    st.write("**Confidence**")
    st.info("Not processed yet")

    st.write("**Reason**")
    st.info("Not processed yet")

st.markdown("### 📝 Draft Response")

st.text_area(
    "AI-generated draft",
    value="Not processed yet",
    height=150,
    disabled=True
)
# =========================
# HUMAN REVIEW
# =========================

st.divider()

st.subheader("👤 Human Review")

st.write("Review the AI-generated draft before taking action.")

col1, col2, col3 = st.columns(3)

with col1:
    edit_clicked = st.button("✏️ Edit", use_container_width=True)

with col2:
    approve_clicked = st.button("✅ Approve", use_container_width=True)

with col3:
    escalate_clicked = st.button("⚠️ Escalate", use_container_width=True)

if edit_clicked:
    st.info("Edit mode selected. Human review is required.")

if approve_clicked:
    st.success("Ticket approved by human reviewer.")

if escalate_clicked:
    st.warning("Ticket escalated for further review.")
# =========================
# MANAGEMENT DASHBOARD
# =========================

st.divider()

st.header("📊 Management Dashboard")

st.subheader("📌 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Tickets", len(df))

with col2:
    if "category" in df.columns:
        complaint_count = (
            df["category"]
            .astype(str)
            .str.lower()
            .eq("complaint")
            .sum()
        )
    else:
        complaint_count = 0

    st.metric("Complaints", complaint_count)

with col3:
    if "is_urgent" in df.columns:
        urgent_count = df["is_urgent"].astype(str).str.lower().isin(
            ["true", "1", "yes", "urgent"]
        ).sum()
    else:
        urgent_count = 0

    st.metric("Urgent Tickets", urgent_count)

with col4:
    if "category" in df.columns:
        top_category = df["category"].value_counts().index[0]
    else:
        top_category = "N/A"

    st.metric("Top Issue", top_category)


# =========================
# TOP ISSUES
# =========================

st.subheader("🔥 Top Issues")

if "category" in df.columns:
    category_counts = df["category"].value_counts()

    st.bar_chart(category_counts)


# =========================
# TICKET TYPE
# =========================

st.subheader("📋 Ticket Type Distribution")

if "ticket_type" in df.columns:
    ticket_type_counts = df["ticket_type"].value_counts()

    st.bar_chart(ticket_type_counts)
st.subheader("📈 Complaint Trend")

if "created_at" in df.columns and "category" in df.columns:
    trend_df = df.copy()

    trend_df["created_at"] = pd.to_datetime(
        trend_df["created_at"],
        errors="coerce"
    )

    trend_df = trend_df[
        trend_df["category"].astype(str).str.lower() == "complaint"
    ]

    trend_df = trend_df.dropna(subset=["created_at"])

    trend_df["date"] = trend_df["created_at"].dt.date

    complaint_trend = trend_df.groupby("date").size()

    st.line_chart(complaint_trend)

else:
    st.info("Complaint trend data is not available.")
