from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 設定隨機的密鑰用於Session

# 當日驗證碼，由管理員設定
VERIFICATION_CODE = ""

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
        return {}

def save_signin(student_id, name, date=None):
    """保存簽到記錄"""
    if date is None:
        date = datetime.today().strftime('%Y-%m-%d')
    
    # 讀取現有簽到資料
    signins = load_signins(date)
    
    # 添加新簽到記錄
    signins[student_id] = name
    
    # 保存更新後的簽到資料
    with open(f'{date}.json', 'w', encoding='utf-8') as f:
        json.dump(signins, f, ensure_ascii=False)

@app.route('/')
def index():
    """簽到頁面"""
    # 檢查是否已經驗證
    if 'verified' not in session or not session['verified']:
        return redirect(url_for('verification'))
    return render_template('index.html')

@app.route('/verification')
def verification():
    """驗證碼頁面"""
    return render_template('verification.html')

@app.route('/verify', methods=['POST'])
def verify():
    """處理驗證碼"""
    code = request.form.get('code')
    if code == VERIFICATION_CODE:
        session['verified'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '驗證碼錯誤'})

@app.route('/signin', methods=['POST'])
def signin():
    """處理簽到請求"""
    # 檢查是否已經驗證
    if 'verified' not in session or not session['verified']:
        return jsonify({'redirect': True})
    
    student_id = request.form.get('student_id')
    name = request.form.get('name')
    
    # 驗證學號和姓名
    students = load_students()
    if student_id not in students:
        return jsonify({'message': '學號不存在，請確認後重試'})
    
    if students[student_id] != name:
        return jsonify({'message': '學號與姓名不符，請確認後重試'})
    
    # 檢查是否已簽到
    signins = load_signins()
    if student_id in signins:
        return jsonify({'message': '您已經簽到過了'})
    
    # 保存簽到記錄
    save_signin(student_id, name)
    
    return jsonify({'message': f'簽到成功！{name}同學'})

@app.route('/admin')
def admin():
    """管理頁面"""
    # 檢查是否已經驗證
    if 'verified' not in session or not session['verified']:
        return redirect(url_for('verification'))
    
    # 獲取今日簽到記錄
    signins = load_signins()
    
    return render_template('admin.html', signins=signins)

@app.route('/logout')
def logout():
    """登出"""
    session.clear()
    return redirect(url_for('verification'))

def set_verification_code(code):
    """設定當日驗證碼"""
    global VERIFICATION_CODE
    VERIFICATION_CODE = code

if __name__ == '__main__':
    print("==== 資訊研究社社團簽到系統 ====")
    
    # 提示管理員輸入驗證碼
    code = input("請輸入今日簽到驗證碼: ")
    
    # 檢查驗證碼是否為空
    while not code.strip():
        print("錯誤: 驗證碼不能為空!")
        code = input("請輸入今日簽到驗證碼: ")
    
    # 設定驗證碼
    set_verification_code(code)
    
    print(f"驗證碼已設定為: {VERIFICATION_CODE}")
    print("系統已啟動，請訪問 http://127.0.0.1:5000/ 使用")
    
    # 啟動Flask應用
    app.run(debug=True)
