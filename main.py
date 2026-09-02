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
)
genre_counts.columns = ["genre", "편수"]

fig1 = px.pie(
    genre_counts,
    names="genre",
    values="편수",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Pastel,
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
# 그래프 2 │ 장르-영화 트리맵 (크기 = 총 관객)
# ════════════════════════════════════════════════════════════
st.subheader("🗺️ 그래프 2 · 장르 안에 영화가 담긴 트리맵 (크기 = 총 관객)")

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],   # 장르 → 영화명 계층
    values="total_audi",
    color="genre",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="장르별 영화 트리맵 (칸 크기 = 총 관객 수)",
)
fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명<br>"
        "<extra></extra>"
    ),
    textinfo="label",
)
fig2.update_layout(
    title_font_size=18,
    height=600,
    margin=dict(t=80, b=40, l=40, r=40),
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "장르별·영화별 총 관객 규모를 면적으로 한눈에 비교할 수 있으며, "
    "특정 장르 안에서 흥행을 독식한 영화가 있는지 확인할 수 있습니다."
)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 3 │ 총 관객 수 분포 - 히스토그램
# ════════════════════════════════════════════════════════════
st.subheader("📊 그래프 3 · 총 관객 수 분포 (히스토그램)")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    color_discrete_sequence=["#6C91BF"],
    title="총 관객 수 분포",
    labels={"total_audi": "총 관객 수 (명)"},
)
fig3.update_traces(
    hovertemplate="총 관객 수 구간: %{x}명<br>영화 편수: %{y}편<extra></extra>",
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

# ── 히스토그램 아래 자동 문구 ────────────────────────────────
most_common_bin_movies = df[df["total_audi"] < df["total_audi"].quantile(0.75)]
lower = int(df["total_audi"].min())
upper = int(df["total_audi"].quantile(0.75))
top_movie_row = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie_row["movieNm"]
top_movie_audi = int(top_movie_row["total_audi"])

st.markdown(
    f"""
    > 📌 **전체 영화의 약 75%** 는 총 관객 수 **{lower:,}명 ~ {upper:,}명** 구간에 몰려 있습니다.  
    > 🏆 가장 관객이 많은 영화는 **「{top_movie_name}」** 으로, 총 **{top_movie_audi:,}명** 을 동원했습니다.
    """
)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "대부분의 영화가 비슷한 관객 수 범위에 몰려 있고, "
    "소수의 영화만 압도적으로 많은 관객을 동원하는 '롱테일' 현상을 확인할 수 있습니다."
)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 4 │ 개봉일 스크린수 vs 총 관객 수 - 산점도 (장르별 색)
# ════════════════════════════════════════════════════════════
st.subheader("🔵 그래프 4 · 개봉일 스크린수 vs 총 관객 수 (장르별 색)")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    title="개봉일 스크린수 vs 총 관객 수",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "total_audi": "총 관객 수 (명)",
        "genre": "장르",
    },
)
fig4.update_traces(
    marker=dict(size=8, opacity=0.75),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "<extra></extra>"
    ),
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
# 그래프 5 │ 장르별 총 관객 수 - 박스플롯 (10편 이상 장르만)
# ════════════════════════════════════════════════════════════
st.subheader("📦 그래프 5 · 장르별 총 관객 수 분포 (10편 이상 장르, 박스플롯)")

# 10편 이상인 장르만 필터
genre_10 = (
    df["genre"]
    .value_counts()
    .loc[lambda s: s >= 10]
    .index.tolist()
)
df_box = df[df["genre"].isin(genre_10)].copy()

fig5 = px.box(
    df_box,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="장르별 총 관객 수 분포 (영화 10편 이상 장르)",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수 (명)",
    },
    points="outliers",   # 아웃라이어만 점으로 표시
)
fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,}명<br>"
        "<extra></extra>"
    ),
)
fig5.update_layout(
    title_font_size=18,
    showlegend=False,
    height=520,
    margin=dict(t=80, b=40, l=40, r=40),
    xaxis_tickangle=-20,
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "장르별로 관객 수의 중앙값과 편차가 얼마나 다른지, "
    "어떤 장르가 흥행 편차가 크고 어떤 장르가 안정적인 성과를 내는지 비교할 수 있습니다."
)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 6 │ 버블 그래프 (스크린수 vs 총관객, 버블 크기 = 첫 주 관객)
# ════════════════════════════════════════════════════════════
st.subheader("🫧 그래프 6 · 개봉일 스크린수 vs 총 관객 수 (버블 크기 = 첫 주 관객)")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=55,
    color_discrete_sequence=px.colors.qualitative.Vivid,
    title="개봉일 스크린수 vs 총 관객 수 (버블 크기 = 첫 주 관객 수)",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "total_audi": "총 관객 수 (명)",
        "first_week_audi": "첫 주 관객 수",
        "genre": "장르",
    },
)
fig6.update_traces(
    marker=dict(opacity=0.65, line=dict(width=0.5, color="white")),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명<br>"
        "<extra></extra>"
    ),
)
fig6.update_layout(
    title_font_size=18,
    height=560,
    margin=dict(t=80, b=40, l=40, r=40),
)

st.plotly_chart(fig6, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "스크린수·총 관객·첫 주 관객 세 가지 변수를 동시에 비교할 수 있으며, "
    "개봉 첫 주에 폭발적인 관객을 모은 영화와 꾸준히 관객을 끌어모은 영화를 구분할 수 있습니다."
)

st.divider()

# ════════════════════════════════════════════════════════════
# 그래프 7 │ 제작 국가 → 장르 선버스트 (크기 = 영화 편수)
# ════════════════════════════════════════════════════════════
st.subheader("☀️ 그래프 7 · 제작 국가 → 장르 선버스트 (크기 = 영화 편수)")

# 국가-장르 조합별 편수 집계
sunburst_df = (
    df.groupby(["nation", "genre"])
    .size()
    .reset_index(name="편수")
)

fig7 = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],   # 국가 → 장르 계층
    values="편수",
    color="nation",
    color_discrete_sequence=px.colors.qualitative.Safe,
    title="제작 국가 → 장르 선버스트 (칸 크기 = 영화 편수)",
)
fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percentRoot:.1%}<br>"
        "<extra></extra>"
    ),
    textinfo="label+percent entry",
    insidetextorientation="radial",
)
fig7.update_layout(
    title_font_size=18,
    height=620,
    margin=dict(t=80, b=40, l=40, r=40),
)

st.plotly_chart(fig7, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것** : "
    "나라별로 어떤 장르의 영화가 많이 박스오피스에 진입했는지, "
    "한국과 외국 영화가 서로 다른 장르 전략을 가지고 있는지 비교할 수 있습니다."
)

st.divider()

# ── 마무리 안내 ───────────────────────────────────────────────
st.markdown(
    """
    ### 🧠 더 탐구해 볼 질문들
    - 가장 흥행한 장르와 편수가 가장 많은 장르가 일치하나요?
    - 스크린수가 많다고 반드시 관객도 많을까요?  예외는 어떤 영화인가요?
    - 첫 주 관객이 많은 영화가 꼭 총 관객도 많을까요?
    - 나라별로 강세인 장르가 다른가요?  그 이유는 무엇일까요?
    """
)
