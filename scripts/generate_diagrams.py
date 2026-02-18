"""
파스텔톤 다이어그램 16개 생성 스크립트
TikZ 스타일, SVG 출력, Apple SD Gothic Neo 폰트
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
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'assets', 'images', 'diagrams')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 한국어 폰트 설정
plt.rcParams['font.family'] = 'Apple SD Gothic Neo'
plt.rcParams['axes.unicode_minus'] = False

# 파스텔 컬러 팔레트
BLUE_L = '#A8C8E8'
BLUE_M = '#7EB3D8'
BLUE_D = '#5B9BD5'
PURPLE_L = '#C3AED6'
PURPLE_M = '#B39DDB'
GREEN_L = '#A8D5BA'
GREEN_M = '#81C784'
YELLOW_L = '#FFE0A3'
YELLOW_M = '#FFD54F'
RED_L = '#F4A7A7'
RED_M = '#EF9A9A'
GRAY_L = '#E0E0E0'
GRAY_M = '#BDBDBD'
WHITE = '#FFFFFF'
DARK = '#333333'


def save_fig(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, format='svg', bbox_inches='tight', dpi=300,
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  -> {name}")


def rounded_box(ax, x, y, w, h, color, text, fontsize=11, text_color=DARK):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor=DARK,
                         linewidth=0.8, zorder=2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, fontweight='bold', zorder=3)


# ============================================================
# 1. digital-humanities-timeline.svg
# ============================================================
def diagram_01():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 2.5)
    ax.axis('off')
    ax.set_title('디지털 인문학 발전 타임라인', fontsize=14, fontweight='bold', pad=15)

    eras = [
        (0.5, '2000s', '디지털 아카이브\n전자 텍스트 구축', BLUE_L),
        (3.0, '2010s', '빅데이터 분석\n텍스트 마이닝', PURPLE_L),
        (5.5, '2020s', '생성형 AI\nLLM 등장', GREEN_L),
        (8.0, '현재', 'AI와 인문학 협업\n바이브 코딩', YELLOW_L),
    ]

    for i, (x, era, desc, color) in enumerate(eras):
        circle = plt.Circle((x + 0.5, 1.8), 0.35, color=color, ec=DARK, lw=1, zorder=3)
        ax.add_patch(circle)
        ax.text(x + 0.5, 1.8, era, ha='center', va='center', fontsize=9, fontweight='bold', zorder=4)
        ax.text(x + 0.5, 0.7, desc, ha='center', va='center', fontsize=9, color=DARK)
        if i < len(eras) - 1:
            ax.annotate('', xy=(eras[i+1][0], 1.8), xytext=(x + 1.0, 1.8),
                        arrowprops=dict(arrowstyle='->', color=GRAY_M, lw=1.5))

    save_fig(fig, 'digital-humanities-timeline.svg')


# ============================================================
# 2. ai-hierarchy-pyramid.svg
# ============================================================
def diagram_02():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.5, 5)
    ax.axis('off')
    ax.set_title('AI 기술 계층 구조', fontsize=14, fontweight='bold', pad=15)

    layers = [
        (-4, 0, 8, 1.0, BLUE_L, '인공지능 (AI)', '사람의 지능을 모방하는 모든 기술'),
        (-3, 1.1, 6, 1.0, PURPLE_L, '머신러닝 (ML)', '데이터에서 패턴을 학습'),
        (-2, 2.2, 4, 1.0, GREEN_L, '딥러닝 (DL)', '인공 신경망으로 복잡한 패턴 학습'),
        (-1, 3.3, 2, 1.0, YELLOW_L, 'LLM', '대규모 언어모델'),
    ]

    for x, y, w, h, color, label, desc in layers:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor=DARK, linewidth=0.8)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2 + 0.1, label, ha='center', va='center',
                fontsize=12, fontweight='bold', color=DARK)
        ax.text(x + w/2, y + h/2 - 0.2, desc, ha='center', va='center',
                fontsize=9, color='#555555')

    save_fig(fig, 'ai-hierarchy-pyramid.svg')


# ============================================================
# 3. ai-landscape-grid.svg
# ============================================================
def diagram_03():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 5.5)
    ax.axis('off')
    ax.set_title('AI가 바꾸는 인문학 4영역', fontsize=14, fontweight='bold', pad=15)

    cards = [
        (0.5, 3, '글쓰기와 창작', 'AI와 함께 소설, 시,\n에세이를 쓰고\n문체를 실험', BLUE_L),
        (5.0, 3, '텍스트 분석', '수천 편의 문학 작품을\n분석하고 패턴을 발견', PURPLE_L),
        (0.5, 0.2, '번역과 소통', '언어의 장벽을 넘어\n다양한 문화를 탐색', GREEN_L),
        (5.0, 0.2, '시각적 스토리텔링', '텍스트를 이미지로 변환\n새로운 표현 방식 탐구', YELLOW_L),
    ]

    for x, y, title, desc, color in cards:
        box = FancyBboxPatch((x, y), 3.8, 2.2, boxstyle="round,pad=0.2",
                             facecolor=color, edgecolor=DARK, linewidth=0.8)
        ax.add_patch(box)
        ax.text(x + 1.9, y + 1.7, title, ha='center', va='center',
                fontsize=12, fontweight='bold', color=DARK)
        ax.text(x + 1.9, y + 0.8, desc, ha='center', va='center',
                fontsize=9, color='#555555')

    save_fig(fig, 'ai-landscape-grid.svg')


# ============================================================
# 4. search-vs-generative.svg
# ============================================================
def diagram_04():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    ax.set_title('검색 AI vs 생성형 AI', fontsize=14, fontweight='bold', pad=15)

    # 검색 AI
    rounded_box(ax, 0, 1.0, 4.5, 2.0, BLUE_L, '', fontsize=10)
    ax.text(2.25, 2.5, '검색 AI', ha='center', va='center', fontsize=13, fontweight='bold', color=BLUE_D)
    ax.text(2.25, 1.9, '기존 정보를 찾아서 보여줌', ha='center', va='center', fontsize=9, color=DARK)
    ax.text(2.25, 1.4, '사용자가 직접 읽고\n원하는 정보를 골라야 함', ha='center', va='center', fontsize=9, color='#666')

    # 화살표
    ax.annotate('', xy=(6.0, 2.0), xytext=(5.0, 2.0),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2))
    ax.text(5.5, 2.4, 'vs', ha='center', va='center', fontsize=14, fontweight='bold', color=DARK)

    # 생성형 AI
    rounded_box(ax, 6.5, 1.0, 4.5, 2.0, GREEN_L, '', fontsize=10)
    ax.text(8.75, 2.5, '생성형 AI', ha='center', va='center', fontsize=13, fontweight='bold', color='#2E7D32')
    ax.text(8.75, 1.9, '질문을 이해하고 답변을 생성', ha='center', va='center', fontsize=9, color=DARK)
    ax.text(8.75, 1.4, '대화하듯 추가 질문으로\n답변을 개선', ha='center', va='center', fontsize=9, color='#666')

    # 핵심 차이
    rounded_box(ax, 2.5, -0.3, 6.0, 0.8, YELLOW_L, "핵심: '찾아준다' vs '만들어준다'", fontsize=10)

    save_fig(fig, 'search-vs-generative.svg')


# ============================================================
# 5. ml-era-timeline.svg
# ============================================================
def diagram_05():
    fig, ax = plt.subplots(figsize=(11, 3.5))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, 3)
    ax.axis('off')
    ax.set_title('ML/AI 시대 구분', fontsize=14, fontweight='bold', pad=15)

    eras = [
        (0.2, 'Classical ML\n1990~2010s', 'SVM, Random Forest\n정형 데이터 중심', BLUE_L),
        (3.8, '전환점\n2017~2022', 'Transformer 등장\nGPT, ChatGPT', PURPLE_L),
        (7.4, 'LLM 시대\n2020s~', '텍스트 생성 중심\n멀티모달, 바이브 코딩', GREEN_L),
    ]

    for x, era, desc, color in eras:
        box = FancyBboxPatch((x, 0.3), 3.2, 2.3, boxstyle="round,pad=0.15",
                             facecolor=color, edgecolor=DARK, linewidth=0.8)
        ax.add_patch(box)
        ax.text(x + 1.6, 2.0, era, ha='center', va='center', fontsize=10, fontweight='bold', color=DARK)
        ax.text(x + 1.6, 1.0, desc, ha='center', va='center', fontsize=9, color='#555')

    for x1, x2 in [(3.4, 3.8), (7.0, 7.4)]:
        ax.annotate('', xy=(x2, 1.5), xytext=(x1, 1.5),
                    arrowprops=dict(arrowstyle='->', color=GRAY_M, lw=2))

    save_fig(fig, 'ml-era-timeline.svg')


# ============================================================
# 6. data-evolution-flow.svg
# ============================================================
def diagram_06():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    ax.set_title('정형 데이터에서 비정형 데이터로', fontsize=14, fontweight='bold', pad=15)

    # 정형 데이터
    rounded_box(ax, 0.3, 1.0, 3.5, 2.0, BLUE_L, '', fontsize=10)
    ax.text(2.05, 2.5, '정형 데이터', ha='center', va='center', fontsize=12, fontweight='bold', color=DARK)
    ax.text(2.05, 1.7, '숫자, 표, 거래 기록\n회귀, 분류, 시계열', ha='center', va='center', fontsize=9, color='#555')

    # 화살표
    ax.annotate('', xy=(5.2, 2.0), xytext=(4.2, 2.0),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2))
    ax.text(4.7, 2.5, '전환', ha='center', va='center', fontsize=10, fontweight='bold', color=DARK)

    # 비정형 데이터
    rounded_box(ax, 5.5, 1.0, 4.5, 2.0, GREEN_L, '', fontsize=10)
    ax.text(7.75, 2.5, '비정형 데이터', ha='center', va='center', fontsize=12, fontweight='bold', color=DARK)
    ax.text(7.75, 1.7, '텍스트, 이미지, 음성\n생성, 대화, 멀티모달', ha='center', va='center', fontsize=9, color='#555')

    # 핵심
    rounded_box(ax, 2.0, -0.2, 6.5, 0.8, YELLOW_L, '데이터의 종류가 AI의 가능성을 결정한다', fontsize=10)

    save_fig(fig, 'data-evolution-flow.svg')


# ============================================================
# 7. ai-working-principle.svg
# ============================================================
def diagram_07():
    fig, ax = plt.subplots(figsize=(11, 3.5))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.3, 3)
    ax.axis('off')
    ax.set_title('생성형 AI 작동 원리 4단계', fontsize=14, fontweight='bold', pad=15)

    steps = [
        (0.2, '1단계', '대량의 텍스트\n학습', BLUE_L),
        (2.9, '2단계', '다음 단어\n예측 능력', PURPLE_L),
        (5.6, '3단계', '사용자 질문에\n답변 생성', GREEN_L),
        (8.3, '4단계', '대화로\n답변 개선', YELLOW_L),
    ]

    for x, step, desc, color in steps:
        box = FancyBboxPatch((x, 0.3), 2.3, 2.2, boxstyle="round,pad=0.15",
                             facecolor=color, edgecolor=DARK, linewidth=0.8)
        ax.add_patch(box)
        ax.text(x + 1.15, 2.0, step, ha='center', va='center', fontsize=11, fontweight='bold', color=DARK)
        ax.text(x + 1.15, 1.0, desc, ha='center', va='center', fontsize=9, color='#555')

    for x in [2.5, 5.2, 7.9]:
        ax.annotate('', xy=(x + 0.4, 1.4), xytext=(x, 1.4),
                    arrowprops=dict(arrowstyle='->', color=GRAY_M, lw=2))

    save_fig(fig, 'ai-working-principle.svg')


# ============================================================
# 8. data-misconceptions.svg
# ============================================================
def diagram_08():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 5)
    ax.axis('off')
    ax.set_title('데이터에 대한 오해', fontsize=14, fontweight='bold', pad=15)

    # 오해 1
    rounded_box(ax, 0.3, 3.0, 8.8, 1.5, RED_L, '', fontsize=10)
    ax.text(1.5, 4.0, 'X  오해 1', ha='left', va='center', fontsize=12, fontweight='bold', color='#C62828')
    ax.text(1.5, 3.4, '데이터 양이 늘어나면 다양성도 늘어난다?\n-> 같은 종류만 쌓이면 편향이 커진다', ha='left', va='center', fontsize=9, color=DARK)

    # 오해 2
    rounded_box(ax, 0.3, 1.0, 8.8, 1.5, RED_L, '', fontsize=10)
    ax.text(1.5, 2.0, 'X  오해 2', ha='left', va='center', fontsize=12, fontweight='bold', color='#C62828')
    ax.text(1.5, 1.4, '모델이 커지면 현실을 더 잘 이해한다?\n-> 모델 크기와 세상에 대한 이해는 별개', ha='left', va='center', fontsize=9, color=DARK)

    # 시사점
    rounded_box(ax, 1.5, -0.3, 6.5, 0.8, GREEN_L, '어떤 데이터를 선택하느냐는 가치 판단의 문제', fontsize=10)

    save_fig(fig, 'data-misconceptions.svg')


# ============================================================
# 9. prompt-4-principles.svg
# ============================================================
def diagram_09():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 6)
    ax.axis('off')
    ax.set_title('프롬프트 4원칙', fontsize=14, fontweight='bold', pad=15)

    principles = [
        (0.5, 4.2, '01 구체적으로', '원하는 것을\n정확히 표현', BLUE_L),
        (5.0, 4.2, '02 맥락 제공', '나의 상황과\n배경 정보 전달', PURPLE_L),
        (0.5, 1.5, '03 역할 부여', 'AI에게\n전문가 역할 부여', GREEN_L),
        (5.0, 1.5, '04 출력 형식', '답변의 형태를\n명시', YELLOW_L),
    ]

    for x, y, title, desc, color in principles:
        box = FancyBboxPatch((x, y), 3.8, 2.0, boxstyle="round,pad=0.2",
                             facecolor=color, edgecolor=DARK, linewidth=0.8)
        ax.add_patch(box)
        ax.text(x + 1.9, y + 1.5, title, ha='center', va='center',
                fontsize=12, fontweight='bold', color=DARK)
        ax.text(x + 1.9, y + 0.6, desc, ha='center', va='center',
                fontsize=10, color='#555')

    # 중앙 레이블
    center = plt.Circle((4.65, 3.6), 0.5, color=YELLOW_M, ec=DARK, lw=1.2, zorder=5)
    ax.add_patch(center)
    ax.text(4.65, 3.6, '4원칙', ha='center', va='center', fontsize=11, fontweight='bold', zorder=6)

    save_fig(fig, 'prompt-4-principles.svg')


# ============================================================
# 10. prompt-before-after.svg
# ============================================================
def diagram_10():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    ax.set_title('Before / After 프롬프트 비교', fontsize=14, fontweight='bold', pad=15)

    # Before
    rounded_box(ax, 0.3, 0.5, 4.3, 2.5, RED_L, '', fontsize=10)
    ax.text(2.45, 2.5, 'Before', ha='center', va='center', fontsize=14, fontweight='bold', color='#C62828')
    ax.text(2.45, 1.8, "'요약해줘'", ha='center', va='center', fontsize=11, color=DARK)
    ax.text(2.45, 1.1, '모호함, 길이 불명\n관점 불명, 임의 해석', ha='center', va='center', fontsize=9, color='#666')

    # 화살표
    ax.annotate('', xy=(5.7, 1.75), xytext=(5.0, 1.75),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2.5))

    # After
    rounded_box(ax, 5.9, 0.5, 4.3, 2.5, GREEN_L, '', fontsize=10)
    ax.text(8.05, 2.5, 'After', ha='center', va='center', fontsize=14, fontweight='bold', color='#2E7D32')
    ax.text(8.05, 1.8, "'3문장으로 요약하고\n키워드 3개를 뽑아줘'", ha='center', va='center', fontsize=10, color=DARK)
    ax.text(8.05, 0.9, '길이 명시, 추가 정보\n적절한 난이도', ha='center', va='center', fontsize=9, color='#666')

    save_fig(fig, 'prompt-before-after.svg')


# ============================================================
# 11. tone-combination-formula.svg
# ============================================================
def diagram_11():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    ax.set_title('말투 조합 공식', fontsize=14, fontweight='bold', pad=15)

    elements = [
        (0.3, '화자', BLUE_L),
        (2.3, '독자', PURPLE_L),
        (4.3, '종결 어미', GREEN_L),
        (6.3, '비유 여부', YELLOW_L),
    ]

    for x, label, color in elements:
        box = FancyBboxPatch((x, 1.5), 1.6, 1.5, boxstyle="round,pad=0.15",
                             facecolor=color, edgecolor=DARK, linewidth=0.8)
        ax.add_patch(box)
        ax.text(x + 0.8, 2.25, label, ha='center', va='center',
                fontsize=11, fontweight='bold', color=DARK)

    # + 기호들
    for x in [2.0, 4.0, 6.0]:
        ax.text(x + 0.15, 2.25, '+', ha='center', va='center', fontsize=16, fontweight='bold', color=DARK)

    # = 기호
    ax.text(8.25, 2.25, '=', ha='center', va='center', fontsize=18, fontweight='bold', color=DARK)

    # 결과
    box = FancyBboxPatch((8.6, 1.3), 1.6, 1.9, boxstyle="round,pad=0.15",
                         facecolor=YELLOW_M, edgecolor=DARK, linewidth=1.2)
    ax.add_patch(box)
    ax.text(9.4, 2.25, '말투\n결정!', ha='center', va='center',
            fontsize=12, fontweight='bold', color=DARK)

    # 아래 설명
    ax.text(5.0, 0.5, '이 네 가지를 조합하면 같은 내용도 완전히 다른 글이 됩니다',
            ha='center', va='center', fontsize=10, color='#555', style='italic')

    save_fig(fig, 'tone-combination-formula.svg')


# ============================================================
# 12. six-tones-radar.svg
# ============================================================
def diagram_12():
    categories = ['친근감', '전문성', '격식', '설득력', '객관성', '간결함']
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    tones = {
        'A. 강의형': ([5, 3, 2, 3, 2, 3], BLUE_L),
        'B. 경험자형': ([4, 4, 3, 4, 3, 3], PURPLE_L),
        'C. 보고서형': ([1, 5, 5, 3, 5, 2], GREEN_L),
        'D. 선배형': ([5, 2, 1, 2, 2, 5], YELLOW_L),
        'E. 마케팅형': ([3, 2, 3, 5, 2, 5], RED_L),
        'F. 기사형': ([2, 4, 4, 3, 5, 3], GRAY_L),
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
    ax.set_title('6가지 말투 레이더 차트', fontsize=14, fontweight='bold', pad=20)

    for name, (values, color) in tones.items():
        values_closed = values + values[:1]
        ax.plot(angles, values_closed, 'o-', linewidth=1.5, label=name, color=color)
        ax.fill(angles, values_closed, alpha=0.1, color=color)

    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=9)
    save_fig(fig, 'six-tones-radar.svg')


# ============================================================
# 13. ai-writing-problems.svg
# ============================================================
def diagram_13():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 5)
    ax.axis('off')
    ax.set_title('AI 글의 6가지 전형적 문제', fontsize=14, fontweight='bold', pad=15)

    problems = [
        (0.3, 3.2, '① 문장 단절', '짧고 끊긴 문장', RED_L),
        (3.6, 3.2, '② 문단 분절', '지나친 줄바꿈', RED_L),
        (6.9, 3.2, '③ 번역투', '영어 직역 표현', RED_L),
        (0.3, 0.8, '④ 슬롭 워드', 'AI 과용 단어', RED_L),
        (3.6, 0.8, '⑤ 종결 단조', '~합니다만 반복', RED_L),
        (6.9, 0.8, '⑥ 메타 해설', '투어 가이드 문장', RED_L),
    ]

    for x, y, title, desc, color in problems:
        box = FancyBboxPatch((x, y), 2.8, 1.8, boxstyle="round,pad=0.15",
                             facecolor=color, edgecolor='#C62828', linewidth=0.8)
        ax.add_patch(box)
        ax.text(x + 1.4, y + 1.2, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color='#B71C1C')
        ax.text(x + 1.4, y + 0.5, desc, ha='center', va='center',
                fontsize=9, color=DARK)

    save_fig(fig, 'ai-writing-problems.svg')


# ============================================================
# 14. multiturn-strategy.svg
# ============================================================
def diagram_14():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 5)
    ax.axis('off')
    ax.set_title('멀티턴 대화 전략', fontsize=14, fontweight='bold', pad=15)

    steps = [
        (0.5, 3.5, '첫 질문', '일반적인 질문으로 시작', BLUE_L),
        (0.5, 2.2, '범위 좁히기', "'그중에서 ~에 집중해줘'", PURPLE_L),
        (0.5, 0.9, '구체화', "'예를 들어 설명해줘'", GREEN_L),
    ]

    strategies = [
        (5.5, 3.5, '형식 바꾸기', "'표로 정리해줘'", YELLOW_L),
        (5.5, 2.2, '수준 조절', "'쉽게 설명해줘'", RED_L),
        (5.5, 0.9, '비판 요청', "'문제점을 지적해줘'", BLUE_L),
    ]

    for items in [steps, strategies]:
        for x, y, title, desc, color in items:
            box = FancyBboxPatch((x, y), 4.0, 1.0, boxstyle="round,pad=0.12",
                                 facecolor=color, edgecolor=DARK, linewidth=0.8)
            ax.add_patch(box)
            ax.text(x + 2.0, y + 0.65, title, ha='center', va='center',
                    fontsize=11, fontweight='bold', color=DARK)
            ax.text(x + 2.0, y + 0.25, desc, ha='center', va='center',
                    fontsize=9, color='#555')

    # 세로 화살표
    for y1, y2 in [(3.5, 3.2), (2.2, 1.9)]:
        ax.annotate('', xy=(2.5, y2), xytext=(2.5, y1),
                    arrowprops=dict(arrowstyle='->', color=GRAY_M, lw=1.5))

    ax.text(2.5, 4.8, '단계적 심화', ha='center', va='center', fontsize=12, fontweight='bold', color=DARK)
    ax.text(7.5, 4.8, '전략적 변환', ha='center', va='center', fontsize=12, fontweight='bold', color=DARK)

    save_fig(fig, 'multiturn-strategy.svg')


# ============================================================
# 15. ai-limitations-overview.svg
# ============================================================
def diagram_15():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    ax.set_title('AI의 5가지 한계', fontsize=14, fontweight='bold', pad=15)

    limits = [
        (0.3, '환각\n(Hallucination)', '사실이 아닌 정보를\n자신있게 답함', RED_L),
        (2.3, '최신 정보\n부족', '학습 데이터 이후\n정보를 모름', YELLOW_L),
        (4.3, '개인 경험\n부재', '자기만의 경험이나\n감정이 없음', BLUE_L),
        (6.3, '수학적\n추론 한계', '복잡한 계산에서\n실수', PURPLE_L),
        (8.3, '일관성\n부족', '같은 질문에\n다른 답변', GREEN_L),
    ]

    for x, title, desc, color in limits:
        box = FancyBboxPatch((x, 0.3), 1.7, 2.7, boxstyle="round,pad=0.12",
                             facecolor=color, edgecolor=DARK, linewidth=0.8)
        ax.add_patch(box)
        ax.text(x + 0.85, 2.4, title, ha='center', va='center',
                fontsize=9, fontweight='bold', color=DARK)
        ax.text(x + 0.85, 1.1, desc, ha='center', va='center',
                fontsize=8, color='#555')

    save_fig(fig, 'ai-limitations-overview.svg')


# ============================================================
# 16. book-roadmap.svg
# ============================================================
def diagram_16():
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, 5)
    ax.axis('off')
    ax.set_title('이 책의 로드맵', fontsize=14, fontweight='bold', pad=15)

    # Part I
    rounded_box(ax, 0.3, 3.2, 4.8, 1.5, BLUE_L, '', fontsize=10)
    ax.text(2.7, 4.2, 'Part I  AI와 인문학의 만남', ha='center', va='center',
            fontsize=11, fontweight='bold', color=DARK)
    ax.text(2.7, 3.6, '1장 AI와 인문학  |  2장 생성형 AI', ha='center', va='center',
            fontsize=9, color='#555')

    # Part II
    rounded_box(ax, 5.7, 3.2, 5.0, 1.5, GREEN_L, '', fontsize=10)
    ax.text(8.2, 4.2, 'Part II  AI와 대화하기', ha='center', va='center',
            fontsize=11, fontweight='bold', color=DARK)
    ax.text(8.2, 3.6, '3장 프롬프트  |  4장 말투  |  5장 평가', ha='center', va='center',
            fontsize=9, color='#555')

    # 화살표
    ax.annotate('', xy=(5.7, 3.95), xytext=(5.1, 3.95),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2))

    # 부록
    rounded_box(ax, 2.5, 0.8, 6.0, 1.5, YELLOW_L, '', fontsize=10)
    ax.text(5.5, 1.8, '부록', ha='center', va='center',
            fontsize=11, fontweight='bold', color=DARK)
    ax.text(5.5, 1.2, 'AI 도구 비교  |  프롬프트 템플릿  |  한국어 글쓰기 가이드', ha='center', va='center',
            fontsize=9, color='#555')

    # 하향 화살표
    ax.annotate('', xy=(5.5, 2.3), xytext=(5.5, 3.2),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=1.5))

    save_fig(fig, 'book-roadmap.svg')


# ============================================================
# 메인 실행
# ============================================================
if __name__ == '__main__':
    print("다이어그램 생성 시작...")
    funcs = [
        diagram_01, diagram_02, diagram_03, diagram_04,
        diagram_05, diagram_06, diagram_07, diagram_08,
        diagram_09, diagram_10, diagram_11, diagram_12,
        diagram_13, diagram_14, diagram_15, diagram_16,
    ]
    for i, fn in enumerate(funcs, 1):
        print(f"[{i:2d}/16] {fn.__name__}")
        fn()
    print(f"\n완료! {len(funcs)}개 다이어그램이 {OUTPUT_DIR}에 저장되었습니다.")
