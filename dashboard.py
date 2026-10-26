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
DATA_DIRS = [BASE_DIR, BASE_DIR / "data", BASE_DIR.parent / "data"]

FILES = {
    "tickets": ["tickets.xlsx", "tickets(3).xlsx"],
    "analysis": ["tickets_analyzed.xlsx", "classified_feedback.xlsx"],
    "routing": ["test_routing.xlsx", "test_routing_results.xlsx"],
    "rag": ["test_rag.xlsx", "rag_results.xlsx"],
    "classified": ["Copy of classified_feedback.xlsx", "classified_feedback.xlsx", "tickets_analyzed.xlsx"],
    "management_report": ["management_summary.md"],
}

# =========================================================
# THEME
# =========================================================
st.markdown("""
<style>
:root {
  --navy:#153451; --blue:#2F6FB2; --pale:#EAF2FA;
  --page:#F5F7FB; --ink:#24364B; --muted:#6B7C90;
  --border:#E1E8F0; --white:#FFFFFF;
}
.stApp { background:var(--page); color:var(--ink); }
[data-testid="stMainBlockContainer"] { max-width:1500px; padding-top:1.5rem; padding-bottom:3rem; }
[data-testid="stSidebar"] { background:#fff; border-right:1px solid var(--border); }
h1,h2,h3 { color:var(--navy)!important; letter-spacing:-.3px; }
h1 { font-weight:800!important; }
h2,h3 { font-weight:720!important; }
p,li { line-height:1.6; }
[data-testid="stMetric"] {
  background:#fff; border:1px solid var(--border); border-radius:14px;
  padding:17px 19px; box-shadow:0 2px 8px rgba(21,52,81,.035);
}
[data-testid="stMetricLabel"] { color:var(--muted)!important; font-weight:650!important; }
[data-testid="stMetricValue"] { color:var(--navy)!important; font-weight:800!important; }
div[data-baseweb="select"]>div, div[data-baseweb="input"]>div {
  border-radius:9px; border-color:#D7E1ED; background:#fff;
}
.stButton>button,.stDownloadButton>button {
  border-radius:9px; min-height:40px; font-weight:650; border:1px solid #D7E1ED;
}
.stButton>button[kind="primary"],.stDownloadButton>button[kind="primary"] {
  background:var(--navy); border-color:var(--navy); color:#fff;
}
[data-testid="stDataFrame"],[data-testid="stTable"] {
  border:1px solid var(--border); border-radius:11px; overflow:hidden; background:#fff;
}
[data-testid="stExpander"] { background:#fff; border:1px solid var(--border); border-radius:11px; }
[data-testid="stAlert"] { border-radius:10px; }
.hero {
  background:linear-gradient(120deg,#10263D 0%,#19466E 65%,#2B6597 100%);
  padding:26px 30px; border-radius:17px; margin-bottom:22px;
  box-shadow:0 8px 22px rgba(21,52,81,.10);
}
.hero-kicker { color:#BBD8F4; font-size:11px; font-weight:750; letter-spacing:1.8px; }
.hero-title { color:white; font-size:28px; font-weight:820; margin-top:8px; line-height:1.3; }
.hero-sub { color:#D8E6F5; font-size:14px; margin-top:8px; }
.section-note { color:#6B7C90; margin-top:-8px; margin-bottom:18px; font-size:14px; }
.small-pill { display:inline-block; background:#EAF2FA; color:#244F7C; border-radius:20px; padding:4px 10px; font-size:12px; font-weight:700; }
@media(max-width:700px) {
 [data-testid="stMainBlockContainer"] { padding:1rem .8rem 2rem; }
 .hero { padding:20px; } .hero-title { font-size:23px; }
}
</style>
""", unsafe_allow_html=True)

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

def load_table(key):
    path = find_file(FILES[key])
    if not path:
        return pd.DataFrame(), None
    try:
        return read_excel(str(path), path.stat().st_mtime), path
    except Exception as exc:
        st.warning(f"Không đọc được file {path.name}: {exc}")
        return pd.DataFrame(), path

tickets, tickets_path = load_table("tickets")
analysis, analysis_path = load_table("analysis")
routing, routing_path = load_table("routing")
rag, rag_path = load_table("rag")
classified, classified_path = load_table("classified")
management_report_path = find_file(FILES["management_report"])

def read_management_report(path):
    if path is None:
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except Exception:
            return ""
    except Exception:
        return ""

management_report_text = read_management_report(management_report_path)

def norm_bool(series):
    return series.astype(str).str.strip().str.lower().isin(["true", "1", "yes", "urgent", "high", "khẩn cấp"])

def col_series(frame, col, default=""):
    if col in frame.columns:
        return frame[col]
    return pd.Series([default] * len(frame), index=frame.index)

