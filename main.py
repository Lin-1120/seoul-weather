```python
import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 100년 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 서울 기온 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    # CSV 파일 불러오기
    df = pd.read_csv(DATA_URL)

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온 숫자로 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 잘못된 데이터 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    # 연도별 평균기온 계산
    yearly = (
        df.groupby("연도", as_index=False)["평균기온"]
        .mean()
        .sort_values("연도")
    )

    return yearly


# -----------------------------
# 데이터 불러오기
# -----------------------------

try:
    data = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.write("인터넷 연결이나 데이터 주소를 확인해주세요.")
    st.stop()


# -----------------------------
# 화면
# -----------------------------

st.title("🌡️ 서울의 100년 기온 변화")

st.write(
    "서울의 일별 기온 데이터를 이용하여 "
    "연도별 평균기온을 계산한 그래프입니다."
)

# 분석 기간
start_year = int(data["연도"].min())
end_year = int(data["연도"].max())

st.info(
    f"📅 분석 기간: **{start_year}년 ~ {end_year}년** "
    f"({end_year - start_year + 1}년)"
)


# -----------------------------
# 연평균 기온 그래프
# -----------------------------

st.subheader("연도별 평균기온")

# 그래프에 사용할 데이터
chart_data = data.set_index("연도")[["평균기온"]]

# Streamlit 버전에 관계없이 사용할 수 있는 기본 형태
st.line_chart(
    chart_data,
    height=500
)

st.caption("단위: ℃")


# -----------------------------
# 주요 기록
# -----------------------------

st.subheader("📊 주요 기록")

col1, col2, col3 = st.columns(3)

# 가장 낮은 연평균 기온
lowest_index = data["평균기온"].idxmin()
lowest_year = int(data.loc[lowest_index, "연도"])
lowest_temp = data.loc[lowest_index, "평균기온"]

# 가장 높은 연평균 기온
highest_index = data["평균기온"].idxmax()
highest_year = int(data.loc[highest_index, "연도"])
highest_temp = data.loc[highest_index, "평균기온"]

# 첫해와 마지막 해
first_temp = data.iloc[0]["평균기온"]
last_temp = data.iloc[-1]["평균기온"]
change = last_temp - first_temp


with col1:
    st.metric(
        "가장 낮은 연평균 기온",
        f"{lowest_temp:.1f} ℃",
        f"{lowest_year}년"
    )

with col2:
    st.metric(
        "가장 높은 연평균 기온",
        f"{highest_temp:.1f} ℃",
        f"{highest_year}년"
    )

with col3:
    st.metric(
        "첫해 대비 변화",
        f"{change:+.1f} ℃",
        f"{start_year}년 → {end_year}년"
    )


# -----------------------------
# 연도별 데이터
# -----------------------------

with st.expander("📋 연도별 평균기온 데이터 보기"):

    display_data = data.copy()

    display_data["평균기온"] = display_data["평균기온"].round(2)

    display_data.columns = [
        "연도",
        "평균기온 (℃)"
```
