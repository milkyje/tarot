import streamlit as st
from config import TAROT_DECK
from tarot_data import load_spreads_data, load_prompts_data, draw_cards
from tarot_ai import get_ai_reading, get_follow_up_reading
import json

# --- 1. 세션 상태 관리 (초기화) ---
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'last_cards' not in st.session_state:
    st.session_state.last_cards = []
if 'last_ai_response' not in st.session_state:
    st.session_state.last_ai_response = ""
if 'last_prompt' not in st.session_state:
    st.session_state.last_prompt = ""

def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- 2. 데이터 로딩 ---
spreads_data = load_spreads_data()
prompts_data = load_prompts_data()

st.title("asTarot - 아스타로트 마스터")

# --- 3. 메인 로직 (입력 화면) ---
if not st.session_state.show_results:
    st.subheader("고민 카테고리 선택")
    
    # 카테고리 선택
    main_categories = list(prompts_data.keys())
    main_category = st.selectbox("큰 카테고리를 선택하세요:", options=main_categories)

    sub_data = prompts_data.get(main_category, {})
    if "templates" in sub_data:
        selected_category = main_category
    else:
        sub_categories = list(sub_data.keys())
        selected_category = st.selectbox("세부 카테고리를 선택하세요:", options=sub_categories)

    user_input = st.text_area("고민 내용을 상세히 입력하세요:", placeholder="상황을 구체적으로 적을수록 리딩이 정확해집니다.")
    
    st.subheader("스프레드 선택")
    
    # JSON의 categories 리스트를 기반으로 필터링
    valid_spreads = []
    for name, info in spreads_data.items():
        if main_category in info["categories"] or f"{main_category}_{selected_category}" in info["categories"]:
            valid_spreads.append(name)

    if not valid_spreads:
        st.warning("선택한 카테고리에 맞는 스프레드가 없습니다.")
    else:
        # 스프레드 선택
        selected_spread_name = st.selectbox("원하는 스프레드를 선택하세요:", options=valid_spreads)
        
        # 선택된 스프레드 정보 미리보기 (안전하게 가져오기)
        s_info = spreads_data.get(selected_spread_name)
        if s_info:
            num_cards = s_info.get("num_cards", 0)
            st.info(f"🔮 **{selected_spread_name}**: 총 {num_cards}장의 카드를 사용합니다.")

        # --- 버튼 섹션 ---
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("프롬프트 복사", use_container_width=True):
                if user_input and selected_spread_name:
                    # 버튼 클릭 시점에서 데이터를 한 번 더 확인 (TypeError 방지 핵심)
                    current_info = spreads_data.get(selected_spread_name)
                    if current_info:
                        drawn = draw_cards(current_info["num_cards"], TAROT_DECK)
                        st.session_state.last_cards = drawn
                        
                        try:
                            t_source = sub_data if "templates" in sub_data else sub_data.get(selected_category, {})
                            template = t_source["templates"].get(selected_spread_name)
                            
                            final_prompt = template.format(
                                user_prompt=user_input,
                                cards=", ".join(drawn),
                                relationship_type=selected_category
                            )
                            st.session_state.last_prompt = final_prompt
                            st.success("프롬프트가 생성되었습니다!")
                            st.code(final_prompt, language='markdown')
                        except Exception as e:
                            st.error("프롬프트 생성 중 오류가 발생했습니다. JSON 형식을 확인해 주세요.")

        with col2:
            if st.button("AI 리딩 시작", use_container_width=True):
                if user_input and selected_spread_name:
                    current_info = spreads_data.get(selected_spread_name)
                    if current_info:
                        with st.spinner("마스터가 카드를 해석하고 있습니다..."):
                            drawn = draw_cards(current_info["num_cards"], TAROT_DECK)
                            st.session_state.last_cards = drawn
                            
                            ai_res, _ = get_ai_reading(
                                selected_category, user_input, [], 
                                selected_spread_name, drawn, prompts_data
                            )
                            st.session_state.last_ai_response = ai_res
                            st.session_state.show_results = True
                            st.rerun()

        with col3:
            if st.button("초기화", use_container_width=True):
                reset_app()

# --- 4. 결과 출력 화면 ---
else:
    st.subheader("타로 리딩 결과")
    st.markdown(st.session_state.last_ai_response)
    
    with st.expander("복채 대신 확인하는 내가 뽑은 카드"):
        st.write(", ".join(st.session_state.last_cards))

    st.markdown("---")
    follow_up_q = st.text_input("리딩에 대해 더 궁금한 점이 있나요?")
    if st.button("추가 질문하기"):
        if follow_up_q:
            with st.spinner("답변을 생성 중입니다..."):
                new_res = get_follow_up_reading(
                    st.session_state.last_ai_response,
                    follow_up_q, 
                    st.session_state.last_prompt, 
                    st.session_state.last_cards
                )
                st.session_state.last_ai_response = new_res
                st.rerun()

    if st.button("메인으로 돌아가기"):
        reset_app()
