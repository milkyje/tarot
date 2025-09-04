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
    
    # 세부 카테고리 선택 로직
    if main_category == "관계 고민":
        sub_categories = list(prompts_data.get(main_category, {}).keys())
        selected_category = st.selectbox("관계의 종류를 선택하세요:", options=sub_categories)
        user_input_label = f"'{selected_category}'에 대한 고민을 구체적으로 입력하세요:"
        if selected_category == "연애":
            placeholder_text = "지금 당신의 마음을 가장 흔드는 연애관계(짝사랑, 썸, 연인, 이별 등)와 그에 대한 구체적인 이야기를 편하게 들려주세요. 상세할 수록 정확한 리딩에 도움이 됩니다."
        elif selected_category == "대인관계":
            placeholder_text = "당신을 둘러싼 대인관계(가족,친구,동료,익명친구 등) 속에서 겪고 있는 어려움이나 궁금한 점을 편하게 이야기 해 주세요."
        elif selected_category == "기타":
            placeholder_text = "상대방이 인외입니까? 반려동물, 식물, 덕질상대 등과의 갈등이 있다면 이야기해 주세요."
    elif main_category == "커리어와 목표":
        sub_categories = list(prompts_data.get(main_category, {}).keys())
        selected_category = st.selectbox("목표의 종류를 선택하세요:", options=sub_categories)
        user_input_label = f"'{selected_category}'에 대한 고민을 구체적으로 입력하세요:"
        if selected_category == "금전운":
            placeholder_text = "당신의 금전운에 관한 고민을 구체적으로 이야기해 주세요. 예) '새로운 투자를 시작해도 될까요?', '지금 재정 상황은 어떨까요?'"
        elif selected_category == "직업운":
            placeholder_text = "당신의 직업에 관한 고민을 구체적으로 이야기해 주세요. 예) '이직을 결심해야 할까요?', '새로운 사업 기회는 어떨까요?'"
        elif selected_category == "학업운":
            placeholder_text = "학업에 대한 고민을 구체적으로 이야기해 주세요. 예) '어떤 전공을 선택해야 할까요?', '곧 있을 시험 합격 가능성은?'"
    elif main_category == "선택과 방향":
        sub_categories = list(prompts_data.get(main_category, {}).keys())
        selected_category = st.selectbox("결정의 종류를 선택하세요:", options=sub_categories)
        user_input_label = f"'{selected_category}'에 대한 고민을 구체적으로 입력하세요:"
        if selected_category == "우선순위 결정":
            placeholder_text = "여러 선택지 중 어떤 것을 먼저 해야 할지 고민이 있다면 각 선택지에 대한 상세한 이야기를 들려주세요. 예시) 여러 가지 할 일이 있는데, 어떤 것부터 처리해야 할까요?"
        elif selected_category == "타이밍 결정":
            placeholder_text = "어떤 일을 시작하거나 끝내야 할 최적의 시기를 고민한다면 그 상황을 구체적으로 이야기해 주세요."
        elif selected_category == "선택지 결정":
            placeholder_text = "여러 대안(예: A와 B) 중 어떤 것을 선택해야 할지 고민이 된다면, 각 대안의 장단점, 그리고 당신의 현재 상황에 대해 자세히 알려주세요."
    elif main_category == "자유로운 질문":
        selected_category = "자유로운 질문"
        user_input_label = "자유로운 질문을 입력하세요:"
        placeholder_text = "어떤 종류의 질문도 좋습니다. 예) '오늘의 운세는 어떨까요?', '제가 궁금한 그 질문에 대한 답을 주세요.'"

    user_input = st.text_area(user_input_label, placeholder=placeholder_text)
    
    st.subheader("스프레드 선택")
    
    # 수정된 부분: selected_category가 main_category와 다를 경우, 세부 카테고리로 필터링
    valid_categories = [main_category]
    if selected_category != main_category:
        valid_categories.append(selected_category)
    
    # '관계 고민_연애'와 같이 prompts.json에 정의된 특별한 카테고리를 위해 추가
    if f"{main_category}_{selected_category}" in [cat for info in spreads_data.values() for cat in info['categories']]:
        valid_categories.append(f"{main_category}_{selected_category}")
    
    valid_spreads = [
        name for name, info in spreads_data.items()
        if any(cat in valid_categories for cat in info['categories'])
    ]
    
    if not valid_spreads:
        st.warning("선택한 카테고리에 맞는 스프레드가 없습니다. 다른 카테고리를 선택해 주세요.")
    else:
        selected_spread_name = st.selectbox("원하는 타로 스프레드를 선택하세요:", options=valid_spreads)

        # 선택된 스프레드에 대한 정보
        spread_info = spreads_data.get(selected_spread_name)
        if spread_info:
            num_cards_to_draw = spread_info["num_cards"]
            positions_text = ", ".join(spread_info["positions"])
            st.info(f"선택한 스프레드는 **{num_cards_to_draw}장**의 카드를 사용합니다. 각 카드 위치의 의미는 다음과 같습니다: **{positions_text}**")
    
    # 3개 버튼을 가로로 정렬
    col1, col2, col3 = st.columns(3)

    # 1. 프롬프트 복사 버튼
    with col1:
        if st.button("프롬프트 복사", use_container_width=True):
            if user_input and 'selected_spread_name' in locals():
                st.session_state.last_user_input = user_input
                st.session_state.last_spread_name = selected_spread_name
                st.session_state.last_category = selected_category
                
                # 카드 뽑기
                drawn_cards = draw_cards(num_cards_to_draw, TAROT_DECK)
                st.session_state.last_cards = drawn_cards

                # 스프레드 정보에 맞는 프롬프트 템플릿 찾기
                try:
                    # '관계 고민' 중 '연애' 카테고리의 '아스타로트 스프레드'에 대한 특별 처리
                    if main_category == "관계 고민" and selected_category == "연애" and selected_spread_name == "아스타로드 스프레드":
                        prompt_template = prompts_data[main_category][selected_category]['templates'][selected_spread_name]
                        formatted_prompt = prompt_template.format(
                            relationship_type=selected_category, 
                            user_prompt=user_input, 
                            cards=drawn_cards
                        )
                    else:
                        prompt_template = prompts_data[main_category][selected_category]['templates'][selected_spread_name]
                        formatted_prompt = prompt_template.format(
                            user_prompt=user_input, 
                            cards=drawn_cards
                        )

                    st.session_state.last_ai_prompt = formatted_prompt
                    st.success("프롬프트가 생성되었습니다. 아래 내용을 복사하여 사용하세요.")
                    st.code(st.session_state.last_ai_prompt, language='markdown')
                except KeyError:
                    st.error("오류: 선택한 카테고리 또는 스프레드에 대한 프롬프트 템플릿을 찾을 수 없습니다.")
            else:
                st.warning("질문과 스프레드를 모두 선택하고 입력해주세요.")
                
    # 2. 리딩하기 버튼
    with col2:
        if st.button("리딩하기", use_container_width=True):
            if user_input and 'selected_spread_name' in locals():
                with st.spinner("타로 마스터가 카드를 뽑고 리딩하고 있습니다..."):
                    # 프롬프트 생성 후 리딩 진행
                    st.session_state.last_user_input = user_input
                    st.session_state.last_spread_name = selected_spread_name
                    st.session_state.last_category = selected_category
                    
                    drawn_cards = draw_cards(num_cards_to_draw, TAROT_DECK)
                    st.session_state.last_cards = drawn_cards
                    
                    ai_response, _ = get_ai_reading(
                        selected_category,
                        user_input,
                        [],
                        selected_spread_name,
                        drawn_cards,
                        prompts_data
                    )
                    st.session_state.last_ai_response = ai_response
                    st.session_state.show_results = True
                    st.rerun()
            else:
                st.warning("질문과 스프레드를 모두 선택하고 입력해주세요.")
    
    # 3. 초기화 버튼
    with col3:
        if st.button("초기화", use_container_width=True):
            reset_app()

# 리딩 결과를 보여주는 코드
if st.session_state.show_results:
    st.write(st.session_state.last_ai_response)
    st.markdown("---")
    
    # 추가 질문 기능
    st.subheader("추가 질문하기")
    follow_up_input = st.text_input("리딩 내용에 대해 더 궁금한 점이 있으신가요?", key="follow_up_input")
    
    if st.button("추가 질문하기"):
        with st.spinner("마스터가 답을 고민하고 있습니다..."):
            ai_response = get_follow_up_reading(
                st.session_state.last_ai_response,
                follow_up_input,
                st.session_state.last_ai_prompt,
                st.session_state.last_cards
            )
            st.session_state.last_ai_response = ai_response
            st.rerun()

    if st.button("새로운 질문하기"):
        reset_app()