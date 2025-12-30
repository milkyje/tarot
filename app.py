import streamlit as st
import random
import json

# 1. 페이지 설정
st.set_page_config(page_title="asTarot 프롬프트 메이커", page_icon="🔮")

# 2. 데이터 로드
try:
    with open('prompts.json', 'r', encoding='utf-8') as f:
        PROMPTS = json.load(f)
except Exception as e:
    st.error(f"prompts.json 파일을 읽을 수 없습니다: {e}")
    st.stop()

# 스프레드별 카드 장수 설정
SPREAD_COUNTS = {
    "원 카드": 1, 
    "투 카드 스프레드": 2, 
    "쓰리 카드 스프레드": 3,
    "켈틱 크로스": 10, 
    "집시의 십자": 5, 
    "아스타로트 스프레드": 12,
    "다중선택 스프레드": 4
}

# 타로 카드 78장 리스트
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

# 3. UI 구성
st.title("🔮 asTarot 프롬프트 생성기")
st.write("카드를 뽑고 완성된 프롬프트를 복사해서 AI에게 전달하세요.")

# 카테고리 선택
main_cat = st.selectbox("대분류", list(PROMPTS.keys()))
sub_cats = [k for k in PROMPTS[main_cat].keys() if k != "templates"]
sub_cat = st.selectbox("중분류", sub_cats) if sub_cats else None

# 템플릿 선택
try:
    target_templates = PROMPTS[main_cat][sub_cat]["templates"] if sub_cat else PROMPTS[main_cat]["templates"]
    selected_spread = st.selectbox("스프레드", list(target_templates.keys()))
except:
    st.error("템플릿을 불러올 수 없습니다.")
    st.stop()

user_prompt = st.text_area("고민 내용을 입력하세요", height=150)

# 4. 프롬프트 생성 로직
if st.button("운명의 카드 뽑고 프롬프트 만들기"):
    if not user_prompt:
        st.warning("먼저 고민 내용을 입력해주세요.")
    else:
        # 카드 무작위 뽑기
        count = SPREAD_COUNTS.get(selected_spread, 1)
        drawn = random.sample(TAROT_DECK, count)
        cards_text = ", ".join(drawn)
        
        # 템플릿 가져오기
        template = target_templates[selected_spread]
        
        # 프롬프트 완성
        try:
            final_prompt = template.format(
                user_prompt=user_prompt,
                cards=cards_text,
                relationship_type=sub_cat if sub_cat else "일반"
            )
        except:
            final_prompt = template.replace("{user_prompt}", user_prompt).replace("{cards}", cards_text)
        
        # 결과 화면 표시
        st.divider()
        st.subheader("📋 생성된 프롬프트")
        st.write("아래 내용을 복사해서 챗GPT 등에 붙여넣으세요.")
        
        # 텍스트 영역에 담아 보여주기 (복사하기 편하도록)
        st.text_area("완성된 지시문", value=final_prompt, height=400)
        
        st.info(f"🃏 뽑힌 카드: {cards_text}")
        
        # 버튼 하나로 복사하는 기능 (브라우저 환경에 따라 작동)
        st.code(final_prompt, language=None)
        st.caption("위 박스 오른쪽 상단의 복사 버튼을 누르세요.")

if st.button("다시 하기"):
    st.rerun()
