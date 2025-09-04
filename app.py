import streamlit as st
from config import TAROT_DECK
from tarot_data import load_spreads_data, load_prompts_data, draw_cards, get_spread_info_from_display_name
from tarot_ai import get_ai_reading, get_follow_up_reading
import json
import pyperclip

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
            placeholder_text = "어떤 일을 시작하거나 끝내야 할 최적의 시기를 고민한다면 그 상황을 구체적으로 알려주세요. 예시) 이직을 하기로 마음먹었는데, 언제 시도하는 것이 좋을까요?"
        elif selected_category == "포기 여부 결정":
            placeholder_text = "어떤 일을 계속할지 포기할지 고민하는 상황에 대해 자세히 이야기해 주세요. 예시) 이 프로젝트를 계속 진행해야 할지, 아니면 포기하는 것이 좋을지 궁금합니다."
        elif selected_category == "접근 방식 결정":
            placeholder_text = "목표에 도달하기 위한 최선의 접근법을 찾고 있다면 여러 방법에 대한 고민을 구체적으로 알려주세요. 예시) 목표는 정해졌는데, 어떤 방식으로 접근해야 성공할 수 있을까요?"
        elif selected_category == "가치 판단 및 윤리적 결정":
            placeholder_text = "옳고 그름, 가치 판단에 어려움이 있는 상황에 대해 상세히 말씀해 주세요. 예시) 갈등 상황에서 어떤 가치에 우선순위를 두는 것이 옳은 결정일까요?"
    elif main_category == "자유로운 질문":
        selected_category = "자유로운 질문"
        user_input_label = "건강관리, 법률문제, 삶의 의미, 내면 탐구, 영성 등 실재적이거나 근원적인 고민에 대해 자유롭게 입력하세요:"
        placeholder_text = "예시) 제 잠재된 재능은 무엇이고, 어떻게 발견할 수 있을까요?"
    elif main_category == "다중 선택":
        selected_category = "다중 선택"
        user_input_label = "선택지(5개 이하)를 입력하기 전에, 먼저 당신이 처한 상황을 구체적으로 입력하세요:"
        placeholder_text = "예시) A와 B 중 어떤 것을 선택해야 할지 고민입니다."
    
    if main_category != "해당 카테고리에 맞는 질문을 골라주세요":
        user_input = st.text_area(user_input_label, height=150, placeholder=placeholder_text)
    
    # 스프레드 선택 로직
    spread_name_map = {}
    
    # 모든 스프레드 목록을 먼저 준비합니다.
    all_spread_display_names = []
    for spread_display_name, spread_info in spreads_data.items():
        all_spread_display_names.append(f"{spread_display_name} ({spread_info['num_cards']}장)")

    # 사용자가 선택한 카테고리에 따라 스프레드 목록을 필터링합니다.
    if main_category and main_category != "전체 스프레드":
        filtered_spreads = [
            name for name in all_spread_display_names
            if main_category in spreads_data.get(name.split(" (")[0], {}).get("categories", [])
        ]
    else:
        filtered_spreads = all_spread_display_names

    for display_name in filtered_spreads:
        spread_name_map[display_name] = display_name.split(" (")[0]

    spread_display_name = st.selectbox("스프레드를 선택하세요:", options=filtered_spreads, help="고민의 깊이에 따라 스프레드를 선택하세요. 질문의 원인과 결과를 파악하고 싶다면 투카드 스프레드를, 깊은 통찰이 필요하다면 켈틱크로스 또는 아스타로드 스프레드를 추천합니다.")
    spread_name = spread_name_map.get(spread_display_name)
    
    # 다중선택 스프레드가 선택되면 선택지 입력 필드를 표시하고 유효성을 검사합니다.
    start_button_disabled = False
    if "다중선택 스프레드" == spread_name:
        st.subheader("선택지 입력")
        st.markdown("점치고 싶은 선택지를 두 개 이상 입력해주세요. 엔터키로 구분됩니다.")
        
        # 텍스트 에어리어에 기본값 설정
        choices_input = st.text_area("선택지 목록 (예: A안, B안)", 
                                     value="선택지 A\n선택지 B", 
                                     height=150)
        
        choices_list = [c.strip() for c in choices_input.split('\n') if c.strip()]
        st.session_state.last_choices = choices_list

        num_choices = len(choices_list)
        if num_choices < 2:
            st.error(f"⚠️ 현재 선택지는 {num_choices}개입니다. 2개 이상 입력해주세요.")
            start_button_disabled = True
        elif num_choices > 5:
            st.error(f"⚠️ 현재 선택지는 {num_choices}개입니다. 5개 이하로 입력해주세요.")
            start_button_disabled = True
        else:
            st.success(f"✔️ 선택지 {num_choices}개가 입력되었습니다.")
            st.session_state.last_choices = choices_list
            start_button_disabled = False
    
    st.session_state.last_spread_name = spread_name
    st.session_state.last_user_input = user_input
    st.session_state.last_category = selected_category
    st.session_state.last_choices = choices_list if 'choices_list' in locals() else []

