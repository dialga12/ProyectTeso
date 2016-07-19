import psycopg2
import datetime
import xml.etree.ElementTree as ET
from CBase import *
import json

class CLogin(CBase):
   pcClave  = None
   pcCodUsu = None
   
   def omLogin(self):
       # Condiciones de excepcion
       if self.mxEmpty(self.pcClave):
#          self.pcError = '<DATA><ERROR>CLAVE DE USUARIO VACIA</ERROR></DATA>'
          self.pcError = '{"ERROR": "CLAVE DE USUARIO VACIA"}'
          return False
       elif self.mxEmpty(self.pcCodUsu):
#          self.pcError = '<DATA><ERROR>CODIGO DE USUARIO VACIO</ERROR></DATA>'
          self.pcError = '{"ERROR": "CODIGO DE USUARIO VACIO"}'
          return False
       # Conectar base de datos           
       self.loSql = CSql()
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       # Verifica usuario
       lcSql = "SELECT * FROM f_Login1('" + self.pcCodUsu.strip() + "', '" + self.pcClave.strip() + "')"
       RS = self.loSql.omExecRS(lcSql)
       if len(RS) == 0:
          self.loSql.omDisconnect()
          self.pcError = '{"ERROR": "ERROR AL LLAMAR A LA FUNCION ALMACENADA PARA VALIDAR AL USUARIO"}'
          return False
       self.loSql.omDisconnect()
       # Verifica cadena de retorno
       try:
          laTmp = json.loads(RS[0][0])
       except:
          print RS[0][0]
          self.pcError = '{"ERROR": "ERROR EN FORMATO XML DE RETORNO DE FUNCION ALMACENADA QUE VALIDA USUARIO"}'
          return False
       if 'ERROR' in laTmp:
          self.pcError = RS[0][0]
          return False
       self.pcData = RS[0][0]
       return True

   def omInit(self):
       # Condiciones de excepcion
       if self.mxEmpty(self.pcClave):
          self.pcError = '<DATA><ERROR>CLAVE DE USUARIO VACIA</ERROR></DATA>'
          return False
       elif self.mxEmpty(self.pcCodUsu):
          self.pcError = '<DATA><ERROR>CODIGO DE USUARIO VACIO</ERROR></DATA>'
          return False
       # Conectar base de datos           
       self.loSql = CSql()
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       # Verifica usuario
       lcSql = "SELECT cNomUsu, cEstado FROM S01TUSU WHERE cCodUsu = '" + self.pcCodUsu.strip() + "' AND cClave = MD5('" + self.pcClave.strip() + "')"
       RS = self.loSql.omExecRS(lcSql)
       if len(RS) == 0:
          self.loSql.omDisconnect()
          self.pcError = '<DATA><ERROR>ERROR AL LLAMAR A LA FUNCION ALMACENADA PARA VALIDAR AL USUARIO</ERROR></DATA>'
          return False
       elif RS[0][1] != 'A':
          self.loSql.omDisconnect()
          self.pcError = '<DATA><ERROR>USUARIO NO ESTA ACTIVO</ERROR></DATA>'
          return False
       lcCodUsu = RS[0][0].strip()
       # Fecha del sistema
       RS = self.loSql.omExecRS("SELECT cConVar FROM S01TVAR WHERE cNomVar = 'GDFECSIS'")
       if RS[0][0] == None:
          self.loSql.omDisconnect()
          self.pcError = '<DATA><ERROR>FECHA DEL SISTEMA [GDFECIS] NO ESTA DEFINIDA. INFORME A TI</ERROR></DATA>'
          return False
       ldFecSis = self.mxValDate(RS[0][0])
       self.loSql.omDisconnect()
       if ldFecSis == None:
          self.pcError = '<DATA><ERROR>FECHA DEL SISTEMA [GDFECIS] TIENE FORMATO INVALIDO. INFORME A TI</ERROR></DATA>'
          return False
       self.pcData = '<DATA><CNOMUSU>' + lcCodUsu + '</CNOMUSU><DFECSIS>' + str(ldFecSis) + '</DFECSIS></DATA>'
       print '***'+self.pcData
       return True

