import psycopg2
import datetime

class CBase:
    def __init__(self):
        self.pcError   = None
        self.pcMensaje = None
        self.loSql     = None
        self.paMeses   = None
        self.pcCodUsu  = None
        self.pcData    = None
        self.ldFecSis  = None
    
    def FindArray(self, p_aArray, p_xSearch, p_nCol = 0):
        llFind = False
        i = 0
        for x in p_aArray:
            if x[p_nCol] == p_xSearch:
               llFind = True
               break
            i += 1
        if not llFind:
           return None
        return i

    def mxValDate(self, p_cFecha):
        try:
           ldFecha = datetime.datetime.strptime(p_cFecha, "%Y-%m-%d").date()
        except:
           ldFecha = None
        return ldFecha
        
    def mxNomDia(self, p_cNroDia):
        if p_cNroDia == '1':
           lcNomDia = 'LUNES'
        elif p_cNroDia == '2':
           lcNomDia = 'MARTES'
        elif p_cNroDia == '3':
           lcNomDia = 'MIERCOLES'
        elif p_cNroDia == '4':
           lcNomDia = 'JUEVES'
        elif p_cNroDia == '5':
           lcNomDia = 'VIERNES'
        elif p_cNroDia == '6':
           lcNomDia = 'SABADO'
        elif p_cNroDia == '7':
           lcNomDia = 'DOMINGO'
        return lcNomDia

    def mxMeses(self):
        self.paMeses = []
        self.paMeses.append(['01', 'ENERO'])
        self.paMeses.append(['02', 'FEBRERO'])
        self.paMeses.append(['03', 'MARZO'])                
        self.paMeses.append(['04', 'ABRIL'])                
        self.paMeses.append(['05', 'MAYO'])                
        self.paMeses.append(['06', 'JUNIO'])                
        self.paMeses.append(['07', 'JULIO'])                
        self.paMeses.append(['08', 'AGOSTO'])                
        self.paMeses.append(['09', 'SETIEMBRE'])                
        self.paMeses.append(['10', 'OCTUBRE'])                
        self.paMeses.append(['11', 'NOVIEMBRE'])                
        self.paMeses.append(['12', 'DICIEMBRE'])                

    def mxToday(self):
        ldFecSis = datetime.date.today()
        return ldFecSis
        
    def mxEmpty(self, p_xValor):
        if p_xValor == None:
           return True
        p_xValor = p_xValor.strip()
        if len(p_xValor) == 0:
           return True
        
    def mxSpace(self, p_cValor, p_nLen):
        lcValor = p_cValor.strip() + ' '*p_nLen
        lcValor = lcValor[:p_nLen]
        return lcValor

class CSql(CBase):
    def __init__(self):
        self.h = None

    def omConnect(self, p_cDB = None):
        llOk = True
        lcConnect = "host=10.0.159.16 dbname=LDoc user=postgres password=34fpm12 port=5432"
        try:
           self.h = psycopg2.connect(lcConnect) 
        except psycopg2.DatabaseError:
           llOk = False
           self.pcError = '<DATA><ERROR>ERROR AL CONECTAR CON LA BASE DE DATOS</ERROR></DATA>'
        return llOk

    def omExecRS(self, p_cSql):
        #print p_cSql
        lcCursor = self.h.cursor()
        lcCursor.execute(p_cSql)
        RS = lcCursor.fetchall()
        '''
        try:
           i = RS[0]
        except:
           RS = None
        '''
        return RS

    def omExec(self, p_cSql):
#        print p_cSql
        llOk = True
        lcCursor = self.h.cursor()
        try:
           lcCursor.execute(p_cSql)
        except Exception as E:
           print type(E)     # the exception instance
           print E.args      # arguments stored in .args
           print E           # __str__ allows args to printed directly:
           print '***'
           llOk = False
        return llOk

    def omDisconnect(self):
        self.h.close()

    def omCommit(self):
        self.h.commit()


class CLogin(CBase):
   pcClave = None
   
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
          self.pcError = '<DATA><ERROR>CODIGO DE USUARIO NO ENCONTRADO O CLAVE ERRADA</ERROR></DATA>'
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


