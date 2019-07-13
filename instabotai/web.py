import os
from flask import Flask, render_template, request

def main():
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def index():
        return render_template("index.html")
        print(request.method)
        if request.method == 'GET':
            if request.form.get('username') == 'username':
                # pass
                print("download")
            elif  request.form.get('password') == 'password':
                # pass # do something else
                print("Decrypted")
            else:
                # pass # unknown
                return render_template("index.html")
        elif request.method == 'GET':
            print("No Post Back Call")


    if __name__ == '__main__':
        app.run()

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8000, debug=True)
main()
