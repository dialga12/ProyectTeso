from Beta import *
from flask import Flask, request, make_response
import barrister

# Implementation of the Alpha interface in the IDL
class Calculator(object):
   def add(self, p_cParStr):
       print p_cParStr
       print p_cParStr['clase']
       return ""

contract = barrister.contract_from_file("interface_structura.json")
server   = barrister.Server(contract)
server.add_handler("Calculator", Calculator())

app = Flask(__name__)

@app.route("/william", methods=["POST"])
def get_Alpha():
    resp_data = server.call_json(request.data)
    resp = make_response(resp_data)
    resp.headers['Content-Type'] = 'application/json'
    return resp

app.run(host="127.0.0.1", port=7667)
#app.run(host="10.0.159.15", port=7667)


