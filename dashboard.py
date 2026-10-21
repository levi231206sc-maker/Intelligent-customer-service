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

# ============================================================
# MANAGEMENT SUMMARY — CUSTOMER FEEDBACK DASHBOARD
# Source: Existing management output
# ============================================================

import pandas as pd
import streamlit as st

st.divider()
st.header("📊 Management Summary — Customer Feedback Dashboard")

st.caption(
    "Phạm vi dữ liệu: 15/09/2026 – 05/10/2026 | "
    "Nguồn: Management output có sẵn"
)

# 1. SCOPE AND KPI
st.subheader("1. Scope and Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tickets", "100")
col2.metric("Urgent Tickets", "24", "24.0%")
col3.metric("Negative Sentiment", "47", "47.0%")
col4.metric("Top Topic", "general_inquiry", "19 tickets")

st.info(
    "Reporting period: 15/09/2026 – 05/10/2026. "
    "Các chỉ số được lấy từ management output có sẵn."
)

# 2. TOPIC DISTRIBUTION
st.subheader("2. Topic Distribution")

topic_data = pd.DataFrame({
    "Topic": [
        "general_inquiry",
        "complaint",
        "transfer",
        "card",
        "fraud",
        "loan",
        "account",
        "digital_banking"
    ],
    "Ticket Count": [19, 19, 16, 15, 12, 11, 4, 4],
    "Percentage": [19, 19, 16, 15, 12, 11, 4, 4]
})

topic_col, topic_chart_col = st.columns([1, 1.5])

with topic_col:
    st.dataframe(
        topic_data,
        use_container_width=True,
        hide_index=True
    )

with topic_chart_col:
    st.bar_chart(
        topic_data.set_index("Topic")[["Ticket Count"]],
        horizontal=True
    )

# 3. SENTIMENT DISTRIBUTION
st.subheader("3. Sentiment Distribution")

sentiment_data = pd.DataFrame({
    "Sentiment": ["neutral", "negative", "positive"],
    "Ticket Count": [50, 47, 3],
    "Percentage": ["50.0%", "47.0%", "3.0%"]
})

sentiment_cols = st.columns(3)

for i, row in sentiment_data.iterrows():
    sentiment_cols[i].metric(
        label=row["Sentiment"].capitalize(),
        value=int(row["Ticket Count"]),
        delta=row["Percentage"]
    )

st.bar_chart(
    sentiment_data.set_index("Sentiment")[["Ticket Count"]],
    horizontal=True
)

# 4. DAILY TREND AND SPIKE
st.subheader("4. Ticket Trend and Spike Detection")

avg_tickets_per_day = 4.76
spike_threshold = 8.66

trend_col1, trend_col2 = st.columns(2)

trend_col1.metric(
    "Average Tickets per Day",
    f"{avg_tickets_per_day:.2f}"
)

trend_col2.metric(
    "Spike Reference Threshold",
    f"{spike_threshold:.2f}"
)

spike_data = pd.DataFrame({
    "Date": ["02/10/2026", "03/10/2026"],
    "Ticket Count": [9, 10]
})

st.bar_chart(
    spike_data.set_index("Date")[["Ticket Count"]]
)

st.warning(
    "02/10/2026: 9 tickets; 03/10/2026: 10 tickets. "
    "Cả hai ngày vượt ngưỡng tham chiếu 8.66 tickets/day. "
    "Đây là tín hiệu cần điều tra, không phải bằng chứng về nguyên nhân."
)

st.caption(
    "Lưu ý: Biểu đồ trên chỉ thể hiện hai ngày spike được cung cấp. "
    "Chưa có dữ liệu từng ngày đầy đủ để vẽ toàn bộ chuỗi thời gian."
)

# 5. REPRESENTATIVE CUSTOMER FEEDBACK
st.subheader("5. Representative Complaints and Feedback")

