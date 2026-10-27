from pathlib import Path
from io import BytesIO
import pandas as pd
import streamlit as st
import plotly.express as px

# =========================================================
# APP CONFIG
# =========================================================
st.set_page_config(
    page_title="Intelligent Customer Service",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
# Support both layouts:
#   project/app/dashboard/dashboard.py + project/data/*.xlsx
#   project/dashboard.py + project/data/*.xlsx
DATA_DIRS = [
    BASE_DIR,
    BASE_DIR / "data",
    BASE_DIR.parent / "data",
    BASE_DIR.parent.parent / "data",
]

FILES = {
    "tickets": ["tickets.xlsx", "tickets(3).xlsx"],
    "analysis": ["tickets_analyzed.xlsx", "classified_feedback.xlsx"],
    "routing": [
        "priority_routing_output.xlsx", "test_routing.xlsx",
        "test_routing (2).xlsx", "test_routing_results.xlsx",
    ],
    "rag": [
        "test_rag.xlsx", "test_rag (2).xlsx", "rag_results.xlsx",
        "rag_output.xlsx",
    ],
    "faq": [
        "faq.xlsx", "FAQ.xlsx", "faq_bank.xlsx", "knowledge_base.xlsx",
        "knowledge_base_output.xlsx",
    ],
    "classified": [
        "Copy of classified_feedback.xlsx",
        "classified_feedback.xlsx",
        "tickets_analyzed.xlsx",
    ],
    "management_report": ["management_summary.md"],
}

# =========================================================
# PROFESSIONAL BANKING THEME
# =========================================================
st.markdown(
    """
    <style>
    :root {
      --navy:#153451;
      --navy-2:#1D4D73;
      --blue:#2F6FB2;
      --pale:#EAF2FA;
      --page:#F4F7FB;
      --ink:#24364B;
      --muted:#6B7C90;
      --border:#DFE7F0;
      --white:#FFFFFF;
      --red:#C2413B;
      --green:#27845C;
      --amber:#B7791F;
    }
    .stApp { background:var(--page); color:var(--ink); }
    [data-testid="stMainBlockContainer"] {
      max-width:1500px; padding-top:1.2rem; padding-bottom:2.8rem;
    }
    [data-testid="stSidebar"] {
      background:#FFFFFF; border-right:1px solid var(--border);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
      color:var(--ink);
    }
    h1,h2,h3 { color:var(--navy)!important; letter-spacing:-.35px; }
    h1 { font-weight:800!important; }
    h2,h3 { font-weight:730!important; }
    p,li { line-height:1.55; }
    [data-testid="stMetric"] {
      background:#FFFFFF; border:1px solid var(--border);
      border-radius:14px; padding:16px 18px;
      box-shadow:0 2px 8px rgba(21,52,81,.035);
    }
    [data-testid="stMetricLabel"] {
      color:var(--muted)!important; font-weight:650!important;
    }
    [data-testid="stMetricValue"] {
      color:var(--navy)!important; font-weight:800!important;
    }
    div[data-baseweb="select"]>div,
    div[data-baseweb="input"]>div,
    div[data-baseweb="textarea"]>div {
      border-radius:9px; border-color:#D7E1ED; background:#FFFFFF;
    }
    .stButton>button {
      border-radius:9px; min-height:40px; font-weight:650;
      border:1px solid #D7E1ED;
    }
    .stButton>button[kind="primary"] {
      background:var(--navy); border-color:var(--navy); color:#FFFFFF;
    }
    [data-testid="stDataFrame"],[data-testid="stTable"] {
      border:1px solid var(--border); border-radius:11px;
      overflow:hidden; background:#FFFFFF;
    }
    [data-testid="stExpander"] {
      background:#FFFFFF; border:1px solid var(--border); border-radius:11px;
    }
    [data-testid="stAlert"] { border-radius:10px; }
    .hero {
      background:linear-gradient(120deg,#10263D 0%,#19466E 65%,#2B6597 100%);
      padding:25px 29px; border-radius:17px; margin-bottom:22px;
      box-shadow:0 8px 22px rgba(21,52,81,.10);
    }
    .hero-kicker {
      color:#BBD8F4; font-size:11px; font-weight:750; letter-spacing:1.8px;
    }
    .hero-title {
      color:#FFFFFF; font-size:28px; font-weight:820;
      margin-top:8px; line-height:1.3;
    }
    .hero-sub { color:#D8E6F5; font-size:14px; margin-top:8px; }
    .section-note {
      color:var(--muted); margin-top:-8px; margin-bottom:18px; font-size:14px;
    }
    .eyebrow {
      color:#6B7C90; font-size:11px; font-weight:750;
      letter-spacing:1.2px; text-transform:uppercase;
    }
    .status-pill {
      display:inline-block; padding:4px 9px; border-radius:18px;
      background:#EAF2FA; color:#244F7C; font-size:12px; font-weight:700;
    }
    .info-card {
      background:#FFFFFF; border:1px solid var(--border);
      border-radius:13px; padding:17px 18px; height:100%;
    }
    @media(max-width:700px) {
      [data-testid="stMainBlockContainer"] { padding:1rem .8rem 2rem; }
      .hero { padding:20px; }
      .hero-title { font-size:23px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# DATA HELPERS
# =========================================================
def find_file(candidates):
    for folder in DATA_DIRS:
        for name in candidates:
            path = folder / name
            if path.exists():
                return path
    return None


@st.cache_data(show_spinner=False)
def read_excel(path_string, modified_time):
    return pd.read_excel(path_string)


def normalize_column_names(frame):
    """Normalize header casing/spacing while preserving the original data."""
    if frame.empty:
        return frame
    result = frame.copy()
    result.columns = [
        str(column).replace("\ufeff", "").strip().lower().replace(" ", "_")
        for column in result.columns
    ]
    return result


def load_table(key):
    path = find_file(FILES[key])
    if path is None:
        return pd.DataFrame(), None
    try:
        frame = read_excel(str(path), path.stat().st_mtime)
        return normalize_column_names(frame), path
    except Exception as exc:
        st.warning(f"Không đọc được file {path.name}: {exc}")
        return pd.DataFrame(), path


tickets, tickets_path = load_table("tickets")
analysis, analysis_path = load_table("analysis")
routing, routing_path = load_table("routing")
rag, rag_path = load_table("rag")
faq, faq_path = load_table("faq")
classified, classified_path = load_table("classified")
management_report_path = find_file(FILES["management_report"])

# If the raw ticket workbook is absent, use the most complete available
# classified/analysis workbook so the dashboard can still open for review.
if tickets.empty:
    fallback = classified if not classified.empty else analysis
    if not fallback.empty and "ticket_id" in fallback.columns:
        tickets = fallback.copy()
        tickets_path = classified_path if not classified.empty else analysis_path


def read_management_report(path):
    if path is None:
        return ""
    for encoding in ("utf-8", "utf-8-sig"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            pass
    return ""


management_report_text = read_management_report(management_report_path)


def norm_bool(series):
    return (
        series.astype(str).str.strip().str.lower()
        .isin(["true", "1", "yes", "urgent", "high", "khẩn cấp"])
    )


def col_series(frame, col, default=""):
    if col in frame.columns:
        return frame[col]
    return pd.Series([default] * len(frame), index=frame.index)


def safe_text(value, fallback="—"):
    try:
        if pd.isna(value) or str(value).strip() in ("", "nan", "None", "NaT"):
            return fallback
    except (TypeError, ValueError):
        pass
    return str(value)


def match_ticket(frame, ticket_id):
    if frame.empty or "ticket_id" not in frame.columns:
        return pd.DataFrame()
    return frame[frame["ticket_id"].astype(str) == str(ticket_id)]


def display_field(row, field, label=None):
    label = label or field.replace("_", " ").title()
    st.markdown(f"**{label}**")
    st.write(safe_text(row.get(field, "—")))


def normalize_sentiment(series):
    mapping = {
        "positive": "Positive",
        "pos": "Positive",
        "positive sentiment": "Positive",
        "tích cực": "Positive",
        "tich cuc": "Positive",
        "neutral": "Neutral",
        "neu": "Neutral",
        "neutral sentiment": "Neutral",
        "trung tính": "Neutral",
        "trung tinh": "Neutral",
        "negative": "Negative",
        "neg": "Negative",
        "negative sentiment": "Negative",
        "tiêu cực": "Negative",
        "tieu cuc": "Negative",
    }
    cleaned = series.fillna("").astype(str).str.strip().str.lower()
    return cleaned.map(mapping)


def valid_text_series(frame, field, invalid_values=None):
    invalid_values = invalid_values or {"", "nan", "none", "unknown"}
    values = (
        col_series(frame, field, "")
        .fillna("")
        .astype(str)
        .str.strip()
    )
    return values[~values.str.lower().isin(invalid_values)]


def build_ticket_view(base, *sources):
    """Enrich original ticket rows by ticket_id without duplicating ticket rows."""
    if base.empty or "ticket_id" not in base.columns:
        return base.copy()
    result = base.copy()
    result["ticket_id"] = result["ticket_id"].astype(str)

    for source in sources:
        if source.empty or "ticket_id" not in source.columns:
            continue
        extra = source.copy()
        extra["ticket_id"] = extra["ticket_id"].astype(str)
        extra = extra.drop_duplicates(subset=["ticket_id"], keep="first")
        extra = extra.set_index("ticket_id")

        for col in extra.columns:
            mapped = result["ticket_id"].map(extra[col])
            if col not in result.columns:
                result[col] = mapped
            else:
                blank = (
                    result[col].isna()
                    | result[col].astype(str).str.strip().isin(
                        ["", "nan", "None", "NaT"]
                    )
                )
                result.loc[blank, col] = mapped.loc[blank]
    return result


# Original ticket messages remain the source for customer wording.
# Classified data is preferred for analyzed fields.
def best_source_for(field):
    for frame in (classified, analysis, tickets):
        if not frame.empty and field in frame.columns and frame[field].notna().any():
            values = frame[field].astype(str).str.strip()
            if values.replace(
                {"": pd.NA, "nan": pd.NA, "None": pd.NA, "NaT": pd.NA}
            ).notna().any():
                return frame
    return tickets


ticket_view = build_ticket_view(tickets, analysis, classified)
metrics_source = classified if not classified.empty else (
    analysis if not analysis.empty else tickets
)
total = len(metrics_source) if not metrics_source.empty else len(tickets)

urgent_source = best_source_for("is_urgent")
urgent_mask_global = norm_bool(col_series(urgent_source, "is_urgent", "false"))
urgent_count = int(urgent_mask_global.sum())

category_source = best_source_for("category")
category_series = (
    col_series(category_source, "category", "")
    .fillna("").astype(str).str.strip()
)
complaint_count = int(
    category_series.str.lower().isin(
        ["complaint", "complaints", "khiếu nại", "khieu nai"]
    ).sum()
)
# Number of distinct category labels, not the number of complaint tickets.
valid_categories_global = category_series[
    ~category_series.str.lower().isin(["", "nan", "none", "unknown"])
]
category_count = int(valid_categories_global.nunique())

sentiment_source = best_source_for("sentiment")
sentiment_global = normalize_sentiment(
    col_series(sentiment_source, "sentiment", "")
)
negative_count = int((sentiment_global == "Negative").sum())

topic_source = best_source_for("topic")
topic_series_global = (
    col_series(topic_source, "topic", "")
    .fillna("").astype(str).str.strip()
)
valid_topics_global = topic_series_global[
    ~topic_series_global.str.lower().isin(["", "nan", "none", "unknown"])
]
topic_counts_global = valid_topics_global.value_counts()
top_topic = (
    topic_counts_global.index[0] if not topic_counts_global.empty else "N/A"
)
top_topic_count = (
    int(topic_counts_global.iloc[0]) if not topic_counts_global.empty else 0
)
top_topic_pct = (
    top_topic_count / len(valid_topics_global) * 100
    if len(valid_topics_global) else 0
)

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
if st.session_state.pop("_navigate_urgent_queue", False):
    st.session_state["page_navigation"] = "Ticket Management"
    st.session_state["ticket_urgent_only"] = True

with st.sidebar:
    st.markdown("## 🏦 Intelligent CS")
    st.caption("Customer Operations Workspace")
    st.divider()

    page = st.radio(
        "ĐIỀU HƯỚNG",
        [
            "Dashboard Overview",
            "Ticket Management",
            "AI Analysis & Review",
            "Management Analytics",
            "Classified Output",
        ],
        key="page_navigation",
    )

    st.divider()
    st.markdown("**DATA STATUS**")
    for label, frame, path in [
        ("Tickets", tickets, tickets_path),
        ("AI Analysis", analysis, analysis_path),
        ("Routing tests", routing, routing_path),
        ("RAG tests", rag, rag_path),
        ("FAQ Knowledge Base", faq, faq_path),
        ("Classified data", classified, classified_path),
    ]:
        if path:
            st.caption(f"● {label}: {len(frame):,} rows")
        else:
            st.caption(f"○ {label}: not found")

    st.caption(
        "Management report: "
        + ("available" if management_report_path else "not found")
    )

# =========================================================
# APP HEADER
# =========================================================
st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">CUSTOMER OPERATIONS WORKSPACE</div>
      <div class="hero-title">🏦 Intelligent Customer Service</div>
      <div class="hero-sub">
        AI-assisted ticket analysis, prioritization and customer feedback insights
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if tickets.empty:
    st.error(
        "Chưa tìm thấy dữ liệu ticket. Hãy đặt tickets.xlsx hoặc tickets(3).xlsx "
        "trong thư mục chứa dashboard.py hoặc thư mục data/."
    )
    st.stop()


def page_note(text):
    st.markdown(
        f'<div class="section-note">{text}</div>',
        unsafe_allow_html=True,
    )


def sort_ticket_ids(frame):
    result = frame.copy()
    if "ticket_id" in result.columns:
        result["_ticket_sort"] = pd.to_numeric(
            result["ticket_id"].astype(str).str.extract(r"(\d+)", expand=False),
            errors="coerce",
        )
        result = result.sort_values(
            "_ticket_sort", ascending=True, na_position="last"
        ).drop(columns=["_ticket_sort"])
    return result


# =========================================================
# PAGE 1: DASHBOARD OVERVIEW
# =========================================================
if page == "Dashboard Overview":
    st.title("Dashboard Overview")
    page_note(
        "Theo dõi nhanh khối lượng ticket, mức độ ưu tiên và các nhóm yêu cầu nổi bật."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("🎫 Total Tickets", f"{total:,}")
    c2.metric(
        "🚨 Urgent Tickets",
        f"{urgent_count:,}",
        f"{urgent_count / max(total, 1):.1%} of total",
    )
    c3.metric("🏷️ Categories", f"{category_count:,}", "Unique category groups")

    st.divider()
    st.markdown("### Ticket Distribution")
    st.caption("Phân bố theo danh mục và loại ticket để nhận diện nhóm công việc nổi bật.")

    chart_col1, chart_col2 = st.columns(2, gap="large")

    with chart_col1:
        with st.container(border=True):
            st.markdown("#### Tickets by Category")
            source = best_source_for("category")
            if "category" in source.columns:
                counts = (
                    valid_text_series(source, "category")
                    .value_counts().head(8).sort_values()
                    .rename_axis("Category").reset_index(name="Tickets")
                )
                if not counts.empty:
                    fig = px.bar(
                        counts, x="Tickets", y="Category",
                        orientation="h", text="Tickets",
                        color_discrete_sequence=["#2F6FB2"],
                    )
                    fig.update_layout(
                        height=320, margin=dict(l=8, r=25, t=10, b=25),
                        plot_bgcolor="white", paper_bgcolor="white",
                        xaxis_title="Number of tickets", yaxis_title="",
                        showlegend=False,
                    )
                    fig.update_traces(textposition="outside", cliponaxis=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Chưa có dữ liệu category hợp lệ.")
            else:
                st.info("Không tìm thấy cột category.")

    with chart_col2:
        with st.container(border=True):
            st.markdown("#### Tickets by Type")
            source = best_source_for("ticket_type")
            if "ticket_type" in source.columns:
                counts = (
                    valid_text_series(source, "ticket_type")
                    .value_counts().head(8).sort_values()
                    .rename_axis("Ticket Type").reset_index(name="Tickets")
                )
                if not counts.empty:
                    fig = px.bar(
                        counts, x="Tickets", y="Ticket Type",
                        orientation="h", text="Tickets",
                        color_discrete_sequence=["#5A8FC5"],
                    )
                    fig.update_layout(
                        height=320, margin=dict(l=8, r=25, t=10, b=25),
                        plot_bgcolor="white", paper_bgcolor="white",
                        xaxis_title="Number of tickets", yaxis_title="",
                        showlegend=False,
                    )
                    fig.update_traces(textposition="outside", cliponaxis=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Chưa có dữ liệu ticket_type hợp lệ.")
            else:
                st.info("Không tìm thấy cột ticket_type.")

    st.divider()
    st.markdown("### Ticket Management")
    st.caption("Xem nhanh danh sách ticket hoặc chuyển thẳng đến hàng đợi khẩn cấp.")

    shortcut_col, shortcut_note = st.columns([1, 3])
    with shortcut_col:
        if st.button(
            "🚨 Open Urgent Queue",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["_navigate_urgent_queue"] = True
            st.rerun()
    with shortcut_note:
        st.caption("Mở Ticket Management và tự động bật bộ lọc ticket khẩn cấp.")

    preview = sort_ticket_ids(ticket_view).reset_index(drop=True)
    if "is_urgent" in preview.columns:
        urgent_preview = preview.loc[norm_bool(preview["is_urgent"])].copy()
    else:
        urgent_preview = preview.iloc[0:0].copy()

    dashboard_filter = st.radio(
        "Display tickets",
        ["All tickets", "Urgent cases only"],
        horizontal=True,
        key="dashboard_ticket_filter",
    )
    display_df = (
        urgent_preview.copy()
        if dashboard_filter == "Urgent cases only"
        else preview.copy()
    )

    preferred = [
        "ticket_id", "created_at", "category", "ticket_type",
        "topic", "sentiment", "is_urgent",
    ]
    visible = [col for col in preferred if col in display_df.columns]

    st.caption(
        f"Showing {len(display_df):,} / {len(preview):,} tickets · "
        f"{len(urgent_preview):,} urgent"
    )
    st.dataframe(
        display_df[visible] if visible else display_df,
        use_container_width=True,
        hide_index=True,
        height=390,
    )


# =========================================================
# PAGE 2: TICKET MANAGEMENT
# =========================================================
elif page == "Ticket Management":
    st.title("Ticket Management")
    page_note("Tìm kiếm, lọc và xem nội dung ticket cùng thông tin cần thiết để xử lý.")

    search_col, cat_col, type_col, urgent_col = st.columns([2, 1, 1, 1])
    with search_col:
        query = st.text_input(
            "Search tickets",
            placeholder="Nhập mã ticket hoặc từ khóa trong nội dung...",
        )
    with cat_col:
        categories = sorted(
            valid_text_series(tickets, "category").unique().tolist()
        )
        category = st.selectbox("Category", ["All"] + categories)
    with type_col:
        types = sorted(
            valid_text_series(tickets, "ticket_type").unique().tolist()
        )
        ticket_type = st.selectbox("Ticket Type", ["All"] + types)
    with urgent_col:
        priority = st.selectbox("Priority", ["All", "Urgent only", "Non-urgent"])

    filtered = ticket_view.copy()
    if query.strip():
        message = col_series(filtered, "customer_message", "").astype(str)
        ids = col_series(filtered, "ticket_id", "").astype(str)
        filtered = filtered[
            message.str.contains(query, case=False, na=False)
            | ids.str.contains(query, case=False, na=False)
        ]
    if category != "All" and "category" in filtered.columns:
        filtered = filtered[filtered["category"].astype(str) == category]
    if ticket_type != "All" and "ticket_type" in filtered.columns:
        filtered = filtered[filtered["ticket_type"].astype(str) == ticket_type]
    if priority != "All" and "is_urgent" in filtered.columns:
        mask = norm_bool(filtered["is_urgent"])
        filtered = filtered[mask] if priority == "Urgent only" else filtered[~mask]

    if st.session_state.get("ticket_urgent_only", False):
        if "is_urgent" in filtered.columns:
            filtered = filtered[norm_bool(filtered["is_urgent"])]
        st.info("Urgent queue is active.")
    if st.button("Clear urgent shortcut"):
        st.session_state["ticket_urgent_only"] = False
        st.rerun()

    filtered = sort_ticket_ids(filtered)
    st.caption(f"Showing {len(filtered):,} / {len(ticket_view):,} tickets")

    cols = [
        c for c in [
            "ticket_id", "created_at", "category", "ticket_type",
            "topic", "sentiment", "is_urgent", "customer_message",
        ] if c in filtered.columns
    ]
    st.dataframe(
        filtered[cols] if cols else filtered,
        use_container_width=True,
        hide_index=True,
        height=320,
    )

    if "ticket_id" in filtered.columns and not filtered.empty:
        ids = filtered["ticket_id"].astype(str).tolist()
        default_id = st.session_state.get("selected_ticket_id", ids[0])
        if default_id not in ids:
            default_id = ids[0]
        selected_id = st.selectbox(
            "Select a ticket to view details",
            ids,
            index=ids.index(default_id),
            key="ticket_detail_selector",
        )
        st.session_state["selected_ticket_id"] = selected_id
        row = filtered[filtered["ticket_id"].astype(str) == selected_id].iloc[0]

        st.divider()
        st.subheader(f"Ticket Detail · {selected_id}")
        st.markdown("**Customer Message**")
        st.info(safe_text(row.get("customer_message", "Không có nội dung khách hàng.")))

        fields = ["category", "ticket_type", "topic", "sentiment", "is_urgent", "created_at"]
        present = [field for field in fields if field in row.index]
        field_cols = st.columns(min(3, max(1, len(present))))
        for i, field in enumerate(present):
            with field_cols[i % len(field_cols)]:
                display_field(row, field)
        # cluster_label intentionally stays in Classified Output, not Ticket Detail.
    else:
        st.warning("Không có ticket nào khớp với bộ lọc.")


# =========================================================
# PAGE 3: AI ANALYSIS & HUMAN REVIEW
# =========================================================
elif page == "AI Analysis & Review":
    st.title("AI Analysis & Review")
    page_note(
        "Kiểm tra phân tích AI, kết quả routing, kiến thức truy xuất và bản nháp "
        "trước khi nhân viên đưa ra quyết định."
    )

    if "ticket_id" not in tickets.columns:
        st.warning("File tickets cần có cột ticket_id.")
        st.stop()

    ticket_ids = tickets["ticket_id"].dropna().astype(str).tolist()
    if not ticket_ids:
        st.warning("Chưa có ticket để phân tích.")
        st.stop()

    current = st.session_state.get("selected_ticket_id", ticket_ids[0])
    if current not in ticket_ids:
        current = ticket_ids[0]

    selected = st.selectbox(
        "Select ticket to review",
        ticket_ids,
        index=ticket_ids.index(current),
        key="analysis_selected_ticket",
    )
    st.session_state["selected_ticket_id"] = selected

    ticket_row = tickets[tickets["ticket_id"].astype(str) == selected].iloc[0]

    st.markdown("### Customer Request")
    st.info(safe_text(ticket_row.get("customer_message", "No customer message available.")))

    analysis_rows = match_ticket(analysis, selected)
    arow = analysis_rows.iloc[0] if not analysis_rows.empty else pd.Series(dtype=object)

    st.divider()
    st.markdown("### AI Analysis")
    st.caption("Ý định, chủ đề, cảm xúc và thông tin được nhận diện trong yêu cầu.")

    if analysis_rows.empty:
        st.info("Không tìm thấy kết quả AI Analysis cho ticket này trong file phân tích.")
    else:
        fields = [
            "intent", "topic", "product", "amount", "channel",
            "transaction_time", "transaction_id", "sentiment",
            "missing_information", "note",
        ]
        existing = [field for field in fields if field in arow.index]
        cols = st.columns(3)
        for i, field in enumerate(existing):
            with cols[i % 3]:
                display_field(arow, field)

    st.divider()
    st.markdown("### Priority & Routing")
    st.caption("Kết quả kiểm thử định tuyến; test case không nhất thiết là ticket thực tế.")

    if routing.empty:
        st.info("Chưa có file routing test.")
    else:
        if "test_id" in routing.columns:
            test_ids = routing["test_id"].dropna().astype(str).drop_duplicates().tolist()
            if test_ids:
                chosen_test = st.selectbox(
                    "Routing test case", test_ids, key="routing_test_case"
                )
                rr = routing[routing["test_id"].astype(str) == chosen_test].iloc[0]
            else:
                rr = None
        else:
            rr = routing.iloc[0]

        if rr is not None:
            route_fields = [
                "expected_priority", "actual_priority", "urgency",
                "expected_department", "actual_department",
                "routing_reason", "both_correct",
            ]
            existing = [field for field in route_fields if field in rr.index]
            cols = st.columns(3)
            for i, field in enumerate(existing):
                with cols[i % 3]:
                    display_field(rr, field)

    st.divider()
    st.markdown("### Knowledge Base & AI Draft")
    st.caption("Tham khảo kiến thức truy xuất và rà soát nội dung AI đề xuất.")

    draft_default = ""
    full_faq_answer = ""
    original_ai_draft = ""
    chosen_faq_id = ""
    chosen_rag = "no_rag"
    rrow = None

    if rag.empty:
        st.info("Chưa có file RAG test.")
    else:
        if "test_id" in rag.columns:
            rag_ids = rag["test_id"].dropna().astype(str).drop_duplicates().tolist()
            if rag_ids:
                chosen_rag = st.selectbox("RAG test case", rag_ids, key="rag_test_case")
                rrow = rag[rag["test_id"].astype(str) == chosen_rag].iloc[0]
        else:
            rrow = rag.iloc[0]

    if rrow is not None:
        st.markdown("#### Retrieved Knowledge")
        kb_left, kb_right = st.columns(2)
        with kb_left:
            for field in ["actual_kb_found", "actual_source", "actual_confidence"]:
                if field in rrow.index:
                    display_field(rrow, field)
        with kb_right:
            for field in ["actual_reason", "expected_faq_source", "test_result"]:
                if field in rrow.index:
                    display_field(rrow, field)

        # Display the full FAQ only when the RAG result says knowledge was found.
        # Never present an expected FAQ as if it had actually been retrieved.
        kb_found_value = safe_text(rrow.get("actual_kb_found", "false"), "false").strip().lower()
        actual_kb_found = kb_found_value in {"true", "1", "yes", "y", "found"}
        source_value = safe_text(rrow.get("actual_source", ""), "")
        if not source_value or source_value in ("—", "N/A", "None", "nan"):
            source_value = safe_text(rrow.get("expected_faq_source", ""), "") if actual_kb_found else ""

        if not actual_kb_found:
            st.info(
                "RAG test này không tìm thấy FAQ thực tế. Hệ thống không hiển thị FAQ dự kiến "
                "như thể đó là nguồn đã truy xuất; trường hợp này cần chuyển nhân viên xem xét."
            )
        elif not faq.empty:
            faq_id_col = next((c for c in ["faq_id", "id"] if c in faq.columns), None)
            faq_source_col = next((c for c in ["source", "faq_id", "id"] if c in faq.columns), None)
            question_col = next((c for c in ["question", "faq_question", "title"] if c in faq.columns), None)
            answer_col = next((c for c in ["answer", "faq_answer", "content", "response"] if c in faq.columns), None)

            # Some RAG outputs contain source labels such as "FAQ01" or text around the ID.
            import re
            source_ids = re.findall(r"FAQ\s*[-_ ]?\d+", source_value, flags=re.IGNORECASE)
            source_ids = [re.sub(r"\s+", "", x).replace("-", "").replace("_", "").upper() for x in source_ids]
            faq_match = pd.DataFrame()
            if faq_id_col and source_ids:
                faq_keys = faq[faq_id_col].astype(str).str.strip().str.upper().str.replace(r"[-_ ]", "", regex=True)
                faq_match = faq[faq_keys.isin(source_ids)]
            elif faq_source_col and source_value:
                faq_match = faq[faq[faq_source_col].astype(str).str.strip().str.casefold() == source_value.strip().casefold()]

            if not faq_match.empty:
                st.markdown("#### Full FAQ Content")
                # Keep the original FAQ answer intact. Use it as the response default
                # so the full approved knowledge text is not lost in the shorter RAG draft.
                first_faq_row = faq_match.iloc[0]
                chosen_faq_id = safe_text(first_faq_row.get(faq_id_col, "FAQ"), "FAQ") if faq_id_col else "FAQ"
                if answer_col:
                    full_faq_answer = safe_text(first_faq_row.get(answer_col), "")
                for _, faq_row in faq_match.iterrows():
                    title = safe_text(faq_row.get(faq_id_col, "FAQ"), "FAQ") if faq_id_col else "FAQ"
                    with st.expander(f"{title} — xem nội dung đầy đủ", expanded=True):
                        if "category" in faq_row.index:
                            st.caption(f"Category: {safe_text(faq_row.get('category'))}")
                        if question_col:
                            st.markdown("**Câu hỏi trong FAQ**")
                            st.write(safe_text(faq_row.get(question_col), "Không có nội dung câu hỏi."))
                        if answer_col:
                            st.markdown("**Câu trả lời đầy đủ trong FAQ**")
                            st.text(safe_text(faq_row.get(answer_col), "Không có nội dung câu trả lời."))
                        if "last_updated" in faq_row.index:
                            st.caption(f"Cập nhật lần cuối: {safe_text(faq_row.get('last_updated'))}")
            else:
                st.info(
                    "Chưa tìm được bản FAQ đầy đủ tương ứng với source của test case này. "
                    "Hãy kiểm tra giá trị actual_source/expected_faq_source và cột faq_id trong faq.xlsx."
                )
        else:
            st.warning(
                "Ứng dụng chưa tìm thấy file faq.xlsx nên chỉ hiển thị được mã nguồn FAQ. "
                "Hãy đặt faq.xlsx cạnh dashboard.py hoặc trong thư mục data."
            )

        original_ai_draft = safe_text(rrow.get("actual_draft_response", ""), "")
        # Prefer the full answer from the matched FAQ as the editable response text.
        # Keep the shorter RAG-generated draft visible below for comparison.
        draft_default = full_faq_answer if full_faq_answer.strip() else original_ai_draft

    if original_ai_draft.strip() and full_faq_answer.strip() and original_ai_draft.strip() != full_faq_answer.strip():
        with st.expander("Xem bản nháp AI ban đầu để đối chiếu"):
            st.text(original_ai_draft)

    st.markdown("#### AI Response Draft")
    if full_faq_answer.strip():
        st.success(f"Đã nạp toàn bộ câu trả lời từ {chosen_faq_id} vào ô phản hồi. Bạn có thể chỉnh sửa trước khi duyệt.")
    draft_key = f"draft_{chosen_rag}"
    if draft_key not in st.session_state:
        st.session_state[draft_key] = draft_default
    edited_draft = st.text_area(
        "Review and edit the response before approval",
        key=draft_key,
        height=180,
        placeholder="Bản nháp phản hồi sẽ xuất hiện tại đây nếu có trong dữ liệu.",
    )
    st.caption(
        "Nếu RAG truy xuất được FAQ, ô phản hồi sẽ ưu tiên toàn bộ câu trả lời nguyên văn từ faq.xlsx; "
        "nếu không tìm được FAQ thì dùng bản nháp có sẵn trong file RAG. "
        "Ứng dụng chưa kết nối API gửi phản hồi và không tự động gửi cho khách hàng."
    )
    if full_faq_answer.strip():
        st.download_button(
            "⬇️ Tải câu trả lời FAQ đầy đủ (.txt)",
            data=full_faq_answer.encode("utf-8-sig"),
            file_name=f"{chosen_faq_id.replace(' ', '_')}_full_answer.txt",
            mime="text/plain",
            key=f"download_full_faq_{chosen_rag}",
        )

    # Keep the existing dashboard and add a complete, searchable FAQ reference.
    # This remains available even when the selected RAG test did not retrieve a FAQ.
    st.divider()
    st.markdown("### 📚 FAQ Library — Full Questions & Answers")
    st.caption(
        "Tra cứu nguyên văn nội dung trong faq.xlsx. Phần này chỉ hiển thị kiến thức "
        "đã có trong file FAQ; không tự bổ sung lãi suất, phí, tỷ giá hoặc chính sách ngoài KB."
    )

    if faq.empty:
        st.warning(
            "Chưa tìm thấy file faq.xlsx. Hãy đặt faq.xlsx trong thư mục data của dự án "
            "để hiển thị đầy đủ câu hỏi và câu trả lời."
        )
    else:
        faq_id_col = next((c for c in ["faq_id", "id"] if c in faq.columns), None)
        faq_category_col = next((c for c in ["category", "topic"] if c in faq.columns), None)
        faq_question_col = next((c for c in ["question", "faq_question", "title"] if c in faq.columns), None)
        faq_answer_col = next((c for c in ["answer", "faq_answer", "content", "response"] if c in faq.columns), None)
        faq_source_col = next((c for c in ["source", "reference"] if c in faq.columns), None)

        if faq_question_col is None or faq_answer_col is None:
            st.warning(
                "File FAQ chưa có đủ cột question và answer. "
                f"Các cột hiện có: {', '.join(map(str, faq.columns))}"
            )
        else:
            search_faq = st.text_input(
                "Tìm FAQ theo mã, chủ đề, câu hỏi hoặc câu trả lời",
                placeholder="Ví dụ: FAQ21, chuyển khoản, khóa thẻ...",
                key="faq_library_search",
            ).strip().casefold()
            faq_view = faq.copy()
            searchable_cols = [c for c in [faq_id_col, faq_category_col, faq_question_col, faq_answer_col, faq_source_col] if c]
            if search_faq:
                mask = faq_view[searchable_cols].fillna("").astype(str).apply(
                    lambda col: col.str.casefold().str.contains(search_faq, regex=False)
                ).any(axis=1)
                faq_view = faq_view[mask]

            st.caption(f"Hiển thị {len(faq_view)} / {len(faq)} FAQ")
            for idx, faq_item in faq_view.iterrows():
                faq_code = safe_text(faq_item.get(faq_id_col, f"FAQ {idx + 1}"), f"FAQ {idx + 1}") if faq_id_col else f"FAQ {idx + 1}"
                faq_question = safe_text(faq_item.get(faq_question_col), "Chưa có nội dung câu hỏi")
                with st.expander(f"{faq_code} — {faq_question}"):
                    if faq_category_col:
                        st.caption(f"Chủ đề: {safe_text(faq_item.get(faq_category_col))}")
                    st.markdown("**Câu hỏi**")
                    st.write(faq_question)
                    st.markdown("**Câu trả lời đầy đủ theo FAQ**")
                    st.text(safe_text(faq_item.get(faq_answer_col), "Chưa có nội dung câu trả lời"))
                    if faq_source_col:
                        st.caption(f"Nguồn: {safe_text(faq_item.get(faq_source_col))}")
                    if "last_updated" in faq_item.index:
                        st.caption(f"Cập nhật lần cuối: {safe_text(faq_item.get('last_updated'))}")

    st.divider()
    st.markdown("### Human Review")
    st.caption("Ghi chú quyết định và đánh dấu trạng thái duyệt.")

    status_key = f"review_status_{selected}"
    note_key = f"review_note_{selected}"
    st.session_state.setdefault(status_key, "Pending review")
    st.session_state.setdefault(note_key, "")

    st.markdown(f"**Current review status:** `{st.session_state[status_key]}`")
    st.text_area(
        "Reviewer note (optional)",
        key=note_key,
        placeholder="Ghi chú chỉnh sửa, lý do chuyển cấp hoặc thông tin cần xác minh...",
    )

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("✏️ Save as edited", key=f"save_edited_{selected}", use_container_width=True):
            st.session_state[status_key] = "Edited"
            st.rerun()
    with b2:
        if st.button("✅ Approve draft", key=f"approve_{selected}", type="primary", use_container_width=True):
            st.session_state[status_key] = "Approved"
            st.rerun()
    with b3:
        if st.button("⚠️ Escalate", key=f"escalate_{selected}", use_container_width=True):
            st.session_state[status_key] = "Escalated"
            st.rerun()

    st.caption(
        "Trạng thái review hiện được lưu trong session của ứng dụng. "
        "Muốn lưu lâu dài hoặc chia sẻ giữa nhiều nhân viên, cần kết nối database."
    )


# =========================================================
# PAGE 4: MANAGEMENT ANALYTICS
# =========================================================
elif page == "Management Analytics":
    st.title("Management Analytics")
    page_note(
        "Phân tích KPI, phân bố chủ đề, cảm xúc khách hàng và xu hướng khiếu nại "
        "để hỗ trợ theo dõi hoạt động."
    )

    # -- Scope & KPIs
    st.markdown("### 1. Scope & Key Performance Indicators")
    st.caption(
        f"Phạm vi thống kê: {len(metrics_source):,} bản ghi trong nguồn dữ liệu phân tích ưu tiên."
    )

    sentiment_frame = best_source_for("sentiment")
    sentiment_normalized = normalize_sentiment(
        col_series(sentiment_frame, "sentiment", "")
    )
    positive = int((sentiment_normalized == "Positive").sum())
    neutral = int((sentiment_normalized == "Neutral").sum())
    negative = int((sentiment_normalized == "Negative").sum())
    valid_sentiment_count = int(sentiment_normalized.notna().sum())

    positive_pct = positive / max(valid_sentiment_count, 1) * 100
    neutral_pct = neutral / max(valid_sentiment_count, 1) * 100
    negative_pct = negative / max(valid_sentiment_count, 1) * 100
    urgent_pct = urgent_count / max(len(urgent_source), 1) * 100

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Tickets", f"{total:,}")
    k2.metric("Urgent Tickets", f"{urgent_count:,}", f"{urgent_pct:.1f}% of source")
    k3.metric("Complaints", f"{complaint_count:,}")
    k4.metric("Categories", f"{category_count:,}", "Unique category groups")

    sentiment_cols = st.columns(3)
    sentiment_cols[0].metric("😊 Positive", f"{positive:,}", f"{positive_pct:.1f}%")
    sentiment_cols[1].metric("😐 Neutral", f"{neutral:,}", f"{neutral_pct:.1f}%")
    sentiment_cols[2].metric("😟 Negative", f"{negative:,}", f"{negative_pct:.1f}%")
    st.caption(
        f"Sentiment percentages use {valid_sentiment_count:,} records with recognized sentiment labels."
    )

    st.divider()

    # -- Topic distribution
    st.markdown("### 2. Topic Distribution")
    topic_frame = best_source_for("topic")
    topic_values = valid_text_series(topic_frame, "topic")
    topic_counts = topic_values.value_counts().head(10).sort_values()

    if not topic_counts.empty:
        topic_chart = (
            topic_counts.rename("Tickets")
            .rename_axis("Topic")
            .reset_index()
        )
        fig_topic = px.bar(
            topic_chart,
            x="Tickets",
            y="Topic",
            orientation="h",
            text="Tickets",
            color_discrete_sequence=["#2F6FB2"],
        )
        fig_topic.update_layout(
            height=360,
            margin=dict(l=8, r=28, t=15, b=25),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="Number of tickets",
            yaxis_title="",
            showlegend=False,
        )
        fig_topic.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_topic, use_container_width=True)
    else:
        st.info("Không tìm thấy dữ liệu topic hợp lệ.")

    st.divider()

    # -- Sentiment distribution
    st.markdown("### 3. Sentiment Distribution")
    if valid_sentiment_count:
        sentiment_chart = (
            sentiment_normalized.dropna()
            .value_counts()
            .reindex(["Positive", "Neutral", "Negative"], fill_value=0)
            .rename("Tickets")
            .rename_axis("Sentiment")
            .reset_index()
        )
        fig_sentiment = px.bar(
            sentiment_chart,
            x="Sentiment",
            y="Tickets",
            text="Tickets",
            color="Sentiment",
            category_orders={"Sentiment": ["Positive", "Neutral", "Negative"]},
            color_discrete_map={
                "Positive": "#27845C",
                "Neutral": "#8A9AAF",
                "Negative": "#C2413B",
            },
        )
        fig_sentiment.update_layout(
            height=330,
            margin=dict(l=8, r=15, t=15, b=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="",
            yaxis_title="Number of tickets",
            showlegend=False,
        )
        fig_sentiment.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_sentiment, use_container_width=True)
    else:
        st.info("Không có dữ liệu sentiment hợp lệ.")

    st.divider()

    # -- Ticket trend and spike detection
    st.markdown("### 4. Ticket Trend & Spike Detection")
    st.caption(
        "Xu hướng khiếu nại theo ngày. Spike Detection đánh dấu ngày vượt ngưỡng "
        "trung bình + 2 độ lệch chuẩn."
    )

    trend_source = best_source_for("category")
    if (
        "created_at" in trend_source.columns
        and "category" in trend_source.columns
    ):
        trend = trend_source.copy()
        trend["created_at"] = pd.to_datetime(trend["created_at"], errors="coerce")
        category_values = (
            trend["category"].fillna("").astype(str).str.strip().str.lower()
        )
        trend = trend[
            category_values.isin(
                {"complaint", "complaints", "khiếu nại", "khieu nai"}
            )
        ].dropna(subset=["created_at"])

        if not trend.empty:
            trend["Date"] = trend["created_at"].dt.normalize()
            daily = trend.groupby("Date").size().rename("Complaints").to_frame()

            st.line_chart(daily, height=300, color="#3575B5")
            st.caption(f"Total complaints in displayed period: {len(trend):,}")

            if len(daily) >= 3:
                daily_values = daily["Complaints"]
                baseline_mean = float(daily_values.mean())
                baseline_std = float(daily_values.std(ddof=0))
                spike_threshold = baseline_mean + 2 * baseline_std
                spike_days = daily_values[daily_values > spike_threshold]

                st.markdown("#### Spike Detection Results")
                st.caption(
                    f"Threshold = mean + 2 × standard deviation "
                    f"= {baseline_mean:.2f} + 2 × {baseline_std:.2f} "
                    f"= {spike_threshold:.2f} complaints/day."
                )

                if not spike_days.empty:
                    spike_df = spike_days.rename("Complaints").reset_index()
                    spike_df["Date"] = pd.to_datetime(
                        spike_df["Date"]
                    ).dt.strftime("%d/%m/%Y")
                    st.warning(
                        f"Phát hiện {len(spike_days)} ngày vượt ngưỡng thống kê. "
                        "Đây là tín hiệu cần kiểm tra, không phải kết luận chắc chắn "
                        "về nguyên nhân."
                    )
                    st.dataframe(
                        spike_df, use_container_width=True, hide_index=True
                    )
                else:
                    st.success(
                        "Không có ngày nào vượt ngưỡng theo quy tắc thống kê này."
                    )
            else:
                st.info(
                    "Cần ít nhất 3 ngày có dữ liệu khiếu nại để chạy Spike Detection."
                )
        else:
            st.info(
                "Không tìm thấy khiếu nại có ngày hợp lệ. "
                "Kiểm tra cột category và created_at."
            )
    else:
        st.info("Cần có hai cột created_at và category để phân tích xu hướng.")

    if management_report_text.strip():
        with st.expander("View management summary note"):
            st.markdown(management_report_text)


# =========================================================
# PAGE 5: CLASSIFIED OUTPUT
# =========================================================
elif page == "Classified Output":
    st.title("Classified Output")
    page_note(
        "Tra cứu và lọc dữ liệu đã phân loại để kiểm tra kết quả phân tích. "
        "Dữ liệu nhạy cảm chỉ nên được truy cập theo quyền được phép."
    )

    source = (
        classified.copy()
        if not classified.empty
        else (analysis.copy() if not analysis.empty else tickets.copy())
    )

    if source.empty:
        st.warning("Không có dữ liệu Classified Output để hiển thị.")
        st.stop()

    source = sort_ticket_ids(source)
    filter_fields = [
        field for field in ["topic", "sentiment", "urgency", "category", "is_urgent"]
        if field in source.columns
    ]

    if filter_fields:
        filter_cols = st.columns(min(len(filter_fields), 4))
        active_filters = {}
        for i, field in enumerate(filter_fields):
            options = ["All"] + sorted(
                source[field].dropna().astype(str).unique().tolist()
            )
            with filter_cols[i % len(filter_cols)]:
                active_filters[field] = st.selectbox(
                    f"Filter by {field.replace('_', ' ').title()}",
                    options,
                    key=f"classified_filter_{field}",
                )
    else:
        active_filters = {}

    filtered = source.copy()
    for field, value in active_filters.items():
        if value != "All":
            filtered = filtered[filtered[field].astype(str) == value]

    search = st.text_input(
        "Search within classified data",
        placeholder="Ticket ID, topic, keyword...",
    )
    if search.strip():
        search_mask = filtered.astype(str).apply(
            lambda column: column.str.contains(search, case=False, na=False)
        ).any(axis=1)
        filtered = filtered[search_mask]

    st.metric("Matching Records", f"{len(filtered):,}")
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        height=470,
    )
    st.caption(
        "Classified Output giữ nguyên các trường phân tích, bao gồm cluster_label "
        "nếu trường này tồn tại trong nguồn dữ liệu. File tải xuống chỉ chứa các dòng "
        "đang khớp với bộ lọc hiện tại. Hãy chia sẻ dữ liệu theo đúng quyền truy cập."
    )
    download_col1, download_col2 = st.columns(2)
    with download_col1:
        csv_bytes = filtered.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ Download CSV",
            data=csv_bytes,
            file_name="classified_output.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with download_col2:
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            filtered.to_excel(writer, index=False, sheet_name="Classified_Output")
        st.download_button(
            "⬇️ Download Excel",
            data=excel_buffer.getvalue(),
            file_name="classified_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption(
    "Intelligent Customer Service · Internal review workspace · "
    "AI suggestions require human review"
)
