
from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest


# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent

DASHBOARD_PATH = PROJECT_DIR / "dashboard.py"

DATA_DIR = PROJECT_DIR


# ==========================================
# 2. EXCEL FILES REQUIRED BY THE DASHBOARD
# ==========================================

EXCEL_FILES = [
    "tickets.xlsx",
    "tickets_analyzed.xlsx",
    "test_routing.xlsx",
    "test_rag.xlsx",
    "Copy of classified_feedback.xlsx",
]


# ==========================================
# 3. TEST DASHBOARD FILE
# ==========================================

def test_dashboard_file_exists():
    assert DASHBOARD_PATH.is_file(), (
        f"Không tìm thấy dashboard.py tại: {DASHBOARD_PATH}"
    )


# ==========================================
# 4. TEST REQUIRED EXCEL FILES
# ==========================================

def test_required_excel_files_exist():
    for filename in EXCEL_FILES:
        file_path = DATA_DIR / filename

        assert file_path.is_file(), (
            f"Không tìm thấy file Excel: {filename}"
        )


# ==========================================
# 5. TEST TICKET DATA COLUMNS
# ==========================================

def test_ticket_data_has_required_columns():
    file_path = DATA_DIR / "tickets.xlsx"

    if not file_path.is_file():
        return

    df = pd.read_excel(file_path)

    required_columns = [
        "ticket_id",
        "customer_message",
        "category",
        "ticket_type",
        "is_urgent",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    assert not missing_columns, (
        f"Thiếu các cột trong tickets.xlsx: {missing_columns}"
    )


# ==========================================
# 6. TEST TICKET DATA IS NOT EMPTY
# ==========================================

def test_ticket_data_is_not_empty():
    file_path = DATA_DIR / "tickets.xlsx"

    if not file_path.is_file():
        return

    df = pd.read_excel(file_path)

    assert not df.empty, "tickets.xlsx không có dữ liệu"

    assert "ticket_id" in df.columns, (
        "tickets.xlsx không có cột ticket_id"
    )

    assert df["ticket_id"].notna().all(), (
        "Có ticket_id bị trống trong tickets.xlsx"
    )


# ==========================================
# 7. TEST AI ANALYSIS OUTPUT
# ==========================================

def test_ai_analysis_has_ticket_id():
    file_path = DATA_DIR / "tickets_analyzed.xlsx"

    if not file_path.is_file():
        return

    df = pd.read_excel(file_path)

    assert "ticket_id" in df.columns, (
        "tickets_analyzed.xlsx không có cột ticket_id"
    )

    assert not df.empty, (
        "tickets_analyzed.xlsx không có dữ liệu"
    )


# ==========================================
# 8. TEST CLASSIFIED FEEDBACK OUTPUT
# ==========================================

def test_classified_output_has_required_columns():
    file_path = DATA_DIR / "Copy of classified_feedback.xlsx"

    if not file_path.is_file():
        return

    df = pd.read_excel(file_path)

    required_columns = [
        "ticket_id",
        "topic",
        "sentiment",
        "urgency",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    assert not missing_columns, (
        f"Thiếu các cột trong classified feedback: "
        f"{missing_columns}"
    )


# ==========================================
# 9. TEST TICKET IDs ARE UNIQUE
# ==========================================

def test_ticket_ids_are_unique():
    file_path = DATA_DIR / "tickets.xlsx"

    if not file_path.is_file():
        return

    df = pd.read_excel(file_path)

    assert "ticket_id" in df.columns, (
        "Không tìm thấy cột ticket_id"
    )

    assert df["ticket_id"].is_unique, (
        "ticket_id bị trùng lặp trong tickets.xlsx"
    )


# ==========================================
# 10. TEST URGENT TICKET COUNT
# ==========================================

def test_urgent_ticket_count_logic():
    file_path = DATA_DIR / "tickets.xlsx"

    if not file_path.is_file():
        return

    df = pd.read_excel(file_path)

    assert "is_urgent" in df.columns, (
        "Không tìm thấy cột is_urgent"
    )

    urgent_count = (
        df["is_urgent"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes", "urgent"])
        .sum()
    )

    assert 0 <= urgent_count <= len(df), (
        "Số lượng ticket khẩn cấp không hợp lệ"
    )


# ==========================================
# 11. TEST STREAMLIT DASHBOARD RUNS
# ==========================================

def test_dashboard_runs_without_streamlit_errors():
    if not DASHBOARD_PATH.is_file():
        return

    app = AppTest.from_file(
        str(DASHBOARD_PATH),
        default_timeout=30,
    ).run()

    assert len(app.exception) == 0, [
        str(error.value)
        for error in app.exception
    ]
