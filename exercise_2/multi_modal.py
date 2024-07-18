from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from dotenv import load_dotenv
import os
import base64

def multimodal():
    # 환경 변수 로드
    load_dotenv()

    # Azure OpenAI 클라이언트 설정
    client = AzureChatOpenAI(
        openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version = "2023-05-15",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def extract_info_from_image(image_path, prompt):
        base64_image = encode_image(image_path)

        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                },
                {
                    "type": "text",
                    "text": "이 명함 이미지에서 정보를 추출해주세요."
                }
            ])
        ]

        response = client.invoke(messages)
        return response.content

    # 프롬프트 템플릿
    prompt = """
    당신은 명함 이미지에서 정보를 추출하는 최고의 전문가입니다. 주어진 명함 이미지를 세심하게 분석하여 다음 정보를 정확하게 추출해주세요. 추출한 정보는 반드시 아래 지정된 JSON 형식으로 반환해야 합니다.

    추출할 정보:
    - 이름: 한글로 번역 (원문이 영어인 경우에만)
    - 회사: 원어 그대로 유지
    - 직급: 한글로 번역 (원문이 영어인 경우에만)
    - 전화번호: 숫자와 기호만 포함
    - 주소: 한글로 번역 (원문이 영어인 경우에만)
    - 이메일: 소문자로 통일

    주의사항:
    1. 회사명은 절대 번역하지 마세요.
    2. 전화번호는 국가 코드를 포함하여 완전한 형태로 추출하세요.
    3. 이메일 주소는 정확히 추출하고, 대소문자를 구분하지 않습니다.
    4. 정보가 없는 경우 해당 필드를 공백 한 칸 문자열(" ")로 설정하세요.
    5. JSON 형식을 엄격히 준수하세요.

    반환 형식:
    {
    "이름": "번역된 이름",
    "회사": "원어 그대로의 회사명",
    "직급": "번역된 직급",
    "전화번호": "추출된 전화번호",
    "주소": "원어 그대로의 주소",
    "이메일": "추출된 이메일"
    }

    추가 지시사항:
    - 명함에 여러 전화번호가 있는 경우, 가장 대표적인 번호만 추출하세요.
    - 주소는 가능한 한 상세하게 추출하되, 불필요한 정보는 제외하세요.
    - 직급이 여러 개 나열된 경우 가장 높은 직급을 선택하세요.
    """
    # 명함 이미지 처리
    image_folder = '/root/LLM_Bootcamp/exercise_2/data/img'        # 해당 루트로 변경
    
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    save_image_files = set()
    results = []  # 모든 결과를 저장할 리스트
    
    # 이미 처리된 이미지 목록 읽기
    try:
        with open('/root/LLM_Bootcamp/exercise_2/data/name.txt', 'r') as f:
            processed_images = set(line.strip() for line in f)
    except FileNotFoundError:
        pass
    
    # 아직 처리되지 않은 이미지만 선택
    image_files = list(set(image_files) - processed_images)
    print("처리할 이미지:", image_files)
    
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        result = extract_info_from_image(image_path, prompt)
        print(f"\n명함 정보 ({image_file}):")
        print(result)
        print("\n")
        results.append({"file": image_file, "info": result})
        print(results)
        with open('/root/LLM_Bootcamp/exercise_2/data/name.txt', 'a') as f:
            f.write(image_file + '\n')
    return results  # 모든 결과를 반환

# 메인 함수 실행
if __name__ == "__main__":
    results = multimodal()
    print("모든 처리 완료")