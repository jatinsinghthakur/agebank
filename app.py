from flask import Flask,jsonify,request
from flask_cors import CORS
from Bank import Bank

app=Flask(__name__)
CORS(app)

@app.route("/create_acc",methods=["POST"])
def create_account():
    data:dict=request.get_json()
    person=Bank()
    res=person.open_account(data.get("name"),data.get("amount"),data.get("dob"),data.get("passcode"))
    data={
        "account_number":res
    }
    return jsonify(data)

@app.route("/debit",methods=["POST"])
def debit():
    data=request.get_json()

    person=Bank()
    res=person.debit(data.get("acc_num"),data.get("passcode"),data.get("amount"))

    return jsonify(res)


@app.route("/verify_credit",methods=["POST"])
def verify_credit():
    person=Bank()
    res=person.verify_credit(request.get_json().get("acc_num"))
    return jsonify({"name":res})

@app.route("/confirm_credit",methods=["POST"])
def confirm_credit():
    data:dict=request.get_json()
    acc_num=data.get("acc_num")
    amount=data.get("amount")
    person=Bank()
    res = person.confirm_credit(acc_num,amount)
    return jsonify(res)


@app.route("/info",methods=["POST"])
def info():
    data:dict=request.get_json()
    acc_num=data.get("acc_num")
    passcode=data.get("passcode")
    person=Bank()
    result=person.info(acc_num,passcode)
    return jsonify(result)
    
if __name__=="__main__":
    app.run(port=3001)