feedback_data = [
    {
        "Ticket ID": "T001",
        "Topic": "card",
        "Customer Message": (
            "Mình làm mất ví, trong đó có thẻ ATM của ngân hàng. "
            "Mình cần khóa thẻ gấp."
        )
    },
    {
        "Ticket ID": "T003",
        "Topic": "transfer",
        "Customer Message": (
            "Mình lỡ nhập sai số tài khoản người nhận khi chuyển 2 triệu, "
            "tiền đã đi rồi. Giờ làm sao lấy lại được?"
        )
    },
    {
        "Ticket ID": "T004",
        "Topic": "transfer",
        "Customer Message": (
            "Mình bấm chuyển tiền nhưng chờ mãi không nhận được mã OTP "
            "qua tin nhắn."
        )
    }
]

for feedback in feedback_data:
    with st.expander(
        f'{feedback["Ticket ID"]} | {feedback["Topic"]}'
    ):
        st.write(feedback["Customer Message"])

# 6. ROOT-CAUSE HYPOTHESES
st.subheader("6. Root-Cause Hypotheses to Verify")

st.markdown("""
- **Transfer:** Kiểm tra trạng thái giao dịch, thời gian đối soát
  và thông tin người nhận. Đây là hướng điều tra, chưa phải kết luận.
- **Card/Fraud:** Rà soát quy trình khóa thẻ, xác minh danh tính
  và cảnh báo giao dịch. Không suy ra nguyên nhân chỉ từ topic.
- **Negative/Urgent tickets:** Đối chiếu nhật ký hệ thống và hồ sơ
  xử lý trước khi xác định nguyên nhân gốc rễ.
""")

# 7. METHODOLOGY AND LIMITATIONS
st.subheader("7. Methodology and Limitations")

with st.expander("View methodology and limitations"):
    st.markdown("""
    1. Topic và sentiment được lấy từ file phân tích có sẵn;
       không được dự đoán lại trong lần chạy này.
    2. Cluster được tính độc lập từ nội dung bằng TF-IDF ký tự
       và KMeans. Cluster phản ánh độ tương đồng văn bản,
       không tự động chứng minh các ticket có cùng nguyên nhân.
    3. Spike sử dụng quy tắc mean + 1.5 standard deviations
       trên toàn bộ ngày trong khoảng thời gian, bao gồm ngày
       không có ticket được tính là 0.
    4. Các ngày vượt ngưỡng là tín hiệu để điều tra,
       không phải bằng chứng nhân quả.
    5. Giả thuyết nguyên nhân cần được xác minh bằng log giao dịch
       và hồ sơ vận hành.
    """)
# ============================================================
# CLASSIFIED OUTPUT — FILTER AND VIEW TICKETS
# ============================================================

st.divider()
st.header("🗂️ Classified Output")

st.caption(
    "Filter tickets by topic, sentiment, and urgency."
)

# Check whether the required columns exist
required_columns = [
    "ticket_id",
    "topic",
    "sentiment",
    "urgency"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.warning(
        "The Excel file is missing these columns: "
        + ", ".join(missing_columns)
    )
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        topic_options = ["All"] + sorted(
            df["topic"].dropna().astype(str).unique().tolist()
        )
        selected_topic = st.selectbox(
            "Filter by Topic",
            topic_options,
            key="classified_topic"
        )

    with col2:
        sentiment_options = ["All"] + sorted(
            df["sentiment"].dropna().astype(str).unique().tolist()
        )
        selected_sentiment = st.selectbox(
            "Filter by Sentiment",
            sentiment_options,
            key="classified_sentiment"
        )

    with col3:
        urgency_options = ["All"] + sorted(
            df["urgency"].dropna().astype(str).unique().tolist()
        )
        selected_urgency = st.selectbox(
            "Filter by Urgency",
            urgency_options,
            key="classified_urgency"
        )

    classified_df = df.copy()

    if selected_topic != "All":
        classified_df = classified_df[
            classified_df["topic"].astype(str) == selected_topic
        ]

    if selected_sentiment != "All":
        classified_df = classified_df[
            classified_df["sentiment"].astype(str) == selected_sentiment
        ]

    if selected_urgency != "All":
        classified_df = classified_df[
            classified_df["urgency"].astype(str) == selected_urgency
        ]

    st.metric("Matching Tickets", len(classified_df))

    st.dataframe(
        classified_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "📥 Download Filtered Tickets (CSV)",
        data=classified_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="classified_tickets.csv",
        mime="text/csv"
    )
