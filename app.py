from flask import Flask
from flask import render_template,request
from utils.Solve import solve
import os

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    return render_template("index.html")

@app.route('/solve',methods=['POST'])
def solve_eq():
    try:
        equation = request.get_json()['equation']
        return solve(equation=equation)
    except:
        return "error"

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))