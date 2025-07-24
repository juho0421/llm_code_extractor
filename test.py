import subprocess

# pip freeze 실행 결과 가져오기
result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)

# requirements.txt 파일에 저장
with open('requirements.txt', 'w') as f:
    f.write(result.stdout)