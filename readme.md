# Snow Removal SNS [Prototype]
2024/03/19 ~ 03/20 Kitami-Hackson@KITAMIBASE

## API Server
### [GET] /snow
除雪データをリスト型ですべて返します。

### [PUT] /snow/new_post
除雪データを登録します。
#### Request
```json
{
  "place": "43.804933, 143.893789",
  "user_id": 123456
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
```