import streamlit as st
import random
import json

# 1. 데이터 로드 및 설정
try:
    with open('prompts.json', 'r', encoding='utf-8') as f:
        PROMPTS = json.load(f)
except Exception as e:
    st.error(f"prompts.json 파일을 읽을 수 없습니다: {e}")
    st.stop()

# 타로 카드 전체 덱
TAROT_DECK = [
    "0. 바보", "1. 마법사", "2. 여사제", "3. 여황제", "4. 황제", "5. 교황", "6. 연인", "7. 전차",
    "8. 힘", "9. 은둔자", "10. 운명의 수레바퀴", "11. 정의", "12. 매달린 사람", "13. 죽음",
    "14. 절제", "15. 악마", "16. 탑", "17. 별", "18. 달", "19. 태양", "20. 심판", "21. 세계",
    "완드 에이스", "완드 2", "완드 3", "완드 4", "완드 5", "완드 6", "완드 7", "완드 8", "완드 9", "완드 10",
    "완드 시종", "완드 기사", "완드 퀸", "완드 킹", "컵 에이스", "컵 2", "컵 3", "컵 4", "컵 5", "컵 6",
    "컵 7", "컵 8", "컵 9", "컵 10", "컵 시종", "컵 기사", "컵 퀸", "컵 킹", "검 에이스", "검 2", "검 3",
    "검 4", "검 5", "검 6", "검 7", "검 8", "검 9", "검 10", "검 시종", "검 기사", "검 퀸", "검 킹",
    "펜타클 에이스", "펜타클 2", "펜타클 3", "펜타클 4", "펜타클 5", "펜타클 6", "펜타클 7", "펜타클 8",
    "펜타클 9", "펜타클 10", "펜타클 시종", "펜타클 기사", "펜타클 퀸", "펜타클 킹"
]

# 메이저 카드만 따로 추출 (앞의 22장)
MAJOR_DECK = TAROT_DECK[:22]

# 스프레드 장수 설정
SPREAD_COUNTS = {
    "원 카드": 1, "투 카드 스프레드": 2, "쓰리 카드 스프레드": 3,
    "켈틱 크로스": 10, "집시의 십자": 5, "아스타로트 스프레드": 12,
    "다중선택 스프레드": 4
}

# 2. UI 구성
st.set_page_config(page_title="asTarot 프롬프트", page_icon="🔮")
st.title("🔮 asTarot 프롬프트 생성기")

main_cat = st.selectbox("대분류", list(PROMPTS.keys()))
sub_cats = [k for k in PROMPTS[main_cat].keys() if k != "templates"]
sub_cat = st.selectbox("중분류", sub_cats) if sub_cats else None

target_templates = PROMPTS[main_cat][sub_cat]["templates"] if sub_cat else PROMPTS[main_cat]["templates"]
selected_spread = st.selectbox("스프레드", list(target_templates.keys()))

user_prompt = st.text_area("고민 내용을 입력하세요", height=150)

# 3. 카드 뽑기 로직
if st.button("운명의 카드 뽑고 프롬프트 만들기"):
    if not user_prompt:
        st.warning("먼저 고민 내용을 입력해주세요.")
    else:
        # [수정] 집시의 십자일 경우 메이저 카드에서만 뽑기
        if selected_spread == "집시의 십자":
            drawn = random.sample(MAJOR_DECK, 5)
            # 위치 순서 반영 (위-아래-좌-우-중앙)
            cards_text = f"1(위): {drawn[0]}, 2(아래): {drawn[1]}, 3(좌): {drawn[2]}, 4(우): {drawn[3]}, 5(중앙): {drawn[4]}"
        else:
            count = SPREAD_COUNTS.get(selected_spread, 1)
            drawn = random.sample(TAROT_DECK, count)
            cards_text = ", ".join(drawn)
        
        template = target_templates[selected_spread]
        
        try:
            final_prompt = template.format(
                user_prompt=user_prompt,
                cards=cards_text,
                relationship_type=sub_cat if sub_cat else "일반"
            )
        except:
            final_prompt = template.replace("{user_prompt}", user_prompt).replace("{cards}", cards_text)
        
        # 4. 결과 출력 및 횡스크롤 방지
        st.divider()
        st.subheader("📋 생성된 프롬프트")
        
        # 가로로 늘어지지 않게 고정된 텍스트 영역
        st.text_area("복사해서 AI에게 전달하세요", value=final_prompt, height=450)
        
        # 복사 버튼 역할을 하는 코드 박스
        st.code(final_prompt, language=None)
        
        if selected_spread == "집시의 십자":
            st.info("💡 집시의 십자는 전통 방식에 따라 '메이저 카드'로만 리딩 프롬프트를 생성했습니다.")
        st.info(f"🃏 뽑힌 카드: {cards_text}")

if st.button("다시 하기"):
    st.rerun()
