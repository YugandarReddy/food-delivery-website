from flask import Flask,render_template

app=Flask(__name__)

@app.route("/")
def login_page():
    return render_template('Login_Page.html')


if __name__== '__main__':
    app.run(host='0.0.0.0',debug=True)