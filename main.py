```python
import streamlit as st
import pandas as pd
import altair as alt

# 페이지 설정
st.set_page_config(
    page_title="서울 100년 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    # CSV 파일 읽기
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온 숫자 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 날짜 또는 평균기온이 없는 행 제거
    df = df.dropna(subset=["날짜", "평균기온"]).copy()

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    # 연도별 평균기온 계산
    yearly = (
        df.groupby("연도", as_index=False)["평균기온"]
        .mean()
        .sort_values("연도")
    )

    # 소수점 둘째 자리까지 반올림
    yearly["평균기온"] = yearly["평균기온"].round(2)

    return yearly


# 데이터 불러오기
try:
    data = load_data()

except Exception as e:
    st.error("기온 데이터를 불러오는 중 오류가 발생했습니다.")
    st.write("오류 내용:", e)
    st.stop()


# 제목
st.title("🌡️ 서울의 100년 기온 변화")

st.write(
    "서울의 일별 기온 데이터를 이용하여 연평균 기온을 계산했습니다."
    " 아래 그래프에서 장기간의 기온 변화를 확인할 수 있습니다."
)


# 분석 기간
start_year = int(data["연도"].min())
end_year = int(data["연도"].max())

st.info(
    f"📅 데이터 분석 기간: **{start_year}년 ~ {end_year}년**"
)


# --------------------------------
# 연평균 기온 그래프
# --------------------------------

st.subheader("연도별 평균기온")

chart = (
    alt.Chart(data)
    .mark_line()
    .encode(
        x=alt.X(
            "연도:Q",
            title="연도",
            axis=alt.Axis(format="d")
        ),
        y=alt.Y(
            "평균기온:Q",
            title="평균기온 (℃)"
        ),
        tooltip=[
            alt.Tooltip("연도:Q", title="연도", format="d"),
            alt.Tooltip("평균기온:Q", title="평균기온", format=".2f")
        ]
    )
    .properties(
        height=500
    )
)

st.altair_chart(chart, use_container_width=True)

st.caption(
    "※ 각 연도의 일별 평균기온을 평균하여 연평균 기온을 계산했습니다."
)


# --------------------------------
# 주요 기록
# --------------------------------

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


# --------------------------------
# 연도별 데이터
# --------------------------------

with st.expander("📋 연도별 평균기온 데이터 보기"):

    display_data = data.copy()

    display_data["평균기온"] = display_data["평균기온"].round(2)

    display_data.columns = [
        "연도",
        "평균기온 (℃)"
    ]

    st.dataframe(
        display_data,
        use_container_width=True
    )
```
