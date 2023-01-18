import sqlite3
import requests
import json

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('op.html')


@app.route('/login', methods=['post'])
def login():
    global result
    data = str(request.form.get('name'))
    a = 'yuedu'
    con = sqlite3.connect('fanyi.db')
    cur = con.cursor()

    if __name__ == "__main__":

        # while True:
        # a = input('请输入词源(yuedu,wanxing)：')

        # data = input('请输入单词：')
        #
        # print(data)

        url = "http://fanyi.youdao.com/translate"

        header = {"i": data, "doctype": "json"}
        response = requests.get(url, header)
        html = response.text

        page = json.loads(html, strict=False)
        result = page["translateResult"][0][0]["tgt"]

        # print("结果：" + result)

        cur.execute("select * from %s " % a)
        PL = cur.fetchall()
        lis = []
        for i in PL:
            lis.append(i[0])

        if data not in lis:
            cur.execute("insert into %s (words, times) values (?,?) " % a, (data, 1))
        else:
            cur.execute("select * from %s where words='%s' " % (a, data))
            L = cur.fetchall()

            n = L[0][1]
            cur.execute("update %s set times =%d where words='%s' " % (a, n + 1, data))
        con.commit()

        # print("*翻译结束*")

    return str(data) + '的意思是：' + str(result)


if __name__ == '__main__':
    app.run()
