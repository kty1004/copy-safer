from flask import Flask

app= Flask('testing server') # 서버 이름을 정하는 것이다.

@app.route('/') # /는 홈페이지를 말함.
def say_hello(): # 이 함수는 사용자가 홈페이지에 들어갔을 때 어떤 것을 보여줄 지 정하는 것임.
    return 'hello! hello!!' # @ 바로 밑에다가 함수를 써야 함.
    
app.run("127.0.0.1") # 서버의 주소