import json
import re

def extract_json(data_list):
    extracted_data = []
    for item in data_list:
        # 'info' 필드에서 JSON 부분 추출
        json_string = re.search(r'```json\n(.*)\n```', item['info'], re.DOTALL).group(1)
        # JSON 문자열을 딕셔너리로 변환
        json_data = json.loads(json_string)
        extracted_data.append(json_data)
    return extracted_data

# 주어진 리스트
data_list = [
    {'file': '명함사진1.jpg', 'info': '```json\n{\n    "이름": "김나연",\n    "회사": "larana",\n    "직급": "제품 관리자",\n    "전화번호": "+123-456-7890",\n    "주소": "아무 도시 123 애니웨어 스트리트, ST 12345",\n    "이메일": "hello@reallygreatsite.com"\n}\n```'}
]

# 함수 호출
extracted_json = extract_json(data_list)

print(extracted_json)