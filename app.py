import streamlit as st
from config import TAROT_DECK
from tarot_data import load_spreads_data, load_prompts_data, draw_cards
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
if 'last_ai_response' not in st.session_state:
    st.session_state.last_ai_response = ""
if 'last_ai_prompt' not in st.session_state:
    st.session_state.last_ai_prompt = ""

def reset_app():
    """앱의 모든 상태를 초기화하고 첫 화면으로 돌아갑니다."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# 데이터 로딩
spreads_data = load_spreads_data()
prompts_data = load_prompts_data()

st.title("asTarot - 내가 보려고 만든")

# 메인 화면: 질문 입력
if not st.session_state.get('show_results', False):
    st.subheader("고민 카테고리 선택")
    
    # 1. 메인 카테고리 선택
    main_categories = list(prompts_data.keys())
    main_category = st.selectbox("고민의 큰 카테고리를 선택하세요:", options=main_categories)

    # 2. 세부 카테고리 설정
    sub_data = prompts_data.get(main_category, {})
    if "templates" in sub_data: # 자유로운 질문처럼 세부 카테고리가 없는 경우
        selected_category = main_category
        sub_categories = []
    else:
        sub_categories = list(sub_data.keys())
        selected_category = st.selectbox("세부 카테고리를 선택하세요:", options=sub_categories)

    # 질문 입력 가이드 설정
    placeholder_dict = {
        "연애": "지금 당신의 마음을 가장 흔드는 연애관계와 구체적인 이야기를 들려주세요.",
        "대인관계": "동료, 친구, 가족 관계에서 겪는 어려움을 이야기해 주세요.",
        "금전운": "투자, 재정 상황 등 금전에 관한 고민을 이야기해 주세요.",
        "직업운": "이직, 사업, 직무 고민 등을 상세히 적어주세요.",
        "자유로운 질문": "궁금한 점을 자유롭게 입력하세요."
    }
    placeholder_text = placeholder_dict.get(selected_category, "고민 내용을 구체적으로 입력할수록 리딩이 정확해집니다.")
    
    user_input = st.text_area(f"'{selected_category}'에 대한 고민을 입력하세요:", placeholder=placeholder_text)
    
    st.subheader("스프레드 선택")
    
    # 3. 스프레드 필터링 로직 (데이터 구조에 맞게 수정)
    valid_spreads = []
    for name, info in spreads_data.items():
        # 메인 카테고리가 포함되어 있거나, 특수 케이스(관계 고민_연애) 대응
        if main_category in info["categories"] or f"{main_category}_{selected_category}" in info["categories"]:
            valid_spreads.append(name)

    if not valid_spreads:
        st.warning("선택한 카테고리에 맞는 스프레드가 없습니다.")
    else:
        selected_spread_name = st.selectbox("원하는 타로 스프레드를 선택하세요:", options=valid_spreads)
        spread_info = spreads_data[selected_spread_name]
        
        # 카드 위치 정보 출력 (중첩 리스트 처리)
        pos_data = spread_info["positions"]
        if isinstance(pos_data[0], list):
            # 쓰리 카드처럼 여러 줄인 경우 합쳐서 보여줌
            flat_positions = [item for sublist in pos_data for item in sublist]
            positions_text = ", ".join(flat_positions)
        else:
            positions_text = ", ".join(pos_data)
            
        st.info(f"**{spread_info['num_cards']}장**의 카드를 사용합니다.\n\n위치: {positions_text}")

    # 버튼 레이아웃
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("프롬프트 복사", use_container_width=True):
            if user_input and 'selected_spread_name' in locals():
                drawn_cards = draw_cards(spread_info["num_cards"], TAROT_DECK)
                st.session_state.last_cards = drawn_cards
                
                # 템플릿 가져오기 (경로 유연하게 처리)
                try:
                    if "templates" in sub_data:
                        template = sub_data["templates"][selected_spread_name]
                    else:
                        template = sub_data[selected_category]["templates"][selected_spread_name]
                    
                    formatted_prompt = template.format(
                        user_prompt=user_input,
                        cards=", ".join(drawn_cards),
                        relationship_type=selected_category
                    )
                    st.session_state.last_ai_prompt = formatted_prompt
                    st.success("프롬프트 생성 완료!")
                    st.code(formatted_prompt, language='markdown')
                except KeyError:
                    st.error("해당 조합의 프롬프트 템플릿을 찾을 수 없습니다. (이름 오타 확인 필요)")

    with col2:
        if st.button("리딩하기", use_container_width=True):
            if user_input and 'selected_spread_name' in locals():
                with st.spinner("카드를 섞고 리딩을 준비 중입니다..."):
                    st.session_state.last_user_input = user_input
                    st.session_state.last_spread_name = selected_spread_name
                    st.session_state.last_category = selected_category
                    
                    drawn_cards = draw_cards(spread_info["num_cards"], TAROT_DECK)
                    st.session_state.last_cards = drawn_cards
                    
                    ai_response, _ = get_ai_reading(
                        selected_category,
                        user_input,
                        [], # 이전 대화 기록
                        selected_spread_name,
                        drawn_cards,
                        prompts_data
                    )
                    st.session_state.last_ai_response = ai_response
                    st.session_state.show_results = True
                    st.rerun()

    with col3:
        if st.button("초기화", use_container_width=True):
            reset_app()

# 4. 결과 출력 화면
if st.session_state.get('show_results', False):
    st.subheader("타로 리딩 결과")
    st.markdown(st.session_state.last_ai_response)
    
    with st.expander("뽑힌 카드 확인"):
        st.write(", ".join(st.session_state.last_cards))

    st.markdown("---")
    
    # 추가 질문
    follow_up_input = st.text_input("리딩 내용에 대해 더 궁금한 점이 있나요?")
    if st.button("추가 질문하기"):
        if follow_up_input:
            with st.spinner("마스터가 답을 고민 중입니다..."):
                new_response = get_follow_up_reading(
                    st.session_state.last_ai_response,
                    follow_up_input,
                    st.session_state.last_ai_prompt,
                    st.session_state.last_cards
                )
                st.session_state.last_ai_response = new_response
                st.rerun()

    if st.button("처음으로 돌아가기"):
        reset_app()
