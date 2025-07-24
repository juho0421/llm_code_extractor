from openai import OpenAI
import re  # 정규 표현식 (코드 부분만 추출하기 위함)


# AI와 chat을 통해 답변을 반환받는 함수
def chat_ai(user_input, chat_history, api_key, model="gpt-3.5-turbo"):
    # 대화 히스토리 저장을 위한 리스트

    client = OpenAI(api_key=api_key)

    # 사용자 입력을 히스토리에 추가
    chat_history.append({"role": "user", "content": user_input})

    # AI 응답 생성
    chat_completion = client.chat.completions.create(
        messages=chat_history,  # 이전 대화 포함
        model=model,
    )

    # AI의 마지막 응답 추출
    response_text = chat_completion.choices[0].message.content.strip()

    # 대화 기록에 AI 응답 추가
    chat_history.append({"role": "assistant", "content": response_text})

    # 마지막 응답 반환
    return response_text


# AI가 생성한 답변 중, python code 부분만을 추출하는 함수
def extract_python_code(response_text):
    # 1차 필터링: $$$ 내부의 내용만 추출
    match = re.search(r"\$\$\$(.*?)\$\$\$", response_text, re.DOTALL)

    if match:
        extracted_code = match.group(1).strip()  # 앞뒤 공백 제거
    else:
        extracted_code = ""  # $$$가 없을 경우 코드가 없음


    # 2차 필터링: ```python ... ``` 내부 코드만 추출
    match_2 = re.search(r"```python(.*?)```", extracted_code, re.DOTALL)

    # 3차 필터링: ``` ... ``` 내부 코드만 추출
    match_3 = re.search(r"```(.*?)```", extracted_code, re.DOTALL)

    if match_2:
        final_code = match_2.group(1).strip()  # 코드 블록 내부 코드만 반환
    elif match_3:
        final_code = match_3.group(1).strip()  # 코드 블록 내부 코드만 반환
    else:
        final_code = extracted_code  # 코드 블록이 없으면 기존 코드 사용

    if final_code == "":
        print("No code")

    return final_code  # 최종 코드 반환


# 추출된 Python Code 부분을 지정된 경로에 저장하는 함수
def save_code_to_file(code, save_path):
    if not code.strip():  # 코드가 비어 있거나 공백만 있을 경우 처리
        # print("No python code")
        return

    # 코드가 있으면 파일로 저장
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(code)