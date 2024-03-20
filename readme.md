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