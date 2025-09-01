import google.generativeai as genai
import json

# AI 리딩을 생성하는 함수
def get_ai_reading(category, user_input, choices, spread_name, cards, prompts_data):
    try:
        prompt_template = prompts_data.get(category, {}).get("templates", {}).get(spread_name)
        if not prompt_template:
            return "죄송합니다. 해당 스프레드에 대한 프롬프트 템플릿이 없습니다."
        
        # '다중선택 스프레드'에 대한 특별 처리
        if spread_name == "다중선택 스프레드":
            prompt = prompt_template.format(
                category=category,
                user_prompt=user_input,
                choices=choices,
                cards=cards
            )
        else:
            prompt = prompt_template.format(
                category=category,
                user_prompt=user_input,
                cards=cards
            )

        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"리딩을 생성하는 중 오류가 발생했습니다: {e}"

