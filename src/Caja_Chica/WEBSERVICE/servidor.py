from CLogin import *
from flask import Flask, request, make_response
import barrister
import json

class Alpha(object):

   def Alpha(self, p_cParStr):
       print 'Alpha...'
       laTmp = json.loads(p_cParStr)
       if laTmp['ID'] == 'InicioSesion':
          lo = CLogin()
          lo.pcCodUsu = laTmp['CCODUSU']
          lo.pcClave  = laTmp['CCLAVE']
          llOk = lo.omLogin()
          if not llOk:
             print lo.pcError
             return lo.pcError
          else:
             print lo.pcData
             return lo.pcData
       else:
          return '{"ERROR": "ERROR INDETERMINADO"}'
       

       '''
       print '111'
       print p_cParStr
       if p_cParStr == None or p_cParStr.strip() == '':
          return '<DATA><ERROR>ERROR EN PARAMETRO</ERROR></DATA>'
       lo = Beta()
       llOk = lo.Dispatch(p_cParStr)
       if llOk:
          return lo.pcData
       else:
          return lo.pcError
       '''
   def mxAlpha(self):
       return 'a'

contract = barrister.contract_from_file("Alpha.json")
server   = barrister.Server(contract)
server.add_handler("Alpha", Alpha())

app = Flask(__name__)

@app.route("/Alpha", methods=["POST"])
def get_Alpha():
    print '000'
    resp_data = server.call_json(request.data)
    print '111'
    resp = make_response(resp_data)
    print '222'
    resp.headers['Content-Type'] = 'application/json'
    print resp
    return resp

app.run(host="10.0.159.7", port=7667)
#app.run(host="10.0.159.15", port=7667)



