import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Intelligent Customer Service",
    page_icon="🏦",
    layout="wide"
)

# =========================
# BANKING PROFESSIONAL THEME
# =========================

st.markdown("""
<style>
/* Main background and typography */
.stApp {
    background: #F3F6FB;
    color: #172B4D;
    font-family: "Inter", "Segoe UI", sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(243, 246, 251, 0.95);
}

[data-testid="stMainBlockContainer"] {
    max-width: 1440px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main title */
h1 {
    color: #102744 !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px;
}

h2, h3 {
    color: #173D67 !important;
    font-weight: 700 !important;
}

/* Section dividers */
hr {
    border: none;
    height: 1px;
    background: #D9E3F0;
    margin-top: 1.8rem;
    margin-bottom: 1.8rem;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E0E8F2;
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 3px 12px rgba(16, 39, 68, 0.045);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #102744 !important;
    font-weight: 800 !important;
}

/* Data tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #FFFFFF;
    border: 1px solid #DCE5F0;
    border-radius: 12px;
    overflow: hidden;
}

/* Inputs and dropdowns */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #FFFFFF;
    border-color: #CFDAE8;
    border-radius: 9px;
}

div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within {
    border-color: #3977B8;
    box-shadow: 0 0 0 1px #3977B8;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 9px;
    min-height: 42px;
    font-weight: 650;
    border: 1px solid #C9D8E9;
    transition: all 0.18s ease;
}

.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {
    background: #173D67;
    color: #FFFFFF;
    border-color: #173D67;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #3977B8;
    color: #173D67;
}

/* Information and status messages */
[data-testid="stAlert"] {
    border-radius: 10px;
    border: 1px solid #DCE5F0;
}

/* Text areas */
textarea {
    border-radius: 10px !important;
    border-color: #CFDAE8 !important;
    background: #FFFFFF !important;
    line-height: 1.6 !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #DCE5F0;
    border-radius: 11px;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    color: #173D67;
    font-weight: 600;
}

/* Charts and general containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #DCE5F0;
    border-radius: 12px;
}

/* Captions */
[data-testid="stCaptionContainer"] {
    color: #718096;
}

/* Responsive spacing */
@media (max-width: 768px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1rem 1rem 2rem;
    }

    h1 {
        font-size: 1.7rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("""
<div style="
    background: linear-gradient(120deg, #102744 0%, #1C4B78 100%);
    padding: 30px 32px;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(16,39,68,0.12);
">
    <div style="
        color: #B9D8F7;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 10px;
    ">
        BANKING OPERATIONS PLATFORM
    </div>
    <div style="
        color: white;
        font-size: 30px;
        font-weight: 800;
        line-height: 1.3;
    ">
        🏦 Intelligent Customer Service
    </div>
    <div style="
        color: #D8E6F5;
        font-size: 15px;
        margin-top: 10px;
    ">
        AI-supported customer service operations & management
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_excel(filename):
    file_path = BASE_DIR / filename
    if not file_path.exists():
        st.error(f"Không tìm thấy file: {file_path}")
        st.stop()
    return pd.read_excel(file_path)

df = load_excel("tickets.xlsx")
analysis_df = load_excel("tickets_analyzed.xlsx")
routing_df = load_excel("test_routing.xlsx")
rag_df = load_excel("test_rag.xlsx")
classified_df = load_excel("Copy of classified_feedback.xlsx")

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

if "ticket_id" in analysis_df.columns and "ticket_id" in df.columns:
    analysis_match = analysis_df[
        analysis_df["ticket_id"].astype(str) == str(selected_ticket)
    ]

    if not analysis_match.empty:
        analysis_row = analysis_match.iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            for field in ["intent", "topic", "product", "amount", "channel"]:
                st.write(f"**{field.replace('_', ' ').title()}**")
                st.info(str(analysis_row.get(field, "N/A")))

        with col2:
            for field in [
                "transaction_time",
                "transaction_id",
                "sentiment",
                "missing_information"
            ]:
                st.write(f"**{field.replace('_', ' ').title()}**")
                st.info(str(analysis_row.get(field, "N/A")))

    else:
        st.warning("Không tìm thấy kết quả AI Analysis cho ticket này.")
else:
    st.warning("File AI Analysis chưa có cột ticket_id.")

# =========================
# PRIORITY & ROUTING
# =========================

st.divider()
st.subheader("🚦 Priority & Routing")

if not routing_df.empty:
    if "test_id" in routing_df.columns:
        test_options = routing_df["test_id"].dropna().astype(str).tolist()
        selected_test = st.selectbox(
            "Select Routing Test Case",
            test_options,
            key="routing_test_selector"
        )

        routing_match = routing_df[
            routing_df["test_id"].astype(str) == selected_test
        ]

        if not routing_match.empty:
            routing_row = routing_match.iloc[0]

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Expected Priority**")
                st.info(str(routing_row.get("expected_priority", "N/A")))

                st.write("**Actual Priority**")
                st.info(str(routing_row.get("actual_priority", "N/A")))

                st.write("**Urgency**")
                st.info(str(routing_row.get("urgency", "N/A")))

            with col2:
                st.write("**Expected Department**")
                st.info(str(routing_row.get("expected_department", "N/A")))

                st.write("**Actual Department**")
                st.info(str(routing_row.get("actual_department", "N/A")))

                st.write("**Routing Reason**")
                st.info(str(routing_row.get("routing_reason", "N/A")))

    st.markdown("### 📋 Routing Test Results")
    st.dataframe(routing_df, use_container_width=True, hide_index=True)

    if "both_correct" in routing_df.columns:
        correct_count = (
            routing_df["both_correct"].astype(str).str.lower()
            .isin(["true", "1", "yes"])
        ).sum()
        st.metric("Test Cases with Correct Priority and Department",
                  f"{correct_count}/{len(routing_df)}")
else:
    st.warning("File test_routing.xlsx không có dữ liệu.")

# =========================
# KNOWLEDGE BASE & RESPONSE
# =========================

st.divider()
st.subheader("📚 Knowledge Base & RAG")

if not rag_df.empty:
    if "test_id" in rag_df.columns:
        rag_options = rag_df["test_id"].dropna().astype(str).tolist()

        selected_rag_test = st.selectbox(
            "Select RAG Test Case",
            rag_options,
            key="rag_test_selector"
        )

        rag_match = rag_df[
            rag_df["test_id"].astype(str) == selected_rag_test
        ]

        if not rag_match.empty:
            rag_row = rag_match.iloc[0]

            st.markdown("### 💬 Customer Message")
            st.write(rag_row.get("customer_message", "N/A"))

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Knowledge Base Found**")
                st.info(str(rag_row.get("actual_kb_found", "N/A")))

                st.write("**Source**")
                st.info(str(rag_row.get("actual_source", "N/A")))

                st.write("**Confidence**")
                st.info(str(rag_row.get("actual_confidence", "N/A")))

            with col2:
                st.write("**Reason**")
                st.info(str(rag_row.get("actual_reason", "N/A")))

                st.write("**Expected FAQ Source**")
                st.info(str(rag_row.get("expected_faq_source", "N/A")))

                st.write("**Test Result**")
                result = str(rag_row.get("test_result", "N/A"))
                if result.upper() == "PASS":
                    st.success(result)
                elif result.upper() == "FAIL":
                    st.error(result)
                else:
                    st.info(result)

            st.markdown("### 📝 Draft Response")
            st.text_area(
                "AI-generated draft",
                value=str(rag_row.get("actual_draft_response", "")),
                height=150,
                disabled=True,
                key="rag_draft_response"
            )

    st.markdown("### 📋 All RAG Test Results")
    st.dataframe(rag_df, use_container_width=True, hide_index=True)
else:
    st.warning("File test_rag.xlsx không có dữ liệu.")

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
    if col not in classified_df.columns
]

if missing_columns:
    st.warning(
        "The Excel file is missing these columns: "
        + ", ".join(missing_columns)
    )
else:
    # Dùng dữ liệu đúng từ classified_feedback.xlsx
    df_classified = classified_df.copy()

    # Tiếp tục phần bộ lọc Topic, Sentiment, Urgency

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
