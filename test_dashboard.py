
from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest


# Xác định vị trí các file trong dự án
PROJECT_DIR = Path(__file__).resolve().parents[1]
DASHBOARD_PATH = (
    PROJECT_DIR / "app" / "dashboard" / "dashboard.py"
)
DATA_DIR = DASHBOARD_PATH.parent


# Các file Excel mà dashboard sử dụng
EXCEL_FILES = [
    "tickets.xlsx",
    "tickets_analyzed.xlsx",
    "test_routing.xlsx",
    "test_rag.xlsx",
    "Copy of classified_feedback.xlsx",
]


def test_dashboard_file_exists():
    """Kiểm tra file dashboard.py có tồn tại."""
    assert DASHBOARD_PATH.is_file()


def test_required_excel_files_exist():
    """Kiểm tra các file Excel đầu vào của dashboard."""
    for filename in EXCEL_FILES:
        assert (DATA_DIR / filename).is_file(), (
            f"Missing Excel file: {filename}"
        )


def test_ticket_data_has_required_columns():
    """Kiểm tra các cột cần thiết để hiển thị ticket."""
    df = pd.read_excel(DATA_DIR / "tickets.xlsx")

    required_columns = [
        "ticket_id",
        "customer_message",
        "category",
        "ticket_type",
        "is_urgent",
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    assert missing == [], (
        f"Missing columns in tickets.xlsx: {missing}"
    )


def test_ticket_data_is_not_empty():
    """Kiểm tra dữ liệu ticket có bản ghi."""
    df = pd.read_excel(DATA_DIR / "tickets.xlsx")

    assert not df.empty
    assert df["ticket_id"].notna().all()


def test_ai_analysis_has_ticket_id():
    """Kiểm tra dữ liệu AI Analysis có khóa liên kết."""
    df = pd.read_excel(DATA_DIR / "tickets_analyzed.xlsx")

    assert "ticket_id" in df.columns
    assert not df.empty


def test_classified_output_has_required_columns():
    """Kiểm tra các cột dùng cho Classified Output."""
    df = pd.read_excel(
        DATA_DIR / "Copy of classified_feedback.xlsx"
    )

    required_columns = [
        "ticket_id",
        "topic",
        "sentiment",
        "urgency",
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    assert missing == [], (
        f"Missing columns in classified output: {missing}"
    )


def test_ticket_ids_are_unique():
    """Kiểm tra ticket_id có bị trùng trong dữ liệu gốc."""
    df = pd.read_excel(DATA_DIR / "tickets.xlsx")

    assert df["ticket_id"].is_unique


def test_urgent_ticket_count_logic():
    """Kiểm tra cách đếm ticket khẩn cấp của dashboard."""
    df = pd.read_excel(DATA_DIR / "tickets.xlsx")

    assert "is_urgent" in df.columns

    urgent_count = (
        df["is_urgent"]
        .astype(str)
        .str.lower()
        .isin(["true", "1", "yes", "urgent"])
        .sum()
    )

    assert 0 <= urgent_count <= len(df)


def test_dashboard_runs_without_streamlit_errors():
    """Chạy ứng dụng và kiểm tra lỗi Streamlit."""
    app = AppTest.from_file(
        str(DASHBOARD_PATH),
        default_timeout=30,
    ).run()

    assert len(app.exception) == 0, [
        str(error.value) for error in app.exception
    ]
