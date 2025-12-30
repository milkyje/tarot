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
    # 1. 메인 카테고리 선택
    main_categories = list(prompts_data.keys())
    main_category = st.selectbox("큰 고민의 종류를 선택하세요:", options=main_categories)

    # 2. 세부 카테고리 설정
    sub_data = prompts_data.get(main_category, {})
    if "templates" in sub_data:
        selected_category = main_category
    else:
        sub_categories = list(sub_data.keys())
        selected_category = st.selectbox("구체적인 고민 분야를 선택하세요:", options=sub_categories)

    # 3. 질문 입력 (이 부분이 에러의 핵심!)
    # 여기서 입력을 해도 아래 draw_cards가 실행되지 않도록 logic을 버튼 안으로 숨깁니다.
    user_input = st.text_area("고민 내용을 입력하세요:", value="", help="입력 후 아래 스프레드를 선택하고 버튼을 눌러주세요.")
    
    # 4. 스프레드 필터링 및 선택
    valid_spreads = [
        name for name, info in spreads_data.items()
        if main_category in info["categories"] or f"{main_category}_{selected_category}" in info["categories"]
    ]

    if not valid_spreads:
        st.warning("선택한 카테고리에 맞는 스프레드가 없습니다.")
    else:
        selected_spread_name = st.selectbox("원하는 스프레드를 선택하세요:", options=valid_spreads)
        
        # UI용 정보 (에러를 일으키지 않는 단순 텍스트 표시)
        info = spreads_data.get(selected_spread_name)
        if info:
            st.caption(f"🔮 {selected_spread_name}: {info['num_cards']}장의 카드를 사용합니다.")

        # --- 버튼 섹션 (에러 유발 로직을 모두 버튼 안으로 격리) ---
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("프롬프트 복사", use_container_width=True):
                if not user_input:
                    st.error("질문을 먼저 입력해 주세요!")
                else:
                    target_info = spreads_data.get(selected_spread_name)
                    # 버튼을 눌렀을 때만 카드를 뽑음
                    drawn = draw_cards(target_info["num_cards"], TAROT_DECK)
                    st.session_state.last_cards = drawn
                    
                    try:
                        t_source = sub_data if "templates" in sub_data else sub_data[selected_category]
                        template = t_source["templates"][selected_spread_name]
                        formatted = template.format(user_prompt=user_input, cards=", ".join(drawn), relationship_type=selected_category)
                        st.success("프롬프트 생성 완료!")
                        st.code(formatted, language='markdown')
                    except:
                        st.error("프롬프트 생성 중 오류가 발생했습니다.")

        with col2:
            if st.button("AI 리딩 시작", use_container_width=True):
                if not user_input:
                    st.error("질문을 먼저 입력해 주세요!")
                else:
                    with st.spinner("운명의 카드를 해석하는 중..."):
                        target_info = spreads_data.get(selected_spread_name)
                        drawn = draw_cards(target_info["num_cards"], TAROT_DECK)
                        st.session_state.last_cards = drawn
                        
                        ai_res, _ = get_ai_reading(selected_category, user_input, [], selected_spread_name, drawn, prompts_data)
                        st.session_state.last_ai_response = ai_res
                        st.session_state.show_results = True
                        st.rerun()

        with col3:
            if st.button("초기화", use_container_width=True):
                reset_app()

else:
    # 결과 화면 (이전과 동일)
    st.subheader("타로 리딩 결과")
    st.markdown(st.session_state.last_ai_response)
    with st.expander("뽑힌 카드 확인"):
        st.write(", ".join(st.session_state.last_cards))
    if st.button("처음으로"):
        reset_app()
