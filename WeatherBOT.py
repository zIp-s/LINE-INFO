import json
import urllib.request
import requests

#ACCCESS TOKEN NAME
line_notify_token = 'YOUR TOKEN'
line_notify_api = 'https://notify-api.line.me/api/notify'
print('アクセストークンセット完了')
 
def main():
    jsonp = urllib.request.urlopen("http://www.drk7.jp/weather/json/23.js").read().decode("utf-8")
    data = json.loads(jsonp.replace("drk7jpweather.callback(", "")[:-2])
    i = 0
    msg = ""
    f = open('LINE.txt', 'w')

    for j in data["pref"]["area"]["西部"]["info"]:
        date = j["date"]
        rainfall_chance = j["rainfallchance"]
        temperature = j["temperature"]
        weather = j["weather"]
        max_temp, min_temp = temperature["range"]

        #天気情報をテキストで保存
        print("{0}".format(date), file=f)
        print("気温：{0}℃ - {1}℃".format(min_temp["content"], max_temp["content"]), file=f)
        print("天気：{0}".format(weather), file=f)
        print("降水確率", file=f)
        for k in rainfall_chance["period"]:
            print("  {0}:{1}%".format(k["hour"], k["content"]), file=f)
        print(file=f)
        i = i + 1

        #取得日数
        if i == 3:
            print('取得完了')
            f.close()

            #ファイルを開きなおす
            f = open('LINE.txt', 'r')
            msg1 = f.read()
            f.close()

            #最終行の改行を削除
            msg1 = msg1.rstrip()
            
            #結果を出力
            print(msg1)

            #LINE SEND
            message = msg1
            payload = {'message': message}
            headers = {'Authorization': 'Bearer ' + line_notify_token}  # Token
            line_notify = requests.post(line_notify_api, data=payload, headers=headers)
            print('LINE送信完了')
            #LINE SEND END
            
            return
 
if __name__ == '__main__':
    main()
