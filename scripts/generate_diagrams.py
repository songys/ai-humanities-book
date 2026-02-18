"""
플랫 카드 스타일 다이어그램 16개 생성 스크립트
참조: 한정님 블로그/fig_server_internal-1.png
흰색 배경 + 카테고리 색상 테두리, SVG 출력
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ============================================================
# 공통 설정
# ============================================================
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'assets', 'images', 'figures')

# 챕터별 출력 폴더
CHAPTER_DIRS = {}
for ch in ['index', 'ch01', 'ch02', 'ch03', 'ch04', 'ch05']:
    d = os.path.join(BASE_DIR, ch)
    os.makedirs(d, exist_ok=True)
    CHAPTER_DIRS[ch] = d

# 한국어 폰트 설정
plt.rcParams['font.family'] = 'Apple SD Gothic Neo'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 카테고리 색상 팔레트 (참조 이미지 스타일)
# 흰색 또는 아주 연한 채움 + 카테고리별 색상 테두리
# ============================================================
# 테두리/텍스트 (강한 색)
C_RED     = '#D04040'   # 네트워크, IO, 나쁜 예
C_ORANGE  = '#E07050'   # 컴퓨팅, 프로세서, 주의
C_PURPLE  = '#9060B0'   # 인터커넥트, 특수, 보조
C_GREEN   = '#558838'   # GPU, 자원, 좋은 예
C_BLUE    = '#4080C0'   # 기본, 일반

# 연한 채움 (배경)
BG_RED    = '#FAE8E8'
BG_ORANGE = '#FFF3E0'
BG_PURPLE = '#F5E0F5'
BG_GREEN  = '#EAF2DA'
BG_BLUE   = '#E5EDF8'

# 카드 배경
BG_CARD   = '#EEF3FA'

# 중립
WHITE     = '#FFFFFF'
DARK      = '#333333'
SUBTLE    = '#666666'
GRAY_L    = '#E0E0E0'
GRAY_M    = '#BDBDBD'


def save_fig(fig, name, chapter='index'):
    """SVG 저장 — 챕터별 폴더, pad_inches로 도형 잘림 방지"""
    path = os.path.join(CHAPTER_DIRS[chapter], name)
    fig.savefig(path, format='svg', bbox_inches='tight', pad_inches=0.3,
                dpi=300, facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  -> figures/{chapter}/{name}")


def rounded_box(ax, x, y, w, h, fill, border, text='', fontsize=11,
                text_color=None, lw=1.2):
    """둥근 모서리 박스 — fill(배경)과 border(테두리) 분리"""
    if text_color is None:
        text_color = border
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.15",
                         facecolor=fill, edgecolor=border,
                         linewidth=lw, zorder=2)
    ax.add_patch(box)
    if text:
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fontsize, color=text_color, fontweight='bold', zorder=3)


def make_axes(figsize, xlim, ylim, title):
    """공통 Figure + Axes 생성 — 연한 블루그레이 카드 배경"""
    fig, ax = plt.subplots(figsize=figsize)
    margin_x = (xlim[1] - xlim[0]) * 0.05
    margin_y = (ylim[1] - ylim[0]) * 0.08
    ax.set_xlim(xlim[0] - margin_x, xlim[1] + margin_x)
    ax.set_ylim(ylim[0] - margin_y, ylim[1] + margin_y)
    ax.axis('off')

    # 연한 블루그레이 카드 배경
    card = FancyBboxPatch(
        (xlim[0] - margin_x * 0.5, ylim[0] - margin_y * 0.3),
        (xlim[1] - xlim[0]) + margin_x,
        (ylim[1] - ylim[0]) + margin_y * 0.6,
        boxstyle="round,pad=0.3",
        facecolor=BG_CARD, edgecolor=GRAY_L, linewidth=0.8, zorder=0
    )
    ax.add_patch(card)

    ax.set_title(title, fontsize=14, fontweight='bold', color=DARK, pad=18)
    return fig, ax


# ============================================================
# 1. digital-humanities-timeline.svg
# ============================================================
def diagram_01():
    fig, ax = make_axes((10, 3.5), (0, 10.5), (-0.3, 2.8),
                        '디지털 인문학 발전 타임라인')

    eras = [
        (0.5, '2000s', '디지털 아카이브\n전자 텍스트 구축', C_BLUE, BG_BLUE),
        (3.0, '2010s', '빅데이터 분석\n텍스트 마이닝', C_PURPLE, BG_PURPLE),
        (5.5, '2020s', '생성형 AI\nLLM 등장', C_GREEN, BG_GREEN),
        (8.0, '현재', 'AI와 인문학 협업\n바이브 코딩', C_ORANGE, BG_ORANGE),
    ]

    for i, (x, era, desc, color, bg) in enumerate(eras):
        circle = plt.Circle((x + 0.5, 1.8), 0.38, color=bg, ec=color, lw=1.5, zorder=3)
        ax.add_patch(circle)
        ax.text(x + 0.5, 1.8, era, ha='center', va='center',
                fontsize=9, fontweight='bold', color=color, zorder=4)
        ax.text(x + 0.5, 0.7, desc, ha='center', va='center',
                fontsize=9, color=DARK)
        if i < len(eras) - 1:
            ax.annotate('', xy=(eras[i+1][0], 1.8), xytext=(x + 1.0, 1.8),
                        arrowprops=dict(arrowstyle='->', color=GRAY_M, lw=1.5))

    save_fig(fig, 'digital-humanities-timeline.svg', 'ch01')


# ============================================================
# 2. ai-hierarchy-pyramid.svg
# ============================================================
def diagram_02():
    fig, ax = make_axes((8, 6.5), (-5, 5), (-0.5, 5.2),
                        'AI 기술 계층 구조')

    layers = [
        (-4, 0, 8, 1.0, WHITE, C_BLUE, '인공지능 (AI)', '사람의 지능을 모방하는 모든 기술'),
        (-3, 1.2, 6, 1.0, WHITE, C_PURPLE, '머신러닝 (ML)', '데이터에서 패턴을 학습'),
        (-2, 2.4, 4, 1.0, WHITE, C_GREEN, '딥러닝 (DL)', '인공 신경망으로 복잡한 패턴 학습'),
        (-1, 3.6, 2, 1.0, WHITE, C_ORANGE, 'LLM', '대규모 언어모델'),
    ]

    for x, y, w, h, fill, border, label, desc in layers:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                             facecolor=fill, edgecolor=border, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2 + 0.12, label, ha='center', va='center',
                fontsize=12, fontweight='bold', color=border)
        ax.text(x + w/2, y + h/2 - 0.22, desc, ha='center', va='center',
                fontsize=9, color=SUBTLE)

    save_fig(fig, 'ai-hierarchy-pyramid.svg', 'ch02')


# ============================================================
# 3. ai-landscape-grid.svg
# ============================================================
def diagram_03():
    fig, ax = make_axes((9, 6.5), (-0.3, 9.8), (-0.3, 5.8),
                        'AI가 바꾸는 인문학 4영역')

    cards = [
        (0.5, 3, '글쓰기와 창작', 'AI와 함께 소설, 시,\n에세이를 쓰고\n문체를 실험', C_BLUE, BG_BLUE),
        (5.0, 3, '텍스트 분석', '수천 편의 문학 작품을\n분석하고 패턴을 발견', C_PURPLE, BG_PURPLE),
        (0.5, 0.2, '번역과 소통', '언어의 장벽을 넘어\n다양한 문화를 탐색', C_GREEN, BG_GREEN),
        (5.0, 0.2, '시각적 스토리텔링', '텍스트를 이미지로 변환\n새로운 표현 방식 탐구', C_ORANGE, BG_ORANGE),
    ]

    for x, y, title, desc, color, bg in cards:
        box = FancyBboxPatch((x, y), 3.8, 2.3, boxstyle="round,pad=0.2",
                             facecolor=WHITE, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 1.9, y + 1.75, title, ha='center', va='center',
                fontsize=12, fontweight='bold', color=color)
        ax.text(x + 1.9, y + 0.8, desc, ha='center', va='center',
                fontsize=9, color=SUBTLE)

    save_fig(fig, 'ai-landscape-grid.svg', 'ch01')


# ============================================================
# 4. search-vs-generative.svg
# ============================================================
def diagram_04():
    fig, ax = make_axes((10, 4.5), (-0.3, 11.3), (-0.8, 3.8),
                        '검색 AI vs 생성형 AI')

    # 검색 AI
    rounded_box(ax, 0, 1.0, 4.5, 2.2, WHITE, C_RED)
    ax.text(2.25, 2.7, '검색 AI', ha='center', va='center',
            fontsize=13, fontweight='bold', color=C_RED)
    ax.text(2.25, 2.0, '기존 정보를 찾아서 보여줌', ha='center', va='center',
            fontsize=9, color=DARK)
    ax.text(2.25, 1.4, '사용자가 직접 읽고\n원하는 정보를 골라야 함', ha='center', va='center',
            fontsize=9, color=SUBTLE)

    # 화살표
    ax.annotate('', xy=(6.0, 2.1), xytext=(5.0, 2.1),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2))
    ax.text(5.5, 2.6, 'vs', ha='center', va='center',
            fontsize=14, fontweight='bold', color=DARK)

    # 생성형 AI
    rounded_box(ax, 6.5, 1.0, 4.5, 2.2, WHITE, C_GREEN)
    ax.text(8.75, 2.7, '생성형 AI', ha='center', va='center',
            fontsize=13, fontweight='bold', color=C_GREEN)
    ax.text(8.75, 2.0, '질문을 이해하고 답변을 생성', ha='center', va='center',
            fontsize=9, color=DARK)
    ax.text(8.75, 1.4, '대화하듯 추가 질문으로\n답변을 개선', ha='center', va='center',
            fontsize=9, color=SUBTLE)

    # 핵심 차이
    rounded_box(ax, 2.5, -0.4, 6.0, 0.85, BG_BLUE, C_BLUE,
                "핵심: '찾아준다' vs '만들어준다'", fontsize=10)

    save_fig(fig, 'search-vs-generative.svg', 'ch02')


# ============================================================
# 5. ml-era-timeline.svg
# ============================================================
def diagram_05():
    fig, ax = make_axes((11, 4), (-0.3, 11.3), (-0.3, 3.3),
                        'ML/AI 시대 구분')

    eras = [
        (0.2, 'Classical ML\n1990~2010s', 'SVM, Random Forest\n정형 데이터 중심', C_BLUE, BG_BLUE),
        (3.8, '전환점\n2017~2022', 'Transformer 등장\nGPT, ChatGPT', C_PURPLE, BG_PURPLE),
        (7.4, 'LLM 시대\n2020s~', '텍스트 생성 중심\n멀티모달, 바이브 코딩', C_GREEN, BG_GREEN),
    ]

    for x, era, desc, color, bg in eras:
        box = FancyBboxPatch((x, 0.3), 3.2, 2.5, boxstyle="round,pad=0.15",
                             facecolor=WHITE, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 1.6, 2.1, era, ha='center', va='center',
                fontsize=10, fontweight='bold', color=color)
        ax.text(x + 1.6, 1.0, desc, ha='center', va='center',
                fontsize=9, color=SUBTLE)

    for x1, x2 in [(3.4, 3.8), (7.0, 7.4)]:
        ax.annotate('', xy=(x2, 1.55), xytext=(x1, 1.55),
                    arrowprops=dict(arrowstyle='->', color=GRAY_M, lw=2))

    save_fig(fig, 'ml-era-timeline.svg', 'ch02')


# ============================================================
# 6. data-evolution-flow.svg
# ============================================================
def diagram_06():
    fig, ax = make_axes((10, 4.5), (-0.3, 10.8), (-0.8, 3.8),
                        '정형 데이터에서 비정형 데이터로')

    # 정형 데이터
    rounded_box(ax, 0.3, 1.0, 3.5, 2.2, WHITE, C_BLUE)
    ax.text(2.05, 2.6, '정형 데이터', ha='center', va='center',
            fontsize=12, fontweight='bold', color=C_BLUE)
    ax.text(2.05, 1.7, '숫자, 표, 거래 기록\n회귀, 분류, 시계열', ha='center', va='center',
            fontsize=9, color=SUBTLE)

    # 화살표
    ax.annotate('', xy=(5.2, 2.1), xytext=(4.2, 2.1),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2))
    ax.text(4.7, 2.6, '전환', ha='center', va='center',
            fontsize=10, fontweight='bold', color=DARK)

    # 비정형 데이터
    rounded_box(ax, 5.5, 1.0, 4.5, 2.2, WHITE, C_GREEN)
    ax.text(7.75, 2.6, '비정형 데이터', ha='center', va='center',
            fontsize=12, fontweight='bold', color=C_GREEN)
    ax.text(7.75, 1.7, '텍스트, 이미지, 음성\n생성, 대화, 멀티모달', ha='center', va='center',
            fontsize=9, color=SUBTLE)

    # 핵심
    rounded_box(ax, 2.0, -0.3, 6.5, 0.85, BG_ORANGE, C_ORANGE,
                '데이터의 종류가 AI의 가능성을 결정한다', fontsize=10)

    save_fig(fig, 'data-evolution-flow.svg', 'ch02')


# ============================================================
# 7. ai-working-principle.svg
# ============================================================
def diagram_07():
    fig, ax = make_axes((11, 4), (-0.3, 11.3), (-0.2, 3.3),
                        '생성형 AI 작동 원리 4단계')

    steps = [
        (0.2, '1단계', '대량의 텍스트\n학습', C_BLUE, BG_BLUE),
        (2.9, '2단계', '다음 단어\n예측 능력', C_PURPLE, BG_PURPLE),
        (5.6, '3단계', '사용자 질문에\n답변 생성', C_GREEN, BG_GREEN),
        (8.3, '4단계', '대화로\n답변 개선', C_ORANGE, BG_ORANGE),
    ]

    for x, step, desc, color, bg in steps:
        box = FancyBboxPatch((x, 0.3), 2.3, 2.4, boxstyle="round,pad=0.15",
                             facecolor=WHITE, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 1.15, 2.1, step, ha='center', va='center',
                fontsize=11, fontweight='bold', color=color)
        ax.text(x + 1.15, 1.0, desc, ha='center', va='center',
                fontsize=9, color=SUBTLE)

    for x in [2.5, 5.2, 7.9]:
        ax.annotate('', xy=(x + 0.4, 1.5), xytext=(x, 1.5),
                    arrowprops=dict(arrowstyle='->', color=GRAY_M, lw=2))

    save_fig(fig, 'ai-working-principle.svg', 'ch02')


# ============================================================
# 8. data-misconceptions.svg
# ============================================================
def diagram_08():
    fig, ax = make_axes((9, 5.5), (-0.3, 9.8), (-0.8, 5.3),
                        '데이터에 대한 오해')

    # 오해 1
    rounded_box(ax, 0.3, 3.0, 8.8, 1.6, WHITE, C_RED)
    ax.text(1.5, 4.1, 'X  오해 1', ha='left', va='center',
            fontsize=12, fontweight='bold', color=C_RED)
    ax.text(1.5, 3.4, '데이터 양이 늘어나면 다양성도 늘어난다?\n-> 같은 종류만 쌓이면 편향이 커진다',
            ha='left', va='center', fontsize=9, color=DARK)

    # 오해 2
    rounded_box(ax, 0.3, 1.0, 8.8, 1.6, WHITE, C_RED)
    ax.text(1.5, 2.1, 'X  오해 2', ha='left', va='center',
            fontsize=12, fontweight='bold', color=C_RED)
    ax.text(1.5, 1.4, '모델이 커지면 현실을 더 잘 이해한다?\n-> 모델 크기와 세상에 대한 이해는 별개',
            ha='left', va='center', fontsize=9, color=DARK)

    # 시사점
    rounded_box(ax, 1.5, -0.4, 6.5, 0.85, BG_GREEN, C_GREEN,
                '어떤 데이터를 선택하느냐는 가치 판단의 문제', fontsize=10)

    save_fig(fig, 'data-misconceptions.svg', 'ch02')


# ============================================================
# 9. prompt-4-principles.svg
# ============================================================
def diagram_09():
    fig, ax = make_axes((9, 6.5), (-0.3, 9.8), (-0.3, 6.5),
                        '프롬프트 4원칙')

    principles = [
        (0.5, 4.2, '01 구체적으로', '원하는 것을\n정확히 표현', C_BLUE),
        (5.0, 4.2, '02 맥락 제공', '나의 상황과\n배경 정보 전달', C_PURPLE),
        (0.5, 1.5, '03 역할 부여', 'AI에게\n전문가 역할 부여', C_GREEN),
        (5.0, 1.5, '04 출력 형식', '답변의 형태를\n명시', C_ORANGE),
    ]

    for x, y, title, desc, color in principles:
        box = FancyBboxPatch((x, y), 3.8, 2.0, boxstyle="round,pad=0.2",
                             facecolor=WHITE, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 1.9, y + 1.5, title, ha='center', va='center',
                fontsize=12, fontweight='bold', color=color)
        ax.text(x + 1.9, y + 0.6, desc, ha='center', va='center',
                fontsize=10, color=SUBTLE)

    # 중앙 레이블
    center = plt.Circle((4.65, 3.6), 0.5, color=BG_BLUE, ec=C_BLUE, lw=1.5, zorder=5)
    ax.add_patch(center)
    ax.text(4.65, 3.6, '4원칙', ha='center', va='center',
            fontsize=11, fontweight='bold', color=C_BLUE, zorder=6)

    save_fig(fig, 'prompt-4-principles.svg', 'ch03')


# ============================================================
# 10. prompt-before-after.svg
# ============================================================
def diagram_10():
    fig, ax = make_axes((10, 4.5), (-0.3, 10.8), (-0.3, 3.8),
                        'Before / After 프롬프트 비교')

    # Before
    rounded_box(ax, 0.3, 0.5, 4.3, 2.7, WHITE, C_RED)
    ax.text(2.45, 2.7, 'Before', ha='center', va='center',
            fontsize=14, fontweight='bold', color=C_RED)
    ax.text(2.45, 2.0, "'요약해줘'", ha='center', va='center',
            fontsize=11, color=DARK)
    ax.text(2.45, 1.2, '모호함, 길이 불명\n관점 불명, 임의 해석', ha='center', va='center',
            fontsize=9, color=SUBTLE)

    # 화살표
    ax.annotate('', xy=(5.7, 1.85), xytext=(5.0, 1.85),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2.5))

    # After
    rounded_box(ax, 5.9, 0.5, 4.3, 2.7, WHITE, C_GREEN)
    ax.text(8.05, 2.7, 'After', ha='center', va='center',
            fontsize=14, fontweight='bold', color=C_GREEN)
    ax.text(8.05, 2.0, "'3문장으로 요약하고\n키워드 3개를 뽑아줘'", ha='center', va='center',
            fontsize=10, color=DARK)
    ax.text(8.05, 1.0, '길이 명시, 추가 정보\n적절한 난이도', ha='center', va='center',
            fontsize=9, color=SUBTLE)

    save_fig(fig, 'prompt-before-after.svg', 'ch03')


# ============================================================
# 11. tone-combination-formula.svg
# ============================================================
def diagram_11():
    fig, ax = make_axes((10, 4.5), (-0.3, 10.8), (-0.2, 3.8),
                        '말투 조합 공식')

    elements = [
        (0.3, '화자', C_BLUE),
        (2.3, '독자', C_PURPLE),
        (4.3, '종결 어미', C_GREEN),
        (6.3, '비유 여부', C_ORANGE),
    ]

    for x, label, color in elements:
        box = FancyBboxPatch((x, 1.5), 1.6, 1.6, boxstyle="round,pad=0.15",
                             facecolor=WHITE, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 0.8, 2.3, label, ha='center', va='center',
                fontsize=11, fontweight='bold', color=color)

    # + 기호들
    for x in [2.0, 4.0, 6.0]:
        ax.text(x + 0.15, 2.3, '+', ha='center', va='center',
                fontsize=16, fontweight='bold', color=DARK)

    # = 기호
    ax.text(8.25, 2.3, '=', ha='center', va='center',
            fontsize=18, fontweight='bold', color=DARK)

    # 결과
    box = FancyBboxPatch((8.6, 1.3), 1.6, 2.0, boxstyle="round,pad=0.15",
                         facecolor=BG_BLUE, edgecolor=C_BLUE, linewidth=1.8)
    ax.add_patch(box)
    ax.text(9.4, 2.3, '말투\n결정!', ha='center', va='center',
            fontsize=12, fontweight='bold', color=C_BLUE)

    # 아래 설명
    ax.text(5.0, 0.5, '이 네 가지를 조합하면 같은 내용도 완전히 다른 글이 됩니다',
            ha='center', va='center', fontsize=10, color=SUBTLE, style='italic')

    save_fig(fig, 'tone-combination-formula.svg', 'ch04')


# ============================================================
# 12. six-tones-radar.svg
# ============================================================
def diagram_12():
    categories = ['친근감', '전문성', '격식', '설득력', '객관성', '간결함']
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    tones = {
        'A. 강의형':   ([5, 3, 2, 3, 2, 3], C_BLUE),
        'B. 경험자형': ([4, 4, 3, 4, 3, 3], C_PURPLE),
        'C. 보고서형': ([1, 5, 5, 3, 5, 2], C_GREEN),
        'D. 선배형':   ([5, 2, 1, 2, 2, 5], C_ORANGE),
        'E. 마케팅형': ([3, 2, 3, 5, 2, 5], C_RED),
        'F. 기사형':   ([2, 4, 4, 3, 5, 3], GRAY_M),
    }

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8, color='#999')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax.set_title('6가지 말투 레이더 차트', fontsize=14, fontweight='bold',
                 color=DARK, pad=20)

    for name, (values, color) in tones.items():
        values_closed = values + values[:1]
        ax.plot(angles, values_closed, 'o-', linewidth=1.8, label=name, color=color)
        ax.fill(angles, values_closed, alpha=0.08, color=color)

    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=9)
    save_fig(fig, 'six-tones-radar.svg', 'ch04')


# ============================================================
# 13. ai-writing-problems.svg
# ============================================================
def diagram_13():
    fig, ax = make_axes((10, 5.5), (-0.3, 10.5), (-0.3, 5.3),
                        'AI 글의 6가지 전형적 문제')

    problems = [
        (0.3, 3.2, '① 문장 단절', '짧고 끊긴 문장', C_RED),
        (3.6, 3.2, '② 문단 분절', '지나친 줄바꿈', C_RED),
        (6.9, 3.2, '③ 번역투', '영어 직역 표현', C_RED),
        (0.3, 0.8, '④ 슬롭 워드', 'AI 과용 단어', C_ORANGE),
        (3.6, 0.8, '⑤ 종결 단조', '~합니다만 반복', C_ORANGE),
        (6.9, 0.8, '⑥ 메타 해설', '투어 가이드 문장', C_ORANGE),
    ]

    for x, y, title, desc, color in problems:
        box = FancyBboxPatch((x, y), 2.8, 1.8, boxstyle="round,pad=0.15",
                             facecolor=WHITE, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 1.4, y + 1.2, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color=color)
        ax.text(x + 1.4, y + 0.5, desc, ha='center', va='center',
                fontsize=9, color=SUBTLE)

    save_fig(fig, 'ai-writing-problems.svg', 'ch05')


# ============================================================
# 14. multiturn-strategy.svg
# ============================================================
def diagram_14():
    fig, ax = make_axes((10, 5.5), (-0.3, 10.5), (-0.3, 5.5),
                        '멀티턴 대화 전략')

    steps = [
        (0.5, 3.5, '첫 질문', '일반적인 질문으로 시작', C_BLUE),
        (0.5, 2.1, '범위 좁히기', "'그중에서 ~에 집중해줘'", C_PURPLE),
        (0.5, 0.7, '구체화', "'예를 들어 설명해줘'", C_GREEN),
    ]

    strategies = [
        (5.5, 3.5, '형식 바꾸기', "'표로 정리해줘'", C_ORANGE),
        (5.5, 2.1, '수준 조절', "'쉽게 설명해줘'", C_RED),
        (5.5, 0.7, '비판 요청', "'문제점을 지적해줘'", C_BLUE),
    ]

    for items in [steps, strategies]:
        for x, y, title, desc, color in items:
            box = FancyBboxPatch((x, y), 4.0, 1.1, boxstyle="round,pad=0.12",
                                 facecolor=WHITE, edgecolor=color, linewidth=1.5)
            ax.add_patch(box)
            ax.text(x + 2.0, y + 0.7, title, ha='center', va='center',
                    fontsize=11, fontweight='bold', color=color)
            ax.text(x + 2.0, y + 0.3, desc, ha='center', va='center',
                    fontsize=9, color=SUBTLE)

    # 세로 화살표
    for y1, y2 in [(3.5, 3.2), (2.1, 1.8)]:
        ax.annotate('', xy=(2.5, y2), xytext=(2.5, y1),
                    arrowprops=dict(arrowstyle='->', color=GRAY_M, lw=1.5))

    ax.text(2.5, 5.0, '단계적 심화', ha='center', va='center',
            fontsize=12, fontweight='bold', color=C_BLUE)
    ax.text(7.5, 5.0, '전략적 변환', ha='center', va='center',
            fontsize=12, fontweight='bold', color=C_ORANGE)

    save_fig(fig, 'multiturn-strategy.svg', 'ch03')


# ============================================================
# 15. ai-limitations-overview.svg
# ============================================================
def diagram_15():
    fig, ax = make_axes((10, 4.5), (-0.3, 10.8), (-0.3, 3.8),
                        'AI의 5가지 한계')

    limits = [
        (0.3, '환각\n(Hallucination)', '사실이 아닌 정보를\n자신있게 답함', C_RED),
        (2.3, '최신 정보\n부족', '학습 데이터 이후\n정보를 모름', C_ORANGE),
        (4.3, '개인 경험\n부재', '자기만의 경험이나\n감정이 없음', C_BLUE),
        (6.3, '수학적\n추론 한계', '복잡한 계산에서\n실수', C_PURPLE),
        (8.3, '일관성\n부족', '같은 질문에\n다른 답변', C_GREEN),
    ]

    for x, title, desc, color in limits:
        box = FancyBboxPatch((x, 0.3), 1.7, 2.8, boxstyle="round,pad=0.12",
                             facecolor=WHITE, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 0.85, 2.5, title, ha='center', va='center',
                fontsize=9, fontweight='bold', color=color)
        ax.text(x + 0.85, 1.1, desc, ha='center', va='center',
                fontsize=8, color=SUBTLE)

    save_fig(fig, 'ai-limitations-overview.svg', 'ch05')


# ============================================================
# 16. book-roadmap.svg
# ============================================================
def diagram_16():
    fig, ax = make_axes((11, 5.5), (-0.3, 11.3), (-0.3, 5.5),
                        '이 책의 로드맵')

    # Part I
    rounded_box(ax, 0.3, 3.2, 4.8, 1.6, WHITE, C_BLUE)
    ax.text(2.7, 4.3, 'Part I  AI와 인문학의 만남', ha='center', va='center',
            fontsize=11, fontweight='bold', color=C_BLUE)
    ax.text(2.7, 3.7, '1장 AI와 인문학  |  2장 생성형 AI', ha='center', va='center',
            fontsize=9, color=SUBTLE)

    # Part II
    rounded_box(ax, 5.7, 3.2, 5.0, 1.6, WHITE, C_GREEN)
    ax.text(8.2, 4.3, 'Part II  AI와 대화하기', ha='center', va='center',
            fontsize=11, fontweight='bold', color=C_GREEN)
    ax.text(8.2, 3.7, '3장 프롬프트  |  4장 말투  |  5장 평가', ha='center', va='center',
            fontsize=9, color=SUBTLE)

    # 화살표
    ax.annotate('', xy=(5.7, 4.0), xytext=(5.1, 4.0),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2))

    # 부록
    rounded_box(ax, 2.5, 0.8, 6.0, 1.6, WHITE, C_PURPLE)
    ax.text(5.5, 1.9, '부록', ha='center', va='center',
            fontsize=11, fontweight='bold', color=C_PURPLE)
    ax.text(5.5, 1.3, 'AI 도구 비교  |  프롬프트 템플릿  |  한국어 글쓰기 가이드',
            ha='center', va='center', fontsize=9, color=SUBTLE)

    # 하향 화살표
    ax.annotate('', xy=(5.5, 2.4), xytext=(5.5, 3.2),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=1.5))

    save_fig(fig, 'book-roadmap.svg', 'index')


# ============================================================
# 메인 실행
# ============================================================
if __name__ == '__main__':
    print("다이어그램 생성 시작 (플랫 카드 스타일)...")
    funcs = [
        diagram_01, diagram_02, diagram_03, diagram_04,
        diagram_05, diagram_06, diagram_07, diagram_08,
        diagram_09, diagram_10, diagram_11, diagram_12,
        diagram_13, diagram_14, diagram_15, diagram_16,
    ]
    for i, fn in enumerate(funcs, 1):
        print(f"[{i:2d}/16] {fn.__name__}")
        fn()
    print(f"\n완료! {len(funcs)}개 다이어그램이 {BASE_DIR}에 저장되었습니다.")