def safe_text(value, fallback="—"):
    if pd.isna(value) or str(value).strip() in ("", "nan", "None"):
        return fallback
    return str(value)

def match_ticket(frame, ticket_id):
    if frame.empty or "ticket_id" not in frame.columns:
        return pd.DataFrame()
    return frame[frame["ticket_id"].astype(str) == str(ticket_id)]

def display_field(frame, row, field, label=None):
    label = label or field.replace("_", " ").title()
    st.markdown(f"**{label}**")
    st.write(safe_text(row.get(field, "—")))

def to_excel_bytes(frame):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        frame.to_excel(writer, index=False, sheet_name="Classified Output")
    return output.getvalue()

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
# Apply navigation requests before creating the sidebar radio widget.
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
        label_visibility="visible",
        key="page_navigation",
    )
    st.divider()
    st.caption("DATA STATUS")
    for label, frame, path in [
        ("Tickets", tickets, tickets_path),
        ("AI Analysis", analysis, analysis_path),
        ("Routing tests", routing, routing_path),
        ("RAG tests", rag, rag_path),
        ("Classified data", classified, classified_path),
    ]:
        if path:
            st.markdown(f"**{label}:** {len(frame):,} rows")
        else:
            st.markdown(f"**{label}:** chưa tìm thấy")
    st.markdown(
        f"**Management report:** {'đã tìm thấy' if management_report_path else 'chưa tìm thấy'}"
    )

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
  <div class="hero-kicker">CUSTOMER OPERATIONS WORKSPACE</div>
  <div class="hero-title">🏦 Intelligent Customer Service</div>
  <div class="hero-sub">AI-assisted ticket analysis, prioritization and customer feedback insights</div>
