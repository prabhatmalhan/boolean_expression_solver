from flask import Flask
from flask import render_template,request
from utils.Solve import solve

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    return render_template("index.html")

@app.route('/solve',methods=['POST'])
def solve_eq():
    try:
        equation = request.get_json()['equation']
    except:
        return "error"
    return solve(equation=equation)

app.run()