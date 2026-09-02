import streamlit as st
import pandas as pd
import plotly.express as px

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    page_icon="🎬",
    layout="wide",
)

# ── 제목 ─────────────────────────────────────────────────────
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    """
    1년간 박스오피스 **10위권**에 든 영화 가운데 이 기간에 개봉한 **216편**의 데이터를 시각화합니다.  
    각 그래프를 살펴보며 영화 산업의 패턴을 스스로 발견해 보세요! 🔍
    """
)
st.divider()

# ── 데이터 불러오기 ───────────────────────────────────────────
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)

    # 장르: 세로막대(|)로 구분된 경우 첫 번째만 사용
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    # 개봉일: 8자리 숫자 → datetime
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d", errors="coerce")
    df["open_year"] = df["openDt"].dt.year
    df["open_month"] = df["openDt"].dt.month

    return df

df = load_data(DATA_URL)

# 데이터 미리 보기 (접을 수 있게)
with st.expander("📋 원본 데이터 미리 보기 (클릭하여 펼치기)"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 1 │ 장르별 영화 편수 - 도넛 그래프
# ════════════════════════════════════════════════════════════
st.subheader("🍩 그래프 1 · 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "genre", "count": "편수"})
)
# pandas 버전에 따른 열 이름 통일
if "genre" not in genre_counts.columns:
    genre_counts.columns = ["genre", "편수"]

fig1 = px.pie(
    genre_counts,
    names="genre",
    values="편수",
    hole=0.45,                       # 도넛 구멍 크기
    color_discrete_sequence=px.colors.qualitative.Pastel,
    hover_data={"편수": True},
    title="장르별 영화 편수 분포",
)
fig1.update_traces(
    textposition="outside",
    textinfo="label+percent",
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig1.update_layout(
    title_font_size=18,
    legend_title_text="장르",
    margin=dict(t=80, b=40, l=40, r=40),
    height=520,
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "박스오피스 상위권을 차지한 영화 중 어떤 장르가 가장 많이 개봉되었는지, "
    "특정 장르가 흥행 시장을 얼마나 점유하고 있는지 한눈에 파악할 수 있습니다."
)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 2 │ 제작 국가별 영화 편수 - 막대 그래프
# ════════════════════════════════════════════════════════════
st.subheader("🌏 그래프 2 · 제작 국가별 영화 편수")

nation_counts = (
    df["nation"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "nation", "count": "편수"})
)
if "nation" not in nation_counts.columns:
    nation_counts.columns = ["nation", "편수"]

fig2 = px.bar(
    nation_counts,
    x="nation",
    y="편수",
    color="nation",
    color_discrete_sequence=px.colors.qualitative.Safe,
    title="제작 국가별 영화 편수",
    text="편수",
)
fig2.update_traces(
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>편수: %{y}편<extra></extra>",
)
fig2.update_layout(
    title_font_size=18,
    xaxis_title="제작 국가",
    yaxis_title="영화 편수",
    showlegend=False,
    height=460,
    margin=dict(t=80, b=40, l=40, r=40),
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "국내 박스오피스 상위권이 어느 나라 영화들로 구성되어 있는지, "
    "한국 영화와 외국 영화의 비율 차이가 얼마나 되는지 비교할 수 있습니다."
)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 3 │ 총 관객 수 분포 - 히스토그램
# ════════════════════════════════════════════════════════════
st.subheader("📊 그래프 3 · 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    color_discrete_sequence=["#6C91BF"],
    title="총 관객 수 분포 (히스토그램)",
    labels={"total_audi": "총 관객 수 (명)"},
)
fig3.update_traces(
    hovertemplate="총 관객 수: %{x}명<br>영화 편수: %{y}편<extra></extra>",
)
fig3.update_layout(
    title_font_size=18,
    xaxis_title="총 관객 수 (명)",
    yaxis_title="영화 편수",
    height=460,
    margin=dict(t=80, b=40, l=40, r=40),
    bargap=0.05,
)

st.plotly_chart(fig3, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "대부분의 영화가 비슷한 관객 수 범위에 몰려 있고, "
    "소수의 영화만 압도적으로 많은 관객을 동원하는 '롱테일' 현상을 확인할 수 있습니다."
)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 4 │ 개봉일 스크린수 vs 총 관객 수 - 산점도
# ════════════════════════════════════════════════════════════
st.subheader("🔵 그래프 4 · 개봉일 스크린수 vs 총 관객 수")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    size="days_in_top10",
    size_max=25,
    color_discrete_sequence=px.colors.qualitative.Vivid,
    title="개봉일 스크린수 vs 총 관객 수 (점 크기 = 10위권 유지 일수)",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "total_audi": "총 관객 수 (명)",
        "genre": "장르",
        "days_in_top10": "10위권 유지 일수",
    },
)
fig4.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "스크린수: %{x}개<br>"
        "총 관객: %{y:,}명<br>"
        "<extra></extra>"
    )
)
fig4.update_layout(
    title_font_size=18,
    height=520,
    margin=dict(t=80, b=40, l=40, r=40),
)