</div>
""", unsafe_allow_html=True)

if tickets.empty:
    st.error(
        "Chưa tìm thấy dữ liệu ticket. Hãy đặt tickets.xlsx trong cùng thư mục với dashboard.py "
        "hoặc trong thư mục data/."
    )
    st.stop()

# =========================================================
# DATA SOURCE PRIORITY AND CONSISTENT TICKET VIEW
# =========================================================
# Classified Output is the preferred source for analyzed fields.
# Original tickets remain the source for the customer's original message.
def best_source_for(field):
    for frame in (classified, analysis, tickets):
        if not frame.empty and field in frame.columns and frame[field].notna().any():
            values = frame[field].astype(str).str.strip()
            if values.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA}).notna().any():
                return frame
    return tickets

def build_ticket_view(base, *sources):
    """Enrich original ticket rows with analyzed fields by ticket_id, without duplicating rows."""
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
            if col not in result.columns:
                result[col] = result["ticket_id"].map(extra[col])
            else:
                existing = result[col]
                blank = existing.isna() | existing.astype(str).str.strip().isin(["", "nan", "None"])
                mapped = result["ticket_id"].map(extra[col])
                result.loc[blank, col] = mapped.loc[blank]
    return result

ticket_view = build_ticket_view(tickets, analysis, classified)

# Use classified rows for analyzed metrics when available; fall back only when necessary.
metrics_source = classified if not classified.empty else (analysis if not analysis.empty else tickets)
total = len(metrics_source) if not metrics_source.empty else len(tickets)

urgent_source = best_source_for("is_urgent")
urgent_mask_global = norm_bool(col_series(urgent_source, "is_urgent", "false"))
urgent_count = int(urgent_mask_global.sum())

category_source = best_source_for("category")
category_series = col_series(category_source, "category", "").fillna("").astype(str).str.strip()
complaint_count = int(category_series.str.lower().isin(
    ["complaint", "complaints", "khiếu nại", "khieu nai"]
).sum())

sentiment_source = best_source_for("sentiment")
sentiment_series_global = (
    col_series(sentiment_source, "sentiment", "")
    .fillna("").astype(str).str.strip().str.lower()
)
negative_labels_global = {"negative", "neg", "negative sentiment", "tiêu cực", "tieu cuc"}
negative_count = int(sentiment_series_global.isin(negative_labels_global).sum())

top_category_counts = category_series[category_series.ne("")].value_counts()
top_category = top_category_counts.index[0] if not top_category_counts.empty else "N/A"

# =========================================================
# PAGE 1: DASHBOARD
# =========================================================

if page == "Dashboard Overview":
    st.title("Dashboard Overview")
    st.markdown(
        '<div class="section-note">'
        'Tổng quan tình hình ticket, phân phối danh mục và các trường hợp cần ưu tiên xử lý.'
        '</div>',
        unsafe_allow_html=True,
    )

    # =====================================================
    # A. DASHBOARD OVERVIEW - KPI CARDS
    # =====================================================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🎫 Total tickets", f"{total:,}")

    c2.metric(
        "🚨 Urgent tickets",
        f"{urgent_count:,}",
        f"{urgent_count / max(total, 1):.1%} of total",
    )

    c3.metric("📣 Complaints", f"{complaint_count:,}")
    c4.metric("🏷️ Most common category", str(top_category))

    st.divider()

    # =====================================================
    # C. TICKET DISTRIBUTION - CHARTS
    # =====================================================
    st.markdown("### Ticket Distribution")
    st.caption(
        "Thống kê số lượng ticket theo danh mục và loại ticket "
        "để nhận diện các nhóm công việc nổi bật."
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### Tickets by category")

        chart_source = best_source_for("category")
        if "category" in chart_source.columns:
            category_counts = (
                chart_source["category"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .head(8)
                .sort_values()
                .rename_axis("Category")
                .reset_index(name="Tickets")
            )

            fig1 = px.bar(
                category_counts,
                x="Tickets",
                y="Category",
                orientation="h",
                text="Tickets",
                color_discrete_sequence=["#2F6FB2"],
            )

            fig1.update_layout(
                height=320,
                margin=dict(l=10, r=30, t=15, b=35),
                plot_bgcolor="white",
                paper_bgcolor="white",
                yaxis_title="",
                xaxis_title="Number of tickets",
                showlegend=False,
            )

            fig1.update_traces(
                textposition="outside",
                cliponaxis=False,
            )

            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Không tìm thấy cột category trong dữ liệu.")

    with chart_col2:
        st.markdown("#### Tickets by type")

        type_source = best_source_for("ticket_type")
        if "ticket_type" in type_source.columns:
            type_counts = (
                type_source["ticket_type"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .head(8)
                .sort_values()
                .rename_axis("Ticket Type")
                .reset_index(name="Tickets")
            )

            fig2 = px.bar(
                type_counts,
                x="Tickets",
                y="Ticket Type",
                orientation="h",
                text="Tickets",
                color_discrete_sequence=["#2F6FB2"],
            )

            fig2.update_layout(
                height=320,
                margin=dict(l=10, r=30, t=15, b=35),
                plot_bgcolor="white",
                paper_bgcolor="white",
                yaxis_title="",
                xaxis_title="Number of tickets",
                showlegend=False,
            )

            fig2.update_traces(
                textposition="outside",
                cliponaxis=False,
            )

            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Không tìm thấy cột ticket_type trong dữ liệu.")

    st.divider()

    # =====================================================
    # D. TICKET MANAGEMENT - PRIORITY ACTIONS + TICKET LIST
    # =====================================================
    st.markdown("### Ticket Management")
    st.caption(
        "Theo dõi danh sách ticket và ưu tiên kiểm tra các trường hợp khẩn cấp."
    )
    shortcut_col, shortcut_note = st.columns([1, 3])
    with shortcut_col:
        if st.button("🚨 Open urgent queue", type="primary", use_container_width=True):
            st.session_state["_navigate_urgent_queue"] = True
            st.rerun()
    with shortcut_note:
        st.caption("Mở danh sách xử lý và tự động bật bộ lọc ticket khẩn cấp.")

    # Chuẩn bị dữ liệu
    preview = ticket_view.copy()

    # Sắp xếp ticket theo mã tăng dần: T001, T002, ..., T100
    if "ticket_id" in preview.columns:
        preview["_ticket_number"] = pd.to_numeric(
            preview["ticket_id"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False),
            errors="coerce",
        )

        preview = preview.sort_values(
            by="_ticket_number",
            ascending=True,
            na_position="last",
        ).drop(columns=["_ticket_number"])

    preview = preview.reset_index(drop=True)

    # Chuẩn hóa cột khẩn cấp
    if "is_urgent" in preview.columns:
        urgent_mask = norm_bool(preview["is_urgent"])
        urgent_preview = preview.loc[urgent_mask].copy()
    else:
        urgent_preview = preview.iloc[0:0].copy()

    total_urgent = len(urgent_preview)

    # Danh sách ticket trên Dashboard
    st.markdown("#### Ticket list")

    dashboard_filter = st.radio(
        "Display tickets",
        ["All tickets", "Urgent cases only"],
        horizontal=True,
        key="dashboard_ticket_filter",
    )

    # Lọc danh sách theo lựa chọn
    if dashboard_filter == "Urgent cases only":
        display_df = urgent_preview.copy()
    else:
        display_df = preview.copy()

    # Chỉ hiển thị các cột cần thiết nếu tồn tại
    preferred = [
        "ticket_id",
        "created_at",
        "category",
        "ticket_type",
        "topic",
        "sentiment",
        "is_urgent",
    ]

    visible_columns = [
        col for col in preferred
        if col in display_df.columns
    ]

    # Hiển thị số lượng ticket
    st.caption(
        f"Đang hiển thị {len(display_df):,} / {len(preview):,} ticket "
        f"• Có {total_urgent:,} ticket khẩn cấp."
    )

    # Hiển thị bảng
    st.dataframe(
        display_df[visible_columns]
        if visible_columns
        else display_df,
        use_container_width=True,
        hide_index=True,
        height=450,
    )
 
# =========================================================
# PAGE 2: TICKET MANAGEMENT
# =========================================================
elif page == "Ticket Management":
    st.title("Ticket Management")
    st.markdown('<div class="section-note">Tìm kiếm, lọc và mở một ticket để xem nội dung khách hàng cùng thông tin xử lý.</div>', unsafe_allow_html=True)

    search_col, cat_col, type_col, urgent_col = st.columns([2, 1, 1, 1])
    with search_col:
        query = st.text_input("Search ticket", placeholder="Nhập ticket ID hoặc từ khóa trong nội dung...")
    with cat_col:
        cats = ["All"] + sorted(col_series(tickets, "category", "").dropna().astype(str).unique().tolist())
        category = st.selectbox("Category", cats)
    with type_col:
        types = ["All"] + sorted(col_series(tickets, "ticket_type", "").dropna().astype(str).unique().tolist())
        ticket_type = st.selectbox("Ticket type", types)
    with urgent_col:
        urgency_filter = st.selectbox("Priority", ["All", "Urgent only", "Non-urgent"])

    filtered = ticket_view.copy()
    if query.strip():
        message = col_series(filtered, "customer_message", "").astype(str)
        ids = col_series(filtered, "ticket_id", "").astype(str)
        filtered = filtered[message.str.contains(query, case=False, na=False) | ids.str.contains(query, case=False, na=False)]
    if category != "All" and "category" in filtered.columns:
        filtered = filtered[filtered["category"].astype(str) == category]
    if ticket_type != "All" and "ticket_type" in filtered.columns:
        filtered = filtered[filtered["ticket_type"].astype(str) == ticket_type]
    if urgency_filter != "All" and "is_urgent" in filtered.columns:
        mask = norm_bool(filtered["is_urgent"])
        filtered = filtered[mask] if urgency_filter == "Urgent only" else filtered[~mask]
    if st.session_state.get("ticket_urgent_only", False) and "is_urgent" in filtered.columns:
        filtered = filtered[norm_bool(filtered["is_urgent"])]
        st.info("Đang bật chế độ chỉ xem ticket khẩn cấp.")
    if st.button("Clear urgent shortcut"):
        st.session_state["ticket_urgent_only"] = False
        st.rerun()

    st.caption(f"Hiển thị {len(filtered):,} / {len(ticket_view):,} ticket")
    cols = [c for c in ["ticket_id", "created_at", "category", "ticket_type", "topic", "sentiment", "is_urgent", "customer_message"] if c in filtered.columns]
    st.dataframe(filtered[cols] if cols else filtered, use_container_width=True, hide_index=True, height=320)

    if "ticket_id" in filtered.columns and not filtered.empty:
        ids = filtered["ticket_id"].astype(str).tolist()
        default_id = st.session_state.get("selected_ticket_id", ids[0])
        if default_id not in ids:
            default_id = ids[0]
        selected = st.selectbox("Open ticket details", ids, index=ids.index(default_id))
        st.session_state["selected_ticket_id"] = selected
        row = filtered[filtered["ticket_id"].astype(str) == selected].iloc[0]

        st.divider()
        st.subheader(f"Ticket detail · {selected}")
        st.markdown("**Customer message**")
        st.info(safe_text(row.get("customer_message", "Không có nội dung khách hàng.")))
        detail_cols = st.columns(4)
        for i, field in enumerate(["category", "ticket_type", "is_urgent", "created_at"]):
            with detail_cols[i]:
                display_field(ticket_view, row, field)
        with st.expander("View all original ticket fields"):
            st.json({str(k): safe_text(v) for k, v in row.to_dict().items()})
    else:
        st.warning("Không có ticket nào khớp với bộ lọc.")

# =========================================================
# PAGE 3: AI ANALYSIS & HUMAN REVIEW
# =========================================================
elif page == "AI Analysis & Review":

    st.title("AI Analysis & Review")
    st.markdown(
        '<div class="section-note">'
        'Xem kết quả phân tích AI, kiểm tra định tuyến, '
        'tham khảo kiến thức và duyệt bản nháp phản hồi trước khi gửi.'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # 1. SELECT TICKET
    # -----------------------------------------------------
    if "ticket_id" not in tickets.columns:
        st.warning("File tickets cần có cột ticket_id.")
        st.stop()

    ticket_ids = (
        tickets["ticket_id"]
        .dropna()
        .astype(str)
        .tolist()
    )

    if not ticket_ids:
        st.warning("Chưa có ticket để phân tích.")
        st.stop()

    current = st.session_state.get(
        "selected_ticket_id",
        ticket_ids[0],
    )

    if current not in ticket_ids:
        current = ticket_ids[0]

    selected = st.selectbox(
        "Select ticket to review",
        ticket_ids,
        index=ticket_ids.index(current),
        key="analysis_selected_ticket",
    )

    st.session_state["selected_ticket_id"] = selected

    ticket_row = tickets[
        tickets["ticket_id"].astype(str) == selected
    ].iloc[0]

    # -----------------------------------------------------
    # CUSTOMER REQUEST
    # -----------------------------------------------------
    st.markdown("### Customer Request")

    st.markdown(
        '<div class="section-note">'
        'Nội dung gốc khách hàng gửi đến ngân hàng.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.info(
        safe_text(
            ticket_row.get(
                "customer_message",
                "No customer message available.",
            )
        )
    )

    # Lấy kết quả phân tích của ticket được chọn
    arow_df = match_ticket(analysis, selected)
    arow = (
        arow_df.iloc[0]
        if not arow_df.empty
        else pd.Series(dtype=object)
    )

    st.divider()

    # -----------------------------------------------------
    # AI ANALYSIS
    # -----------------------------------------------------
    st.markdown("### AI Analysis")

    st.caption(
        "Kết quả AI nhận diện ý định, chủ đề, cảm xúc "
        "và các thông tin liên quan đến yêu cầu."
    )

    if arow_df.empty:
        st.info(
            "Không tìm thấy kết quả AI Analysis "
            "cho ticket này trong file phân tích."
        )
    else:
        fields = [
            "intent",
            "topic",
            "product",
            "amount",
            "channel",
            "transaction_time",
            "transaction_id",
            "sentiment",
            "missing_information",
            "note",
        ]

        existing = [
            field for field in fields
            if field in arow.index
        ]

        cols = st.columns(3)

        for i, field in enumerate(existing):
            with cols[i % 3]:
                display_field(analysis, arow, field)

    st.divider()

    # -----------------------------------------------------
    # PRIORITY & ROUTING
    # -----------------------------------------------------
    st.markdown("### Priority & Routing")

    st.caption(
        "Kiểm tra kết quả ưu tiên và định tuyến "
        "trên các tình huống kiểm thử của hệ thống."
    )

    if routing.empty:
        st.info("Chưa có file routing test.")
    else:
        st.caption(
            "Lưu ý: đây là dữ liệu kiểm thử định tuyến. "
            "Mã test case không nhất thiết tương ứng với mã ticket thực tế."
        )

        if "test_id" in routing.columns:
            test_ids = (
                routing["test_id"]
                .dropna()
                .astype(str)
                .drop_duplicates()
                .tolist()
            )

            if test_ids:
                chosen_test = st.selectbox(
                    "Routing test case",
                    test_ids,
                    key="routing_test_case",
                )

                rr = routing[
                    routing["test_id"].astype(str) == chosen_test
                ].iloc[0]
            else:
                rr = None
        else:
            rr = routing.iloc[0]

        if rr is not None:
            route_fields = [
                "expected_priority",
                "actual_priority",
                "urgency",
                "expected_department",
                "actual_department",
                "routing_reason",
                "both_correct",
            ]

            existing = [
                field for field in route_fields
                if field in rr.index
            ]

            cols = st.columns(3)

            for i, field in enumerate(existing):
                with cols[i % 3]:
                    display_field(routing, rr, field)

    st.divider()

    # -----------------------------------------------------
    # KNOWLEDGE BASE & AI DRAFT
    # -----------------------------------------------------
    st.markdown("### Knowledge Base & AI Draft")

    st.caption(
        "Kiểm tra kiến thức được truy xuất và nội dung "
        "AI đề xuất trước khi nhân viên duyệt."
    )

    draft_default = ""
    chosen_rag = "no_rag"
    rag_ids = []

    if rag.empty:
        st.info("Chưa có file RAG test.")
    else:
        if "test_id" in rag.columns:
            rag_ids = (
                rag["test_id"]
                .dropna()
                .astype(str)
                .drop_duplicates()
                .tolist()
            )

            if rag_ids:
                chosen_rag = st.selectbox(
                    "RAG test case",
                    rag_ids,
                    key="rag_test_case",
                )

                rrow = rag[
                    rag["test_id"].astype(str) == chosen_rag
                ].iloc[0]
            else:
                rrow = None
        else:
            rrow = rag.iloc[0]

        if rrow is not None:
            # Kết quả truy xuất kiến thức
            st.markdown("#### Retrieved Knowledge")

            kb_col1, kb_col2 = st.columns(2)

            with kb_col1:
                for field in [
                    "actual_kb_found",
                    "actual_source",
                    "actual_confidence",
                ]:
                    if field in rrow.index:
                        display_field(rag, rrow, field)

            with kb_col2:
                for field in [
                    "actual_reason",
                    "expected_faq_source",
                    "test_result",
                ]:
                    if field in rrow.index:
                        display_field(rag, rrow, field)

            # Lấy bản nháp từ dữ liệu kiểm thử
            draft_default = safe_text(
                rrow.get("actual_draft_response", ""),
                "",
            )

    st.markdown("#### AI Response Draft")
    
    # AI Draft thay đổi theo RAG test case được chọn
    draft_key = f"draft_{chosen_rag if chosen_rag != 'no_rag' else 'no_rag'}"

    if draft_key not in st.session_state:
        st.session_state[draft_key] = draft_default

    edited_draft = st.text_area(
        "Review and edit the response before approval",
        key=draft_key,
        height=180,
        placeholder=(
            "Bản nháp phản hồi sẽ xuất hiện tại đây "
            "nếu có trong dữ liệu."
        ),
    )

    st.caption(
        "Bản nháp cần được nhân viên rà soát. "
        "Ứng dụng không tự động gửi phản hồi cho khách hàng."
    )

    st.divider()

    # -----------------------------------------------------
    # HUMAN REVIEW
    # -----------------------------------------------------
    st.markdown("### Human Review")

    st.caption(
        "Nhân viên kiểm tra bản nháp, ghi chú và lựa chọn "
        "trạng thái xử lý phù hợp."
    )

    status_key = f"review_status_{selected}"
    review_note_key = f"review_note_{selected}"

    st.session_state.setdefault(
        status_key,
        "Pending review",
    )

    st.session_state.setdefault(
        review_note_key,
        "",
    )

    current_status = st.session_state[status_key]

    st.markdown(
        f"**Current review status:** `{current_status}`"
    )

    review_note = st.text_area(
        "Reviewer note (optional)",
        key=review_note_key,
        placeholder=(
            "Ghi chú chỉnh sửa, lý do chuyển cấp "
            "hoặc thông tin cần xác minh..."
        ),
    )

    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button(
            "✏️ Save as edited",
            use_container_width=True,
            key=f"save_edited_{selected}",
        ):
            st.session_state[status_key] = "Edited"
            st.success(
                "Đã đánh dấu bản nháp là Edited "
                "trong phiên làm việc hiện tại."
            )
            st.rerun()

    with b2:
        if st.button(
            "✅ Approve draft",
            type="primary",
            use_container_width=True,
            key=f"approve_{selected}",
        ):
            st.session_state[status_key] = "Approved"
            st.success(
                "Đã đánh dấu bản nháp là Approved "
                "trong phiên làm việc hiện tại."
            )
            st.rerun()

    with b3:
        if st.button(
            "⚠️ Escalate",
            use_container_width=True,
            key=f"escalate_{selected}",
        ):
            st.session_state[status_key] = "Escalated"
            st.warning(
                "Đã đánh dấu ticket cần chuyển cấp "
                "trong phiên làm việc hiện tại."
            )
            st.rerun()

    st.caption(
        "Trạng thái review hiện được lưu trong session của ứng dụng. "
        "Muốn lưu lâu dài giữa các phiên hoặc chia sẻ giữa nhiều nhân viên, "
        "cần kết nối database."
    )


# =========================================================
# PAGE 4: MANAGEMENT ANALYTICS
# =========================================================
elif page == "Management Analytics":
    st.title("Phân tích quản lý")
    st.markdown(
        '<div class="section-note">'
        'Tổng quan hiệu quả xử lý ticket, cảm xúc khách hàng '
        'và xu hướng khiếu nại.'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # 1. PREPARE DATA
    # -----------------------------------------------------
    # KPIs use the preferred classified output when available.
    total = len(metrics_source) if not metrics_source.empty else len(tickets)
    sentiment_frame = best_source_for("sentiment")
    sentiment_series = (
        col_series(sentiment_frame, "sentiment", "")
        .fillna("").astype(str).str.strip().str.lower()
    )
    negative_labels = {"negative", "neg", "negative sentiment", "tiêu cực", "tieu cuc"}
    negative = int(sentiment_series.isin(negative_labels).sum())
    negative_denominator = max(len(sentiment_frame), 1)

    urgent_denominator = max(len(urgent_source), 1)
    urgent_pct = urgent_count / urgent_denominator * 100
    negative_pct = negative / negative_denominator * 100

    # -----------------------------------------------------
    # 2. KPI CARDS
    # -----------------------------------------------------
    st.markdown("### Tổng quan hiệu quả")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #DCE5EF;
                border-radius:12px;
                padding:18px;
                min-height:115px;
                box-shadow:0 2px 8px rgba(16,43,78,0.04);
            ">
                <div style="color:#64748B;font-size:13px;">
                    Tổng số ticket
                </div>
                <div style="color:#17365D;font-size:30px;
                            font-weight:700;margin-top:8px;">
                    {total:,}
                </div>
                <div style="color:#64748B;font-size:12px;">
                    Tất cả ticket trong dữ liệu
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #F2D5D3;
                border-radius:12px;
                padding:18px;
                min-height:115px;
                box-shadow:0 2px 8px rgba(16,43,78,0.04);
            ">
                <div style="color:#64748B;font-size:13px;">
                    Ticket khẩn cấp
                </div>
                <div style="color:#C2413B;font-size:30px;
                            font-weight:700;margin-top:8px;">
                    {urgent_count:,}
                </div>
                <div style="color:#C2413B;font-size:12px;">
                    {urgent_pct:.1f}% of analyzed records
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #DCE5EF;
                border-radius:12px;
                padding:18px;
                min-height:115px;
                box-shadow:0 2px 8px rgba(16,43,78,0.04);
            ">
                <div style="color:#64748B;font-size:13px;">
                    Cảm xúc tiêu cực
                </div>
                <div style="color:#17365D;font-size:30px;
                            font-weight:700;margin-top:8px;">
                    {negative:,}
                </div>
                <div style="color:#64748B;font-size:12px;">
                    {negative_pct:.1f}% of analyzed records
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #DCE5EF;
                border-radius:12px;
                padding:18px;
                min-height:115px;
                box-shadow:0 2px 8px rgba(16,43,78,0.04);
            ">
                <div style="color:#64748B;font-size:13px;">
                    Chủ đề phổ biến nhất
                </div>
                <div style="color:#17365D;font-size:24px;
                            font-weight:700;margin-top:12px;
                            overflow-wrap:anywhere;">
                    {top_category}
                </div>
                <div style="color:#64748B;font-size:12px;">
                    Chủ đề xuất hiện nhiều nhất
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # 3. DISTRIBUTION CHARTS
    # -----------------------------------------------------
    st.markdown("")
    st.markdown("### Phân bố ticket")

    left, right = st.columns(2, gap="large")

    with left:
        with st.container(border=True):
            st.markdown("#### Chủ đề ticket")
            st.caption("Số lượng ticket theo chủ đề")

            topic_frame = best_source_for("topic")
            if "topic" in topic_frame.columns and topic_frame["topic"].notna().any():
                topic_counts = (
                    topic_frame["topic"].fillna("Unknown").astype(str)
                    .str.strip().replace("", "Unknown").value_counts()
                    .head(10).sort_values()
                )
                st.bar_chart(
                    topic_counts, horizontal=True, height=320, color="#3575B5"
                )
            else:
                st.info("Không tìm thấy dữ liệu topic trong các file hiện có.")

    with right:
        with st.container(border=True):
            st.markdown("#### Cảm xúc khách hàng")
            st.caption("Phân bố cảm xúc khách hàng")

            sentiment_data = best_source_for("sentiment").copy()

            if (
                not sentiment_data.empty
                and "sentiment" in sentiment_data.columns
            ):
                sentiment_counts = (
                    sentiment_data["sentiment"]
                    .fillna("Unknown")
                    .astype(str)
                    .str.strip()
                    .replace("", "Unknown")
                    .value_counts()
                )

                st.bar_chart(
                    sentiment_counts,
                    height=320,
                    color="#3575B5",
                )
            else:
                st.info("Không tìm thấy dữ liệu sentiment.")

    # -----------------------------------------------------
    # 4. COMPLAINT TREND
    # -----------------------------------------------------
    st.markdown("")
    st.markdown("### Xu hướng khiếu nại")
    st.caption("Số ticket được phân loại là khiếu nại theo ngày")

    with st.container(border=True):
        trend_source = best_source_for("category")
        if "created_at" in trend_source.columns and "category" in trend_source.columns:
            trend = trend_source.copy()
            trend["created_at"] = pd.to_datetime(
                trend["created_at"],
                errors="coerce",
            )

            category_values = (
                trend["category"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.lower()
            )

            trend = trend[
                category_values.isin(
                    {"complaint", "complaints", "khiếu nại", "khieu nai"}
                )
            ].dropna(subset=["created_at"])

            if not trend.empty:
                trend["Date"] = trend["created_at"].dt.normalize()

                daily = (
                    trend.groupby("Date")
                    .size()
                    .rename("Complaints")
                    .to_frame()
                )

                st.line_chart(
                    daily,
                    height=280,
                    color="#3575B5",
                )
                st.caption(
                    f"Total complaints in the displayed period: "
                    f"{len(trend):,}"
                )
            else:
                st.info(
                    "Không tìm thấy dữ liệu khiếu nại có ngày hợp lệ. "
                    "Hãy kiểm tra giá trị trong cột category."
                )
        else:
            st.info(
                "Cần có hai cột created_at và category để hiển thị xu hướng."
            )

    # -----------------------------------------------------
    # 5. EXPORT SUMMARY (without repeating KPI cards)
    # -----------------------------------------------------
    summary = pd.DataFrame([
        {"Chỉ số": "Tổng số ticket", "Giá trị": total},
        {"Chỉ số": "Ticket khẩn cấp", "Giá trị": urgent_count},
        {"Chỉ số": "Ticket khiếu nại", "Giá trị": complaint_count},
        {"Chỉ số": "Cảm xúc tiêu cực", "Giá trị": negative},
        {"Chỉ số": "Chủ đề phổ biến nhất", "Giá trị": top_category},
    ])

    export_col, note_col = st.columns([1, 3])
    with export_col:
        st.download_button(
            "Tải báo cáo CSV",
            summary.to_csv(index=False).encode("utf-8-sig"),
            "management_summary.csv",
            "text/csv",
            use_container_width=True,
        )
    with note_col:
        st.caption(
            "Xuất nhanh các chỉ số đang hiển thị để lưu trữ hoặc mở bằng Excel. "
            "Báo cáo chi tiết có thể được lưu riêng trong hồ sơ dự án."
        )


# =========================================================
# PAGE 5: CLASSIFIED OUTPUT
# =========================================================
elif page == "Classified Output":
    st.title("Classified Output")
    st.markdown('<div class="section-note">Tra cứu dữ liệu đã phân loại, lọc theo thuộc tính và xuất kết quả để phục vụ báo cáo.</div>', unsafe_allow_html=True)

    # Prefer the dedicated classified workbook; use analysis/tickets only as fallback.
    source = classified.copy() if not classified.empty else (analysis.copy() if not analysis.empty else tickets.copy())
    if source.empty:
        st.warning("Không có dữ liệu Classified Output để hiển thị.")
        st.stop()

    if "ticket_id" in source.columns:
        source["_sort_ticket_number"] = pd.to_numeric(
            source["ticket_id"].astype(str).str.extract(r"(\\d+)", expand=False),
            errors="coerce",
        )
        source = source.sort_values("_sort_ticket_number", na_position="last").drop(
            columns=["_sort_ticket_number"]
        )

    filter_fields = [f for f in ["topic", "sentiment", "urgency", "category", "is_urgent"] if f in source.columns]
    filter_cols = st.columns(min(max(len(filter_fields), 1), 4))
    active_filters = {}
    for i, field in enumerate(filter_fields):
        options = ["All"] + sorted(source[field].dropna().astype(str).unique().tolist())
        with filter_cols[i % len(filter_cols)]:
            active_filters[field] = st.selectbox(f"Filter by {field.replace('_',' ').title()}", options, key=f"classified_{field}")
    filtered = source.copy()
    for field, value in active_filters.items():
        if value != "All":
            filtered = filtered[filtered[field].astype(str) == value]

    search = st.text_input("Search within classified data", placeholder="Ticket ID, topic, keyword...")
    if search.strip():
        search_mask = filtered.astype(str).apply(lambda s: s.str.contains(search, case=False, na=False)).any(axis=1)
        filtered = filtered[search_mask]

    st.metric("Matching records", f"{len(filtered):,}")
    st.dataframe(filtered, use_container_width=True, hide_index=True, height=430)

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "⬇️ Download filtered CSV",
            data=filtered.to_csv(index=False).encode("utf-8-sig"),
            file_name="classified_output.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary",
        )
    with d2:
        try:
            excel_data = to_excel_bytes(filtered)
            st.download_button(
                "⬇️ Download filtered Excel",
                data=excel_data,
                file_name="classified_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except Exception as exc:
            st.warning(f"Không tạo được file Excel: {exc}")
    st.caption("Lưu ý: chỉ tải xuống và chia sẻ dữ liệu theo quyền được phép; tránh công khai thông tin định danh hoặc dữ liệu giao dịch nhạy cảm.")

st.divider()
st.caption("Intelligent Customer Service · Internal review workspace · AI suggestions require human review")
