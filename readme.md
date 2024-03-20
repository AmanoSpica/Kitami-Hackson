# YUKIDOKE [Prototype]
2024/03/19 ~ 03/20 Kitami-Hackson@KITAMIBASE

## API Server
### [GET] /snow
(下記Queryがない場合、または0を指定した場合は) 除雪データをリスト型ですべて返します。

#### Request
直近のデータのみ取得したい場合はリクエストURLにQueryを追加してください。<br>
下記例では直近2時間のデータを取得し返します。<br>
例）`/snow/?data_before_hour=2`

### [POST] /snow/new_post
除雪データを登録します。
#### Request
```json
{
  "latitude": "43.804933",
  "longitude":"143.893789",
  "user_id": 123
}
```
### [GET] /chat
chatデータをリスト型ですべて返します。


### [POST] /chat/new_message
新規メッセージを登録します。
#### Request
```json
{
  "user_name": "string",
  "message": "string"
}
```


## 実行環境
Python 3.12.2
(その他ライブラリは`requirements.txt`に記載しています)

### 環境構築
```cmd
# venv環境の構築
$ python3 -m venv env

# 仮想環境を起動 (Powershell)
$ env\Scripts\Activate.ps1
# 仮想環境を起動 (Mac)
$ source env/bin/activate

# ライブラリをインストール
(venv) > pip install -r requirements.txt

# 実行
(venv) > python3 main.py

# 開発用 reloadオプションで起動
(venv) > uvicorn main:app --reload
```