if st.session_state.show_results == False:
    st.markdown("---")
    st.subheader("리딩을 시작하시려면 버튼을 눌러주세요. (Gemini 1.5)")
    if st.button("프롬프트 확인 및 리딩 시작", disabled=start_button_disabled):
        # 프롬프트만 미리 생성하고 세션에 저장
        with st.spinner("프롬프트를 생성하고 있습니다..."):
            _, raw_prompt = get_ai_reading(
                st.session_state.last_category,
                st.session_state.last_user_input,
                st.session_state.last_choices,
                st.session_state.last_spread_name,
                st.session_state.last_cards,
                prompts_data
            )
            st.session_state.last_ai_prompt = raw_prompt
            st.session_state.prompt_ready = True
    
# '프롬프트 확인' 버튼을 누른 후에만 아래 UI를 보여줍니다.
if 'prompt_ready' in st.session_state and st.session_state.prompt_ready:
    st.markdown("---")
    st.subheader("이 프롬프트로 다른 AI 모델에서도 리딩을 받아보세요.")
    
    # pyperclip 오류를 해결하기 위해 st.code 블록에 내장된 복사 기능만 사용하도록 수정
    st.code(st.session_state.last_ai_prompt, language='markdown')

    st.markdown("---")
    # 리딩을 실제로 진행하는 버튼
    if st.button("타로 리딩 시작"):
        with st.spinner("타로 마스터가 카드를 뽑고 리딩하고 있습니다..."):
            # 이미 생성된 프롬프트와 카드를 사용하여 리딩을 진행
            ai_response, _ = get_ai_reading(
                st.session_state.last_category,
                st.session_state.last_user_input,
                st.session_state.last_choices,
                st.session_state.last_spread_name,
                st.session_state.last_cards,
                prompts_data
            )
            st.session_state.last_ai_response = ai_response
            st.session_state.show_results = True
            st.session_state.prompt_ready = False # 리딩 후에는 상태 초기화
            st.rerun()

# 리딩 결과를 보여주는 코드 (기존 코드와 동일)
if st.session_state.show_results:
    st.write(st.session_state.last_ai_response)
    st.markdown("---")
    
    # 추가 질문 기능
    st.subheader("추가 질문하기")
    follow_up_input = st.text_input("리딩 내용에 대해 더 궁금한 점이 있으신가요?", key="follow_up_input")
    if st.button("추가 질문하기", disabled=not follow_up_input):
        with st.spinner("타로 마스터가 추가 질문에 답하고 있습니다..."):
            follow_up_response = get_follow_up_reading(st.session_state.last_ai_prompt, follow_up_input)
            st.session_state.last_ai_response += f"\n\n**사용자의 추가 질문:** {follow_up_input}\n\n**타로 마스터의 답변:** {follow_up_response}"
            st.experimental_rerun()