"""Extract the logged-in Shiraz University semester calendar into JSON.

The script opens Chrome and leaves authentication/navigation to the user. After
navigation to the calendar page, press Enter in the terminal to extract it.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


FIELD_IDS = {
    "unit": "edUnit",
    "year": "edYear",
    "term": "edTerm",
    "semester_start": "edTStart",
    "semester_end": "edTEnd",
    "exam_start": "edExamStart",
    "exam_end": "edExamEnd",
    "tuition_deadline": "edTuitionEnd",
    "evaluation_start": "edEvalStart",
    "evaluation_end": "edEvalEnd",
    "registration_batch_end": "edRegBatchDate",
    "registration_batch_year": "edRegBatchEntrant",
    "registration_batch_max_units": "edRegBatchMax",
    "practical_grade_extra_days": "edActGradeTime",
    "special_course_grade_deadline": "edLimitGradeSpc",
    "graduate_defense_deadline": "edTTDefDeadline",
    "registration_day_start_time": "edStartHour",
}

REGISTRATION_FIELDS = {
    "pre_registration": ("edPreStart", "edPreEndStd"),
    "registration_stage_1": ("edReg1Start", "edReg1End"),
    "registration_stage_2": ("edReg2Start", "edReg2EndStd"),
    "add_drop": ("edAddStart", "edAddEndStd"),
    "final_drop": ("edDropStart", "edDropEndStd"),
}

GRADE_DEADLINE_FIELDS = {
    "associate": "edL1",
    "continuous_associate": "edL9",
    "non_continuous_bachelor": "edL2",
    "bachelor": "edL3",
    "professional_doctorate": "edL6",
    "doctorate": "edL7",
    "non_continuous_master": "edL4",
    "continuous_master": "edL5",
    "scholar": "edL8",
    "residency": "edL10",
}

REGISTRATION_NAMES = {
    "pre_registration": "ثبت نام مقدماتی",
    "registration_stage_1": "مرحله اول ثبت نام",
    "registration_stage_2": "مرحله دوم ثبت نام",
    "add_drop": "حذف و اضافه",
    "final_drop": "حذف نهایی",
}

SEMESTER_NAMES = {
    "unit": "واحد دانشگاهی",
    "year": "سال",
    "term": "ترم",
    "semester_start": "شروع نیمسال",
    "semester_end": "پایان نیمسال",
    "exam_start": "شروع امتحانات",
    "exam_end": "پایان امتحانات",
    "tuition_deadline": "مهلت پرداخت شهریه",
    "evaluation_start": "شروع ارزیابی",
    "evaluation_end": "پایان ارزیابی",
    "graduate_defense_deadline": "آخرین مهلت دفاع تحصیلات تکمیلی",
    "special_course_grade_deadline": "مهلت درج نمره دروس خاص",
    "registration_batch_end": "آخرین مهلت ثبت نام گروهی",
    "registration_batch_year": "ورودی نیمسال ثبت نام گروهی",
    "registration_batch_max_units": "حداکثر واحد ثبت نام گروهی",
    "practical_grade_extra_days": "مهلت اضافی نمره دروس عملی",
    "registration_day_start_time": "ساعت شروع روز اول ثبت نام",
}

GRADE_DEADLINE_NAMES = {
    "associate": "کاردانی",
    "continuous_associate": "کاردانی پیوسته",
    "non_continuous_bachelor": "کارشناسی ناپیوسته",
    "bachelor": "کارشناسی",
    "professional_doctorate": "دکترای حرفه‌ای",
    "doctorate": "دکترا",
    "non_continuous_master": "کارشناسی ارشد ناپیوسته",
    "continuous_master": "کارشناسی ارشد پیوسته",
    "scholar": "دانشور",
    "residency": "دکتری دستیاری",
}


def normalize_text(value: str) -> str:
    """Normalize whitespace and Arabic/Persian variants without changing digits."""
    replacements = str.maketrans(
        {
            "ي": "ی",
            "ى": "ی",
            "ك": "ک",
            "ۀ": "ه",
            "ة": "ه",
            "ـ": "",
        }
    )
    value = unicodedata.normalize("NFKC", value).translate(replacements)
    return re.sub(r"\s+", " ", value).strip()


def to_ascii_digits(value: str) -> str:
    return str(value).translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))


def to_persian_digits(value: str) -> str:
    return str(value).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


def add_jalali_days(value: str, days: int) -> str:
    year, month, day = [int(part) for part in to_ascii_digits(value).split("/")]
    for _ in range(days):
        day += 1
        month_length = 31 if month <= 6 else 30
        if month == 12:
            month_length = 30
        if day > month_length:
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
    return to_persian_digits(f"{year:04d}/{month:02d}/{day:02d}")


def text_or_empty(driver: webdriver.Chrome, element_id: str) -> str:
    try:
        return normalize_text(driver.find_element(By.ID, element_id).text)
    except NoSuchElementException:
        return ""


def extract_table(table: Any) -> dict[str, Any]:
    rows = table.find_elements(By.XPATH, "./tbody/tr | ./tr")
    parsed_rows: list[list[str]] = []
    header: list[str] | None = None

    for row in rows:
        cells = row.find_elements(By.XPATH, "./th | ./td")
        values = [normalize_text(cell.text) for cell in cells]
        if not values:
            continue
        if header is None and row.find_elements(By.XPATH, "./th"):
            header = values
        else:
            parsed_rows.append(values)

    if header:
        records = []
        for values in parsed_rows:
            record = {
                header[index] or f"column_{index + 1}": values[index]
                if index < len(values)
                else ""
                for index in range(len(header))
            }
            records.append(record)
    else:
        records = [
            {f"column_{index + 1}": value for index, value in enumerate(values)}
            for values in parsed_rows
        ]

    return {
        "id": table.get_attribute("id") or "",
        "class": table.get_attribute("class") or "",
        "headers": header or [],
        "rows": records,
    }


def find_table(tables: list[dict[str, Any]], header_name: str) -> dict[str, Any]:
    for table in tables:
        if header_name in table["headers"]:
            return table
    return {"headers": [], "rows": []}


def extract_stage_one_openings(
    tables: list[dict[str, Any]], registration_start: str
) -> list[dict[str, str]]:
    table = find_table(tables, "ورودی")
    openings = []
    for row in table["rows"]:
        cohort = row.get("ورودی", "")
        day_offset = to_ascii_digits(row.get("روز", ""))
        start_time = row.get("ساعت شروع", "")
        if not cohort or not day_offset.isdigit() or not start_time:
            continue
        if int(day_offset) == 0 and to_ascii_digits(start_time) == "0":
            continue
        date_value = add_jalali_days(registration_start, int(day_offset))
        openings.append(
            {
                "cohort": cohort,
                "date": date_value,
                "start_time": start_time,
                "datetime": f"{date_value} ساعت {start_time}",
            }
        )
    return openings


def extract_student_processes(tables: list[dict[str, Any]]) -> list[dict[str, str]]:
    table = next((table for table in tables if table["id"] == "edList"), {})
    return [
        {
            "row": row.get("ردیف", ""),
            "process": row.get("فرآیند", ""),
            "start": row.get("از تاریخ", ""),
            "end": row.get("تا تاریخ", ""),
        }
        for row in table.get("rows", [])
        if row.get("فرآیند")
    ]


def extract_registration_levels(tables: list[dict[str, Any]]) -> list[str]:
    for table in tables:
        values = [value for row in table["rows"] for value in row.values()]
        if any("مقاطعی که بازه" in value for value in values):
            marker_index = next(
                index for index, value in enumerate(values) if "مقاطعی که بازه" in value
            )
            return [value for value in values[marker_index + 1:] if value]
    return []


def extract_registration_extras(
    tables: list[dict[str, Any]], default_start_time: str
) -> list[dict[str, str]]:
    table = find_table(tables, "عنوان")
    extras = []
    for row in table["rows"]:
        title = row.get("عنوان", "").rstrip(":")
        if title == "مهلت اضافی ثبت دروس خاص":
            extras.append(
                {
                    "name": title,
                    "value": row.get("تاریخ شروع", ""),
                }
            )
    extras.append(
        {
            "name": "ساعت شروع روز اول هر مرحله",
            "value": default_start_time,
        }
    )
    return extras


def extract_calendar(driver: webdriver.Chrome) -> dict[str, Any]:
    metadata = {
        key: text_or_empty(driver, element_id)
        for key, element_id in FIELD_IDS.items()
    }

    registration = {}
    for name, (start_id, end_id) in REGISTRATION_FIELDS.items():
        registration[name] = {
            "start": text_or_empty(driver, start_id),
            "end": text_or_empty(driver, end_id),
        }

    grade_deadlines = {
        name: text_or_empty(driver, element_id)
        for name, element_id in GRADE_DEADLINE_FIELDS.items()
    }

    tables = [
        extract_table(table)
        for table in driver.find_elements(By.CSS_SELECTOR, "table")
        if table.is_displayed()
    ]

    registration_periods = [
        {
            "name": REGISTRATION_NAMES[name],
            "start": values["start"],
            "end": values["end"],
        }
        for name, values in registration.items()
    ]
    grade_deadlines = [
        {
            "name": GRADE_DEADLINE_NAMES[name],
            "date": value,
        }
        for name, value in grade_deadlines.items()
    ]
    semester_details = [
        {
            "key": key,
            "name": SEMESTER_NAMES[key],
            "value": value,
        }
        for key, value in metadata.items()
        if key not in {
            "semester_start",
            "semester_end",
            "exam_start",
            "exam_end",
            "evaluation_start",
            "evaluation_end",
        }
    ]
    registration_start = registration["registration_stage_1"]["start"]
    return {
        "semester": metadata,
        "semester_details": semester_details,
        "registration_periods": registration_periods,
        "grade_deadlines": grade_deadlines,
        "registration_extras": extract_registration_extras(
            tables, metadata["registration_day_start_time"]
        ),
        "registration_applicable_levels": extract_registration_levels(tables),
        "stage_one_registration_openings": extract_stage_one_openings(
            tables, registration_start
        ),
        "student_processes": extract_student_processes(tables),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract a logged-in semester calendar page to JSON."
    )
    parser.add_argument(
        "--start-url",
        default="http://sess.shirazu.ac.ir/",
        help="Page to open before manual login (default: Shiraz university portal).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("semester-calendar.json"),
        help="Output JSON path.",
    )
    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=300,
        help="Maximum time to wait for the calendar page after pressing Enter.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    driver = webdriver.Chrome()
    driver.get(args.start_url)

    print("Chrome is open.")
    print("Log in and navigate to the semester calendar page.")
    input("When the page is visible, press Enter here to extract it: ")

    try:
        WebDriverWait(driver, args.wait_seconds).until(
            EC.presence_of_element_located((By.ID, "edYear"))
        )
    except TimeoutException as error:
        driver.quit()
        raise RuntimeError(
            "The page did not contain the expected semester calendar field 'edYear'."
        ) from error

    result = extract_calendar(driver)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Saved semester calendar to {args.output}")
    driver.quit()


if __name__ == "__main__":
    main()
