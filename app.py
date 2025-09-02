import streamlit as st
from config import TAROT_DECK
from tarot_data import load_spreads_data, load_prompts_data, draw_cards, get_spread_info_from_display_name
from tarot_ai import get_ai_reading, get_follow_up_reading
import json

# 세션 상태 초기화
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'last_cards' not in st.session_state:
    st.session_state.last_cards = []
if 'last_user_input' not in st.session_state:
    st.session_state.last_user_input = ""
if 'last_spread_name' not in st.session_state:
    st.session_state.last_spread_name = ""
if 'last_category' not in st.session_state:
    st.session_state.last_category = ""
if 'last_choices' not in st.session_state:
    st.session_state.last_choices = []
if 'last_ai_response' not in st.session_state:
    st.session_state.last_ai_response = ""
if 'last_ai_prompt' not in st.session_state:
    st.session_state.last_ai_prompt = ""

def reset_app():
    """앱의 모든 상태를 초기화하고 첫 화면으로 돌아갑니다."""
    st.session_state.show_results = False
    st.session_state.last_cards = []
    st.session_state.last_user_input = ""
    st.session_state.last_spread_name = ""
    st.session_state.last_category = ""
    st.session_state.last_choices = []
    st.session_state.last_ai_response = ""
    st.session_state.last_ai_prompt = ""
    st.rerun()

# 데이터 로딩
spreads_data = load_spreads_data()
prompts_data = load_prompts_data()

st.title("asTarot - 내가 보려고 만든")

# 메인 화면: 질문 입력
if not st.session_state.show_results:
    st.subheader("고민 카테고리 선택")
    main_categories = list(prompts_data.keys())
    main_category = st.selectbox("고민의 큰 카테고리를 선택하세요:", options=main_categories)

    selected_category = main_category
    user_input_label = ""
    placeholder_text = ""

    if main_category == "관계":
        sub_categories = list(prompts_data.get(main_category, {}).keys())
        selected_category = st.selectbox("관계의 종류를 선택하세요:", options=sub_categories)
        user_input_label = f"'{selected_category}'에 대한 고민을 구체적으로 입력하세요:"
        if selected_category == "연애":
            placeholder_text = "예시) 남자친구와 자꾸 싸우는데, 이 관계를 계속 유지하는 게 맞을까요?"
        elif selected_category == "대인관계":
            placeholder_text = "예시) 직장 상사와 관계가 어려운데, 어떻게 풀어나가야 할까요?"

    elif main_category == "성공":
        sub_categories = list(prompts_data.get(main_category, {}).keys())
        selected_category = st.selectbox("성공의 종류를 선택하세요:", options=sub_categories)
        user_input_label = f"'{selected_category}'에 대한 고민을 구체적으로 입력하세요:"
        if selected_category == "금전운":
            placeholder_text = "예시) 새로 시작한 사업의 금전운이 궁금합니다."
        elif selected_category == "직업운":
            placeholder_text = "예시) 지금 직장을 계속 다니는 것이 좋을까요, 아니면 이직을 시도해 볼까요?"
        elif selected_category == "학업운":
            placeholder_text = "예시) 이번 시험을 잘 보려면 어떤 공부 방법을 택해야 할까요?"
    
    elif main_category == "결정":
        sub_categories = list(prompts_data.get(main_category, {}).keys())
        selected_category = st.selectbox("결정의 종류를 선택하세요:", options=sub_categories)
        user_input_label = f"'{selected_category}'에 대한 고민을 구체적으로 입력하세요:"
        if selected_category == "우선순위 결정":
            placeholder_text = "예시) 여러 가지 할 일이 있는데, 어떤 것부터 처리해야 할까요?"
        elif selected_category == "타이밍 결정":
            placeholder_text = "예시) 이직을 하기로 마음먹었는데, 언제 시도하는 것이 좋을까요?"
        elif selected_category == "포기 여부 결정":
            placeholder_text = "예시) 이 프로젝트를 계속 진행해야 할지, 아니면 포기하는 것이 좋을지 궁금합니다."
        elif selected_category == "접근 방식 결정":
            placeholder_text = "예시) 목표는 정해졌는데, 어떤 방식으로 접근해야 성공할 수 있을까요?"
        elif selected_category == "가치 판단 및 윤리적 결정":
            placeholder_text = "예시) 갈등 상황에서 어떤 가치에 우선순위를 두는 것이 옳은 결정일까요?"

    elif main_category == "탐색":
        selected_category = "탐색"
        user_input_label = "삶의 의미, 내면 탐구, 영성 등 근원적인 고민에 대해 자유롭게 입력하세요:"
        placeholder_text = "예시) 제 잠재된 재능은 무엇이고, 어떻게 발견할 수 있을까요?"
    
    elif main_category == "다중 선택":
        selected_category = "다중 선택"
        user_input_label = "선택지를 입력하기 전에, 먼저 당신이 처한 상황을 구체적으로 입력하세요:"
        placeholder_text = "예시) A와 B 중 어떤 것을 선택해야 할지 고민입니다."

    if main_category != "해당 카테고리에 맞는 질문을 골라주세요":
        user_input = st.text_area(user_input_label, height=150, placeholder=placeholder_text)
    
    # 스프레드 선택 로직
    spread_options_map = {}
    if main_category == "다중 선택":
        # '다중 선택' 카테고리에는 '다중선택 스프레드'만 허용
        spread_options_map["다중선택 스프레드"] = "다중선택 스프레드"
    elif selected_category == "연애":
        # '연애' 카테고리에는 '집시의 십자' 스프레드 추가
        all_spreads = list(spreads_data.keys())
        for spread in all_spreads:
            if selected_category in spreads_data[spread].get("categories", []):
                spread_options_map[spread] = spread
    else:
        # 그 외 모든 카테고리에는 '집시의 십자'와 '다중선택 스프레드'를 제외
        all_spreads = list(spreads_data.keys())
        for spread in all_spreads:
            if selected_category in spreads_data[spread].get("categories", []) and spread not in ["집시의 십자", "다중선택 스프레드"]:
                spread_options_map[spread] = spread

    spread_display_names = list(spread_options_map.keys())

    spread_name = st.selectbox(
        "사용할 스프레드를 선택하세요:",
        options=spread_display_names,
        help="스프레드를 선택하면 리딩에 사용되는 카드 수와 위치별 의미가 달라집니다."
    )

    choices = []
    if spread_name == "다중선택 스프레드":
        st.subheader("선택지 입력")
        num_choices = st.number_input("선택지 개수", min_value=2, max_value=5, value=2, step=1)
