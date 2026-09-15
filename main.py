```python
import streamlit as st
import pandas as pd

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
    """서울 기온 데이터를 불러오고 연평균 기온을 계산합니다."""
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    # 연도별 평균기온 계산
    yearly = (
        df.dropna(subset=["평균기온"])
        .groupby("연도", as_index=False)["평균기온"]
        .mean()
    )

    return yearly


# 데이터 불러오기
try:
    yearly_data = load_data()
except Exception as e:
    st.error("기온 데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
    st.stop()


# 제목
st.title("🌡️ 서울의 100년 기온 변화")
st.markdown(
    "서울의 일별 기온 데이터를 이용해 **연도별 평균기온**을 계산하고 "
    "장기간의 기온 변화를 보여줍니다."
)

# 분석 기간
start_year = int(yearly_data["연도"].min())
end_year = int(yearly_data["연도"].max())

st.info(
    f"📅 분석 기간: **{start_year}년 ~ {end_year}년** "
    f"({end_year - start_year + 1}년)"
)

# 그래프용 데이터
chart_data = yearly_data.set_index("연도")

# 선 그래프
st.subheader("연도별 평균기온")

st.line_chart(
    chart_data["평균기온"],
    height=500,
)

st.caption("단위: °C · 각 연도의 일별 평균기온을 평균하여 계산")

# 요약 정보
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "가장 낮은 연평균 기온",
        f"{yearly_data['평균기온'].min():.1f} °C",
        f"{int(yearly_data.loc[yearly_data['평균기온'].idxmin(), '연도'])}년"
    )

with col2:
    st.metric(
        "가장 높은 연평균 기온",
        f"{yearly_data['평균기온'].max():.1f} °C",
        f"{int(yearly_data.loc[yearly_data['평균기온'].idxmax(), '연도'])}년"
    )

with col3:
    first_temp = yearly_data.iloc[0]["평균기온"]
    last_temp = yearly_data.iloc[-1]["평균기온"]
    change = last_temp - first_temp

    st.metric(
        "첫해 대비 마지막 해 변화",
        f"{change:+.1f} °C",
        f"{start_year}년 → {end_year}년"
    )

# 데이터 표
with st.expander("연도별 평균기온 데이터 보기"):
    display_data = yearly_data.copy()
    display_data["평균기온"] = display_data["평균기온"].round(2)
    display_data.columns = ["연도", "평균기온 (°C)"]

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
```
