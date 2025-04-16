# 資訊研究社社團簽到系統

## 系統功能
- 驗證機制：管理員啟動系統時輸入當日驗證碼。使用者必須輸入正確驗證碼才能簽到。
- 簽到功能：使用者輸入學號與姓名進行簽到。需輸入驗證碼（由管理員啟動時設定）。避免重複簽到。
- 登入狀況查看：顯示已簽到的學生。

## 使用技術
- 前端技術：HTML、CSS、JavaScript (Fetch API)
- 後端技術：Python (Flask 框架)
- 資料處理：JSON 作為資料存儲格式
- 伺服器公開：使用ngrok來讓同學能使用

## 安裝與啟動
### 安裝依賴
```bash
pip install flask
```

### 啟動系統
```bash
python app.py
```
啟動後，系統會提示您輸入今日的簽到驗證碼。輸入後，伺服器會開始運行。

### 使用ngrok公開伺服器（選用）
1. 下載並安裝ngrok (https://ngrok.com/)
2. 執行命令：
```bash
ngrok http 5000
```
3. 使用ngrok提供的網址讓外部用戶訪問

## 檔案結構
- app.py：主要的Flask應用程式
- member.txt：社團成員資料（JSON格式）
- YYYY-MM-DD.json：每日簽到記錄
- templates/：HTML模板
  - verification.html：驗證頁面
  - index.html：簽到頁面
  - admin.html：管理頁面
- check.py：檢查未簽到成員

## 作者
資訊研究社
