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

# 데이터 로딩
spreads_data = load_spreads_data()
prompts_data = load_prompts_data()

st.title("타로 리더")

# 초기화 버튼 추가
if st.session_state.show_results:
    if st.button("새로운 질문하기"):
        reset_app()
        st.experimental_rerun()

# 메인 화면 UI (결과가 없을 때만 표시)
if not st.session_state.show_results:
    with st.sidebar:
        st.header("타로 리딩 설정")

        # 1. 메인 카테고리 선택
        main_categories = list(prompts_data.keys())
        main_category = st.selectbox("고민 카테고리:", options=main_categories)

        # 2. 하위 카테고리 선택 (관계, 성공, 결정 카테고리)
        selected_category = main_category

        if main_category == "관계":
            sub_categories = list(prompts_data.get(main_category, {}).keys())
            selected_category = st.selectbox("관계의 종류:", options=sub_categories)

        elif main_category == "결정":
            sub_categories = list(prompts_data.get(main_category, {}).keys())
            selected_category = st.selectbox("결정의 종류:", options=sub_categories)

        elif main_category == "성공":
            sub_categories = list(prompts_data.get(main_category, {}).keys())
            selected_category = st.selectbox("성공의 종류:", options=sub_categories)
        
        # 스프레드 선택 기능
        spread_options = []
        if selected_category == "다중 선택":
            spread_options = ["다중선택 스프레드"]
        else:
            for spread_name, spread_info in spreads_data.items():
                if selected_category in spread_info.get("categories", []):
                    spread_options.append(f"{spread_name} ({spread_info['num_cards']}장)")
        
        spread_display_name = st.selectbox("사용할 스프레드를 선택하세요:", options=spread_options)
        
    # 고민 입력 UI
    st.markdown("---")
    st.subheader("당신의 고민을 이야기해주세요.")
    placeholder_text = prompts_data.get(selected_category, {}).get("placeholder", "고민을 입력해주세요. 구체적으로 작성할수록 정확한 리딩을 받을 수 있습니다.")
    
    user_input = st.text_area(
        "고민을 입력해주세요. 구체적으로 작성할수록 정확한 리딩을 받을 수 있습니다.",
        value="",
        height=150,
        placeholder=placeholder_text
    )

    # '다중 선택' 카테고리일 때만 선택지 입력란 표시
    choices = []
    if selected_category == "다중 선택":
        st.subheader("선택지 입력")
        num_choices = st.number_input("선택지 개수", min_value=2, max_value=5, value=2, step=1)
        
        for i in range(num_choices):
            choice = st.text_input(f"선택지 {i + 1}", key=f"choice_{i}", placeholder=f"예시) 선택지 {i + 1}에 대한 구체적인 내용")
            if choice:
                choices.append(choice)
    
    # 리딩 시작 버튼
    if st.button("리딩 시작"):
        if not user_input:
            st.warning("고민을 입력해주세요.")
        elif selected_category == "다중 선택" and len(choices) < 2:
            st.warning("선택지를 2개 이상 입력해주세요.")
        else:
            st.session_state.show_results = True
            st.session_state.last_category = selected_category
            st.session_state.last_user_input = user_input
            st.session_state.last_choices = choices
            st.session_state.last_spread_name = spread_display_name
            st.experimental_rerun()

# 결과 화면
if st.session_state.show_results:
    st.subheader(f"선택한 스프레드: {st.session_state.last_spread_name}")
    st.subheader("뽑은 카드")

    # 스프레드 이름으로 정보 가져오기
    spread_name, spread_info = get_spread_info_from_display_name(st.session_state.last_spread_name, spreads_data)
    num_cards = spread_info["num_cards"]
    positions = spread_info["positions"]

    # 카드 뽑기
    cards = draw_cards(TAROT_DECK, num_cards, spread_name)
    st.session_state.last_cards = cards

    # 카드 이미지 표시
    cols = st.columns(min(num_cards, 5))
    for i, card in enumerate(cards):
        with cols[i % 5]:
            st.image(f"https://tarot-images.s3.ap-northeast-2.amazonaws.com/{card}.png", caption=f"{i+1}. {positions[i] if i < len(positions) else '카드'} - {card}")

    st.markdown("---")
    
    st.subheader("타로 리딩 결과")
    with st.spinner('AI가 카드를 해석하고 있어요...'):
        ai_response, raw_prompt = get_ai_reading(
            st.session_state.last_category, 
            st.session_state.last_user_input, 
            st.session_state.last_choices, 
            spread_name, 
            st.session_state.last_cards, 
            prompts_data
        )
        st.session_state.last_ai_response = ai_response
        st.session_state.last_ai_prompt = raw_prompt
        st.write(ai_response)
        
    st.markdown("---")

    # 프롬프트 보여주기
    with st.expander("Gemini 1.5에 전달된 프롬프트 보기"):
        st.code(st.session_state.last_ai_prompt, language='markdown')

    st.markdown("---")

    # 추가 질문 기능
    follow_up_input = st.text_input("리딩 내용에 대해 더 궁금한 점이 있으신가요?", key="follow_up_input")
    if st.button("추가 질문하기", disabled=not follow_up_input):
        with st.spinner("타로 마스터가 추가 질문에 답하고 있습니다..."):
            follow_up_response = get_follow_up_reading(
                st.session_state.last_ai_response,
                st.session_state.last_user_input,
                st.session_state.last_cards,
                follow_up_input
            )
            st.markdown(f"**타로 마스터의 답변:**\\n{follow_up_response}")