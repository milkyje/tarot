import streamlit as st
from config import TAROT_DECK
from tarot_data import load_spreads_data, load_prompts_data, draw_cards
from tarot_ai import get_ai_reading, get_follow_up_reading

# --- 1. 세션 상태 초기화 ---
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'last_cards' not in st.session_state:
    st.session_state.last_cards = []
if 'last_ai_response' not in st.session_state:
    st.session_state.last_ai_response = ""

def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# 데이터 로딩
spreads_data = load_spreads_data()
prompts_data = load_prompts_data()

st.title("asTarot - 아스타로트 마스터")

if not st.session_state.show_results:
    # --- 2. 입력 폼 구간 ---
    with st.form("tarot_input_form"):
        st.subheader("고민 카테고리 및 정보 입력")
        
        main_categories = list(prompts_data.keys())
        main_category = st.selectbox("고민의 큰 카테고리:", options=main_categories)

        sub_data = prompts_data.get(main_category, {})
        if "templates" in sub_data:
            selected_category = main_category
        else:
            sub_categories = list(sub_data.keys())
            selected_category = st.selectbox("세부 카테고리:", options=sub_categories)

        user_input = st.text_area("고민 내용을 입력하세요:", placeholder="상황을 구체적으로 적어주세요.")
        
        # 해당 카테고리에 맞는 스프레드 필터링
        valid_spreads = [
            name for name, info in spreads_data.items()
            if main_category in info["categories"] or f"{main_category}_{selected_category}" in info["categories"]
        ]
        
        selected_spread_name = st.selectbox("타로 스프레드 선택:", options=valid_spreads)
        
        # 제출 버튼
        submit_button = st.form_submit_button("운명의 카드 뽑기", use_container_width=True)

    # --- 3. 실행 구간 (에러 방지를 위해 변수 재정의) ---
    if submit_button:
        if not user_input:
            st.warning("고민 내용을 먼저 입력해 주세요!")
        else:
            # 버튼 클릭 시점에 선택된 스프레드 정보를 다시 가져옵니다 (TypeError 해결 핵심)
            target_info = spreads_data.get(selected_spread_name)
            
            if target_info:
                with st.spinner("아스타로트 마스터가 카드를 해석하고 있습니다..."):
                    try:
                        # 카드 뽑기
                        num_to_draw = target_info.get("num_cards", 1)
                        drawn = draw_cards(num_to_draw, TAROT_DECK)
                        st.session_state.last_cards = drawn
                        
                        # AI 리딩 실행
                        ai_res, _ = get_ai_reading(
                            selected_category, 
                            user_input, 
                            [], 
                            selected_spread_name, 
                            drawn, 
                            prompts_data
                        )
                        st.session_state.last_ai_response = ai_res
                        st.session_state.show_results = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"리딩 중 오류가 발생했습니다: {e}")
            else:
                st.error("선택된 스프레드 정보를 찾을 수 없습니다.")

    # 초기화 버튼
    if st.button("전체 초기화"):
        reset_app()

else:
    # --- 4. 결과 출력 구간 ---
    st.subheader("타로 리딩 결과")
    st.markdown(st.session_state.last_ai_response)
    
    with st.expander("뽑힌 카드 확인"):
        st.write(", ".join(st.session_state.last_cards))
        
    if st.button("다시 상담하기"):
        reset_app()
