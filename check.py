import json
import os
from datetime import datetime

def load_students():
    """從 member.txt 讀取所有學生資料"""
    try:
        with open('member.txt', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            return {}
    except FileNotFoundError:
        print("錯誤: member.txt 檔案未找到")
        return {}
    except json.JSONDecodeError:
        print("錯誤: member.txt 檔案格式不正確，應為有效的 JSON 格式")
        return {}

def load_signins(date=None):
    """讀取特定日期的簽到紀錄，預設為今天"""
    if date is None:
        date = datetime.today().strftime('%Y-%m-%d')
    
    try:
        with open(f'{date}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"警告: {date}.json 檔案未找到，可能該日尚無簽到記錄")
        return {}

def find_unsigned_students(date=None):
    """找出所有尚未簽到的學生"""
    students = load_students()
    signins = load_signins(date)
    
    # 找出未簽到的學生
    unsigned = {}
    for student_id, name in students.items():
        if student_id not in signins:
            unsigned[student_id] = name
    
    return unsigned

def export_to_file(data, filename):
    """將資料輸出到檔案"""
    with open(filename, 'w', encoding='utf-8') as f:
        for student_id, name in data.items():
            f.write(f"{student_id}, {name}\n")

def main():
    print("==== 未簽到學生查詢系統 ====")
    
    # 詢問是否要查詢特定日期
    use_specific_date = input("是否要查詢特定日期？(y/n, 預設為今天): ").lower() == 'y'
    
    date = None
    if use_specific_date:
        date_input = input("請輸入日期 (YYYY-MM-DD 格式): ")
        try:
            # 驗證日期格式
            datetime.strptime(date_input, '%Y-%m-%d')
            date = date_input
        except ValueError:
            print("錯誤: 日期格式不正確，將使用今天的日期")
    
    # 取得未簽到的學生
    unsigned = find_unsigned_students(date)
    
    # 顯示結果
    if not unsigned:
        print("恭喜！所有學生都已簽到。")
    else:
        print(f"\n共有 {len(unsigned)} 名學生尚未簽到:")
        print("-" * 30)
        for idx, (student_id, name) in enumerate(unsigned.items(), 1):
            print(f"{idx}. {student_id} - {name}")
        
        # 詢問是否要導出到檔案
        export = input("\n是否要將未簽到名單導出到檔案? (y/n): ").lower() == 'y'
        if export:
            today = datetime.today().strftime('%Y-%m-%d')
            filename = f"unsigned_{today}.txt"
            export_to_file(unsigned, filename)
            print(f"已將名單導出至 {filename}")

if __name__ == "__main__":
    main()