st.plotly_chart(fig4, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "개봉 초기 스크린을 많이 확보할수록 총 관객 수도 늘어나는 경향이 있는지, "
    "장르별로 스크린 배분 전략이 다른지 살펴볼 수 있습니다."
)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 5 │ 10위권 유지 일수 vs 총 관객 수 - 산점도 (장르별)
# ════════════════════════════════════════════════════════════
st.subheader("📅 그래프 5 · 10위권 유지 일수 vs 총 관객 수")

fig5 = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    trendline="ols",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="10위권 유지 일수 vs 총 관객 수 (추세선 포함)",
    labels={
        "days_in_top10": "10위권 유지 일수 (일)",
        "total_audi": "총 관객 수 (명)",
        "genre": "장르",
    },
)
fig5.update_traces(
    selector=dict(mode="markers"),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "유지 일수: %{x}일<br>"
        "총 관객: %{y:,}명<br>"
        "<extra></extra>"
    ),
)
fig5.update_layout(
    title_font_size=18,
    height=520,
    margin=dict(t=80, b=40, l=40, r=40),
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "10위권에 오래 머문 영화일수록 총 관객 수가 많은지, "
    "즉 '롱런'이 흥행 성공의 지표가 될 수 있는지 추세선을 통해 확인할 수 있습니다."
)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 6 │ 장르별 총 관객 수 - 박스플롯
# ════════════════════════════════════════════════════════════
st.subheader("📦 그래프 6 · 장르별 총 관객 수 분포 (박스플롯)")

# 편수가 2편 이상인 장르만 표시
genre_filter = genre_counts[genre_counts["편수"] >= 2]["genre"].tolist()
df_filtered = df[df["genre"].isin(genre_filter)].copy()

fig6 = px.box(
    df_filtered,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="장르별 총 관객 수 분포 (2편 이상 장르)",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수 (명)",
    },
    points="all",          # 모든 데이터 포인트 표시
)
fig6.update_layout(
    title_font_size=18,
    showlegend=False,
    height=520,
    margin=dict(t=80, b=40, l=40, r=40),
    xaxis_tickangle=-30,
)

st.plotly_chart(fig6, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "장르별로 관객 수의 중앙값과 편차가 얼마나 다른지, "
    "어떤 장르가 흥행 편차가 크고 어떤 장르가 안정적인 성과를 내는지 비교할 수 있습니다."
)

st.divider()

# ── 마무리 안내 ───────────────────────────────────────────────
st.markdown(
    """
    ### 🧠 더 탐구해 볼 질문들
    - 가장 흥행한 장르와 편수가 가장 많은 장르가 일치하나요?
    - 스크린수가 많다고 반드시 관객도 많을까요?  예외는 어떤 영화인가요?
    - 10위권에 오래 머문 영화들의 공통점은 무엇일까요?
    """
)
