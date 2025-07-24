import os
import subprocess
import time
from api_key import api_key
from module import *

save_name = "test"
save_path = os.path.join(os.getcwd(), f'{save_name}.py')

### Chat with LLM ###
print("\nStarting chat with AI. To end the chat, type 'exit' or 'quit'. If you want to run the python code, type 'run'")

### Chat history ###
chat_history = [
    {"role": "system",
     "content": "You are an AI for generating Python code. You must mark the beginning and end of the Python code with $$$"}
]

while True:
    user_input = input("\nYou: ").strip()

    # end code
    if user_input.lower() in ["exit", "quit"]:
        print("--- Chat ended. ---")
        break

    # run code
    elif user_input.lower() == "run":
        if os.path.exists(save_path):
            print(f"Executing Python code from '{save_path}'...\n")
            result = subprocess.run(["python", save_path], capture_output=True, text=True)

            # 실행 결과 출력
            if result.stdout:
                print(f"--- 출력값 ---\n{result.stdout}")
            if result.stderr:
                print(f"--- 출력 오류 ---\n{result.stderr}")
        else:
            print(f"Error: No Python code saved at '{save_path}'.")


    # chat with AI
    else:
        # AI 응답 출력
        response_text = chat_ai(user_input, chat_history, api_key)

        # AI 응답을 콘솔에 출력
        print(f"\nAI: {response_text}\n", flush=True)

        time.sleep(1)  # 1초 동안 대기

        # AI 응답에서 Python 코드 추출
        extracted_code = extract_python_code(response_text)

        if extracted_code is not None:
            # 추출된 코드를 파일로 저장
            save_code_to_file(extracted_code, save_path)
            print(f'Python code has been saved to {save_path}')

        else:
            print("No valid Python code extracted from AI response.")
