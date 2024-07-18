import sqlite3
import json
import os

# 데이터베이스 생성 및 시작
def init_db():
    db_path = '/root/LLM_Bootcamp/exercise_2/data/business_cards.db'
    db_dir = os.path.dirname(db_path)

    # 데이터베이스 디렉터리가 존재하지 않으면 생성
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS business_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company TEXT,
        position TEXT,
        phone TEXT,
        address TEXT,
        email TEXT,
        card_image BLOB
    )
    ''')

    # 변경사항 저장
    conn.commit()

    return conn

# 데이터 삽입 함수
def insert_business_cards_from_json(conn, json_file, image_path):
    insert_business_card(
        conn,
        json_file['이름'],
        json_file['회사'],
        json_file['직급'],
        json_file['전화번호'],
        json_file['주소'],
        json_file['이메일'],
        image_path
    )

def insert_business_card(conn, name, company, position, phone, address, email, card_image_path):
    with open(card_image_path, 'rb') as file:
        card_image = file.read()

    cursor = conn.cursor()        
    cursor.execute('''
        INSERT INTO business_cards (name, company, position, phone, address, email, card_image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, company, position, phone, address, email, card_image_path))
    
    conn.commit()

# 모든 데이터 조회 함수
def fetch_all_business_cards(conn):
    cursor = conn.cursor()    

    cursor.execute('SELECT * FROM business_cards')
    return cursor.fetchall()

# 특정 데이터 가져오는 함수
def fetch_order_business_cards(conn, index):
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM business_cards WHERE id= ?', (index, ))
    return cursor.fetchall()

conn1 = init_db()

# 예시 데이터 삽입 - stringfy 하는 걸로 생각
sample_json = {
  "이름": "이수진",
  "회사": "Borcelle",
  "직급": "디자이너",
  "전화번호": "+123-456-7890",
  "주소": "123 Anywhere St., Any City",
  "이메일": "hello@reallygreatsite.com"
}

image_path = "<image_path>"

insert_business_cards_from_json(conn1, sample_json, image_path)
u = fetch_all_business_cards(conn1)
print(u)

print(fetch_order_business_cards(conn1, 2))