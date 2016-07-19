import xml.etree.ElementTree as ET
from CPlanillas import *
from CAdelantos import *
from CActivoFijo import *
from CContabilizar import *
from CCntPlanillas import *

# Implementation of the Beta interface
class Beta(CBase):
   lcParStr = None
   lcClase  = None
   lcMetodo = None
   loRoot   = None
   
   def Dispatch(self, p_cParStr):
       if self.mxEmpty(p_cParStr):
          self.pcError = '<DATA><ERROR>NO HA DEFINIDO PARAMETRO</ERROR></DATA>'
          return False
       self.lcParStr = p_cParStr
       self.loRoot = ET.fromstring(self.lcParStr)   # OJOFPM PONER TRY CATCH
       # Carga datos de clase y metodo
       for lo in self.loRoot:
           if lo.tag == 'CLASS':
              self.lcClase = lo.text
           if lo.tag == 'METHOD':
              self.lcMetodo = lo.text
       # Verifica si ha definido atributo Clase y Metodo
       if self.lcClase == None:
          self.pcError = '<DATA><ERROR>NO HA DEFINIDO ETIQUETA [CLASS]</ERROR></DATA>'
          return False
       elif self.lcMetodo == None:
          self.pcError = '<DATA><ERROR>NO HA DEFINIDO ETIQUETA [METHOD]</ERROR></DATA>'
          return False
       llOk = self.CallMethodClass()
       return llOk

   def CallMethodClass(self):
       print self.lcClase
       print self.lcMetodo
       ##############################################################
       # Clase Test
       ##############################################################
       if (self.lcClase == 'CTEST') and (self.lcMetodo == 'TEST'):
          lcNombre = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CNOMBRE':
                 lcNombre = lo.text
          # Valida variables
          if lcNombre == None:
             self.pcData = '<DATA><ERROR>NOMBRE NO DEFINIDO</ERROR></DATA>' 
             return False
          self.pcData = '<DATA><CDATO>SALUDOS ' + lcNombre + '</CDATO></DATA>'
          return True
       ##############################################################
       # Clase Login
       ##############################################################
       if (self.lcClase == 'CLOGIN') and (self.lcMetodo == 'LOGIN'):
          lcCodUsu = lcClave = lcNombre = lcTipo = lnCambio = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
              elif lo.tag == 'CCLAVE':
                 lcClave = lo.text
          # Llama a clase que realiza apertura de planilla
          lo = CLogin()
          lo.pcCodUsu = lcCodUsu
          lo.pcClave  = lcClave
          llOk = lo.omLogin()
          if llOk:
             self.pcData = lo.pcData
          else:
             self.pcError = lo.pcError
          return True
       ##############################################################
       # Clase CPlanillas metodo de apertura de planilla
       ##############################################################
       elif (self.lcClase == 'CPLANILLAS') and (self.lcMetodo == 'APERTURA'):
          lcCodUsu = lcDescri = lcCodPla = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
              elif lo.tag == 'CDESCRI':
                 lcDescri = lo.text
              elif lo.tag == 'CCODPLA':
                 lcCodPla = lo.text
          # Llama a clase que realiza apertura de planilla
          lo = CPlanillas()
          lo.pcDescri = lcDescri
          lo.pcCodPla = lcCodPla
          lo.pcCodUsu = lcCodUsu
          llOk = lo.omApertura()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Clase CAdelantos metodo de genera adelanto de quincena
       ##############################################################
       elif (self.lcClase == 'CADELANTOS') and (self.lcMetodo == 'GENERARQUINCENA'):
          lcCodUsu = lcTermId = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
              elif lo.tag == 'CTERMID':
                 lcTermId = lo.text
          # Valida variables
          if lcCodUsu == None:
             self.pcError = '<DATA><ERROR>CODIGO DE USUARIO NO DEFINIDO</ERROR></DATA>' 
             return False
          elif lcTermId == None:
             self.pcError = '<DATA><ERROR>IDENTIFICADOR DE TERMINAL DEFINIDO</ERROR></DATA>' 
             return False
          # Llama a clase que realiza apertura de planilla
          lo = CAdelantos()
          lo.pcTermId = lcTermId
          lo.pcCodUsu = lcCodUsu
          llOk = lo.omGenerarQuincena()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##################################################################
       # Clase CAdelantos metodo de realiza el pago o abono de quincena
       ##################################################################
       elif (self.lcClase == 'CADELANTOS') and (self.lcMetodo == 'PAGOQUINCENA'):
          lcCodUsu = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
          # Llama a clase que realiza apertura de planilla
          lo = CAdelantos()
          lo.pcCodUsu = lcCodUsu
          llOk = lo.omPagoQuincena()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Clase CAdelantos metodo que genera adelanto de comision  OJOFPM
       ##############################################################
       elif (self.lcClase == 'CADELANTOS') and (self.lcMetodo == 'GENERARCOMISION'):
          lcCodUsu = lcTermId = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
              elif lo.tag == 'CTERMID':
                 lcTermId = lo.text
          # Llama a clase que realiza apertura de planilla
          lo = CAdelantos()
          lo.pcTermId = lcTermId
          lo.pcCodUsu = lcCodUsu
          llOk = lo.omGenerarComision()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Clase CAdelantos metodo que paga el adelanto de comision
       ##############################################################
       elif (self.lcClase == 'CADELANTOS') and (self.lcMetodo == 'PAGOCOMISION'):
          print '***'
          lcCodUsu = lcTermId = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
              elif lo.tag == 'CTERMID':
                 lcTermId = lo.text
          # Llama a clase que realiza apertura de planilla
          lo = CAdelantos()
          lo.pcCodUsu = lcCodUsu
          lo.pcTermId = lcTermId
          llOk = lo.omPagoComision()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Clase CPlanillas metodo que valida iniciar procesar planilla
       ##############################################################
       elif (self.lcClase == 'CPLANILLAS') and (self.lcMetodo == 'INITPROCESAR'):
          lcCodUsu = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
          # Valida variables
          if lcCodUsu == None:
             self.pcError = '<DATA><ERROR>CODIGO DE USUARIO NO DEFINIDO</ERROR></DATA>' 
             return False
          # Llama a clase que valida el proceso de planilla
          lo = CPlanillas()
          lo.pcCodUsu = lcCodUsu
          llOk = lo.omInitProcesarPlanilla()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Clase CPlanillas metodo de que procesa planilla
       # '<DATA><CLASS>CPLANILLAS</CLASS><METHOD>PROCESARPLANILLA</METHOD><CCODUSU>9999</CCODUSU></DATA>'
       ##############################################################
       elif (self.lcClase == 'CPLANILLAS') and (self.lcMetodo == 'PROCESARPLANILLA'):
          lcCodUsu = lcCodPla = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
          # Valida variables
          # Llama a clase que realiza apertura de planilla
          lo = CPlanillas()
          lo.pcCodUsu = lcCodUsu
          llOk = lo.omProcesarPlanilla()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       #########################################################################
       # Clase CContabilizar metodo inicia contabilizacion de planilla mensual   OJOFPM REVISAR SI SE ELIMINA
       #########################################################################
       elif (self.lcClase == 'CCONTABILIZAR') and (self.lcMetodo == 'INITCONTABILIZARPLANILLA'):
          lcCodUsu = lcCodPla = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
          # Valida variables
          if lcCodUsu == None:
             self.pcError = '<DATA><ERROR>CODIGO DE USUARIO NO DEFINIDO</ERROR></DATA>' 
             return False
          # Llama a clase que realiza apertura de planilla
          lo = CContabilizar()
          lo.pcCodUsu = lcCodUsu
          llOk = lo.omInitContabilizarPlanilla()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Clase CContabilizar metodo que contabiliza planilla mensual
       ##############################################################
       elif (self.lcClase == 'CCONTABILIZAR') and (self.lcMetodo == 'CONTABILIZARPLANILLA'):
          lcCodUsu = lcCodPla = lcTermid = ldFecSis = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
              if lo.tag == 'CCODPLA':
                 lcCodPla = lo.text
              if lo.tag == 'CTERMID':
                 lcTermId = lo.text
              if lo.tag == 'DFECSIS':
                 ldFecSis = lo.text
          # Llama a clase que realiza apertura de planilla
          lo = CContabilizar()
          lo.pcCodUsu = lcCodUsu
          lo.pcCodPla = lcCodPla
          lo.pcTermId = lcTermId
          lo.pdFecSis = ldFecSis
          llOk = lo.omContabilizarPlanilla()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Clase CLogin metodo que inicia sesion
       ##############################################################
       elif (self.lcClase == 'CLOGIN') and (self.lcMetodo == 'INIT'):
          lcCodUsu = lcClave = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
              if lo.tag == 'CCLAVE':
                 lcClave = lo.text
          # Valida variables
          if lcCodUsu == None:
             self.pcError = '<DATA><ERROR>CODIGO DE USUARIO NO DEFINIDO</ERROR></DATA>' 
             return False
          elif lcClave == None:
             self.pcError = '<DATA><ERROR>CLAVE DE USUARIO NO DEFINIDO</ERROR></DATA>' 
             return False
          # Llama a clase que realiza apertura de planilla
          lo = CLogin()
          lo.pcCodUsu = lcCodUsu
          lo.pcClave  = lcClave
          llOk = lo.omInit()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Clase CActivoFijo metodo que deprecia
       ##############################################################
       elif (self.lcClase == 'CACTIVOFIJO') and (self.lcMetodo == 'DEPRECIACION'):
          lcCodUsu = lcTermId = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
              if lo.tag == 'CTERMID':
                 lcTermId = lo.text
          # Llama a clase que realiza apertura de planilla
          lo = CActivoFijo()
          lo.pcCodUsu = lcCodUsu
          lo.pcTermId = lcTermId
          llOk = lo.omDepreciacion()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Clase CCntPlanillas metodo que contabiliza
       ##############################################################
       elif (self.lcClase == 'CCNTPLANILLAS') and (self.lcMetodo == 'CONTABILIZAR'):
          lcCodUsu = lcTermId = None
          # Carga variables
          for lo in self.loRoot:
              if lo.tag == 'CCODUSU':
                 lcCodUsu = lo.text
              if lo.tag == 'CTERMID':
                 lcTermId = lo.text
          # Llama a clase que realiza apertura de planilla
          lo = CCntPlanillas()
          lo.pcCodUsu = lcCodUsu
          lo.pcTermId = lcTermId
          llOk = lo.omContabilizar()
          self.pcData = lo.pcData
          self.pcError = lo.pcError
          return llOk
       ##############################################################
       # Error
       ##############################################################
       else:
          print 'OJO'
          self.pcError = '<DATA><ERROR>CLASE [' + self.lcClase + '] y METODO [' + self.lcMetodo + '] NO ESTAN DEFINIDAS</ERROR></DATA>'
          return False

