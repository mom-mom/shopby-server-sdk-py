"""Shopby API용 KST Timezone 처리 모듈"""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Any
from zoneinfo import ZoneInfo

from pydantic import BeforeValidator, PlainSerializer


KST = ZoneInfo("Asia/Seoul")


# ------------------------------------
#  KST Datetime 타입
# ------------------------------------
def _validate_kst_datetime(value: Any) -> datetime:
    """
    KST datetime으로 변환

    입력:
      - ISO 8601 문자열 ("2025-11-06T17:27:44.085197059", "2025-11-06T17:27:44")
      - "YYYY-MM-DD HH:MM:SS" 문자열 (공백 구분)
      - "YYYY-MM-DD" 문자열 (시간 없으면 00:00:00으로 처리)
      - naive datetime → KST로 간주
      - aware datetime → KST로 변환
    """
    # 이미 datetime 객체
    if isinstance(value, datetime):
        if value.tzinfo is None:
            # naive datetime → KST로 간주
            return value.replace(tzinfo=KST)
        else:
            # aware datetime → KST로 변환
            return value.astimezone(KST)

    # 문자열 입력
    if isinstance(value, str):
        # ISO 8601 형식 시도 (가장 포괄적 - 'T' 구분자와 microseconds 처리)
        # 예: "2025-11-06T17:27:44.085197059", "2025-11-06T17:27:44"
        try:
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            if dt.tzinfo is None:
                return dt.replace(tzinfo=KST)
            else:
                return dt.astimezone(KST)
        except ValueError:
            pass

        # "YYYY-MM-DD HH:MM:SS" 형식 시도 (공백 구분)
        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return dt.replace(tzinfo=KST)
        except ValueError:
            pass

        # "YYYY-MM-DD" 형식 시도 (00:00:00으로 처리)
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            return dt.replace(tzinfo=KST)
        except ValueError:
            raise ValueError(
                f"Invalid datetime format (expected ISO 8601, 'YYYY-MM-DD HH:MM:SS', or 'YYYY-MM-DD'): {value}"
            )

    raise TypeError(f"Invalid type for KstDatetime: {type(value)}")


def _serialize_kst_datetime(value: datetime) -> str:
    """JSON 직렬화 시 KST 문자열로 변환"""
    return value.astimezone(KST).strftime("%Y-%m-%d %H:%M:%S")


KstDatetime = Annotated[
    datetime,
    BeforeValidator(_validate_kst_datetime),
    PlainSerializer(_serialize_kst_datetime, when_used="json-unless-none"),
]
"""
Shopby API의 datetime 필드용 커스텀 타입 (KST timezone)

입력:
  - ISO 8601 문자열 ("2025-11-06T17:27:44.085197059" 등)
  - "YYYY-MM-DD HH:MM:SS" 문자열 (공백 구분)
  - "YYYY-MM-DD" 문자열 (날짜만)
  - naive datetime → KST로 변환
  - aware datetime → KST로 변환
출력(JSON):
  - "YYYY-MM-DD HH:MM:SS" (KST)

Example:
    ```python
    class MyModel(BaseDto):
        created_at: KstDatetime
        updated_at: KstDatetime | None = None
    ```
"""


# ------------------------------------
#  KST Date 타입
# ------------------------------------
def _validate_kst_date(value: Any) -> date:
    """
    KST date로 변환

    입력:
      - "YYYY-MM-DD" 문자열
      - date 객체
    """
    if isinstance(value, date) and not isinstance(value, datetime):
        return value

    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format (expected 'YYYY-MM-DD'): {value}")

    raise TypeError(f"Invalid type for KstDate: {type(value)}")


def _serialize_kst_date(value: date) -> str:
    """JSON 직렬화 시 날짜 문자열로 변환"""
    return value.strftime("%Y-%m-%d")


KstDate = Annotated[
    date,
    BeforeValidator(_validate_kst_date),
    PlainSerializer(_serialize_kst_date, when_used="json-unless-none"),
]
"""
Shopby API의 date 필드용 커스텀 타입 (날짜만)

입력:
  - "YYYY-MM-DD" 문자열
  - date 객체
출력(JSON):
  - "YYYY-MM-DD"

Example:
    ```python
    class MyModel(BaseDto):
        start_date: KstDate
        end_date: KstDate | None = None
    ```
"""


# ------------------------------------
#  유틸리티 함수
# ------------------------------------
def to_kst_string(dt: datetime) -> str:
    """
    datetime을 KST 문자열로 변환 (API 요청 시 사용)

    Args:
        dt: datetime 객체 (naive 또는 aware)

    Returns:
        "YYYY-MM-DD HH:MM:SS" 형식의 KST 문자열

    Example:
        ```python
        from datetime import datetime
        from shopby_sdk.base.kst import to_kst_string

        # naive datetime (KST로 간주)
        dt = datetime(2025, 3, 1, 12, 30, 0)
        print(to_kst_string(dt))  # "2025-03-01 12:30:00"

        # UTC datetime (KST로 변환)
        from zoneinfo import ZoneInfo
        utc_dt = datetime(2025, 3, 1, 3, 30, 0, tzinfo=ZoneInfo("UTC"))
        print(to_kst_string(utc_dt))  # "2025-03-01 12:30:00"
        ```
    """
    if dt.tzinfo is None:
        # naive datetime → KST로 간주
        dt = dt.replace(tzinfo=KST)
    # KST로 변환하여 문자열로
    return dt.astimezone(KST).strftime("%Y-%m-%d %H:%M:%S")
