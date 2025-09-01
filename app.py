import streamlit as st
from config import TAROT_DECK
from tarot_data import load_spreads_data, load_prompts_data, draw_cards
from tarot_ai import get_ai_reading
import json

# 데이터 로딩
spreads_data = load_spreads_data()
prompts_data = load_prompts_data()

st.title("타로 리더")

# 사이드바 메뉴 구성
with st.sidebar:
    st.header("타로 리딩 설정")

    # 1. 메인 카테고리 선택
    main_categories = list(prompts_data.keys())
    main_category = st.selectbox("고민 카테고리:", options=main_categories)

    # 2. 하위 카테고리 선택 (관계, 성공, 결정, 탐색 카테고리)
    selected_category = main_category
    
    # '관계' 카테고리의 하위 카테고리
    if main_category == "관계":
        sub_categories = list(prompts_data.get(main_category, {}).keys())
        selected_category = st.selectbox("관계의 종류:", options=sub_categories)
    
    # '결정' 카테고리의 하위 카테고리
    elif main_category == "결정":
        sub_categories = list(prompts_data.get(main_category, {}).keys())
        selected_category = st.selectbox("결정의 종류:", options=sub_categories)
        
    # '성공' 카테고리의 하위 카테고리
    elif main_category == "성공":
        sub_categories = list(prompts_data.get(main_category, {}).keys())
        selected_category = st.selectbox("성공의 종류:", options=sub_categories)
    
    # '다중 선택' 카테고리일 때만 다중 선택 스프레드 선택
    elif main_category == "다중 선택":
        selected_category = main_category
    
    # 스프레드 목록 필터링
    spread_name_map = {}
    filtered_spreads = []

    if selected_category == "다중 선택":
        filtered_spreads = ["다중선택 스프레드 (1 + n*2장)"]
        spread_name_map["다중선택 스프레드 (1 + n*2장)"] = "다중선택 스프레드"
    else:
        for spread_display_name, spread_info in spreads_data.items():
            if selected_category in spread_info.get("categories", []):
                display_name = f"{spread_display_name} ({spread_info['num_cards']}장)"
                filtered_spreads.append(display_name)
                spread_name_map[display_name] = spread_display_name
                
    spread_name_with_count = st.selectbox(
        "사용할 스프레드를 선택하세요:",
        options=filtered_spreads,
        help="스프레드를 선택하면 리딩에 사용되는 카드 수와 위치별 의미가 달라집니다."
    )
    
    spread_name = spread_name_map.get(spread_name_with_count)

# 메인 화면 UI
# 카테고리에 따라 다른 플레이스홀더 문구 표시
placeholder_text = {
    "연애": "지금 당신의 마음을 가장 흔드는 연애 관계와 그에 대한 구체적인 이야기를 편하게 들려주세요.",
    "대인관계": "당신을 둘러싼 대인관계 속에서 어떤 어려움이나 궁금증이 있나요? 편하게 이야기해 주세요.",
    "기타": "어떤 고민이든 좋습니다. 마음속에 품고 있는 이야기를 편하게 들려주세요.",
    "금전운": "당신의 금전운에 대한 고민을 구체적으로 이야기해 주세요. 예를 들어, '새로운 투자를 시작할까요?' 또는 '재정적 어려움을 겪고 있는데 어떻게 해야 할까요?' 와 같이요.",
    "직업운": "당신의 직업에 대한 고민을 구체적으로 이야기해 주세요. 예를 들어, '이직을 하는 것이 좋을까요?' 또는 '새로운 사업을 시작해도 될까요?' 와 같이요.",
    "학업운": "당신의 학업에 대한 고민을 구체적으로 이야기해 주세요. 예를 들어, '어떤 전공을 선택해야 할까요?' 또는 '시험을 잘 볼 수 있을까요?' 와 같이요.",
    "우선순위 결정": "여러 선택지 중 어떤 것을 먼저 해야 할지 고민인가요? 각 선택지에 대한 구체적인 이야기를 들려주세요.",
    "타이밍 결정": "어떤 일을 시작하거나 끝내야 할지 시기를 정하는 데 어려움이 있나요? 그 상황에 대해 구체적으로 이야기해 주세요.",
    "포기 여부 결정": "어떤 일을 계속해야 할지, 아니면 포기해야 할지 고민인가요? 그 상황에 대해 구체적으로 이야기해 주세요.",
    "접근 방식 결정": "어떤 목표를 위해 어떤 접근 방식을 취해야 할지 고민인가요? 그 상황에 대해 구체적으로 이야기해 주세요.",
    "가치 판단 및 윤리적 결정": "어떤 상황에서 옳고 그름을 판단하는 데 어려움이 있나요? 그 상황에 대해 구체적으로 이야기해 주세요.",
    "탐색": "자신에 대해 더 깊이 알고 싶나요? 혹은 어떤 방향으로 나아가야 할지 막막한가요? 편하게 이야기해 주세요."
}.get(selected_category, "고민을 입력해주세요. 구체적으로 작성할수록 정확한 리딩을 받을 수 있습니다.")


user_input = st.text_area(
    "고민을 입력해주세요. 구체적으로 작성할수록 정확한 리딩을 받을 수 있습니다.",
    value="",
    height=150,
    placeholder=placeholder_text
)

# '다중 선택' 카테고리일 때만 선택지 입력란 표시
choices = []
if spread_name == "다중선택 스프레드":
    st.subheader("선택지 입력")
    # choices 변수를 리스트로 초기화하고 사용자가 입력하는 만큼 동적으로 추가
    num_choices = st.number_input("선택지 개수", min_value=2, max_value=5, value=2, step=1)
    
    for i in range(num_choices):
        choice = st.text_input(f"선택지 {i + 1}", key=f"choice_{i}", placeholder=f"예시) 선택지 {i + 1}에 대한 구체적인 내용")
        if choice:
            choices.append(choice)

if st.button("리딩 시작"):
    if not user_input:
        st.warning("고민을 입력해주세요.")
    elif spread_name == "다중선택 스프레드" and not all(choices):
        st.warning("선택지를 모두 입력해주세요.")
    else:
        with st.spinner('카드를 뽑고 있어요...'):
            num_cards = spreads_data.get(spread_name, {}).get("num_cards", 0)
            if spread_name == "다중선택 스프레드":
                num_cards = 1 + len(choices) * 2
            
            cards = draw_cards(TAROT_DECK, num_cards, spread_name)

        st.subheader("뽑은 카드")
        st.write(f"**스프레드:** {spread_name_with_count}")
        st.write(f"**총 {len(cards)}장**")
        st.write(f"**카드 목록:** {', '.join(cards)}")
        
        st.markdown("---")
        st.subheader("타로 리딩 결과")
        ai_response = get_ai_reading(selected_category, user_input, choices, spread_name, cards, prompts_data)
        st.write(ai_response)
