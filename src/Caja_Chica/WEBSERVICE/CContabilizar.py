# -*- coding: utf-8 -*-
from decimal import *
from CBase import *
from CPlanillas import *

##############################################################
# Clase que contabiliza transacciones de planillas
##############################################################
class CContabilizar(CPlanillaBase):
    pcCodUsu = None
    lcCodCnt = None
    laCtaCnt = []

    #-----------------------------------------------------------------
    # Valida si se puede contabilizar planilla
    #-----------------------------------------------------------------
    def mxInitContabilizarPlanilla(self):   ## OJOFPM ES PUBLICO O PROTEGIDO
        if self.pcCodUsu == None:
           self.pcError = '<DATA><ERROR>CODIGO DE USUARIO NO DEFINIDO</ERROR></DATA>'
           return False
        elif self.pcCodPla == None:
           self.pcError = '<DATA><ERROR>CODIGO DE PLANILLA NO DEFINIDO</ERROR></DATA>'
           return False
        elif self.pdFecSis == None:
           self.pcError = '<DATA><ERROR>FECHA DEL SISTEMA NO DEFINIDA</ERROR></DATA>'
           return False
        llOk = self.mxValInit()
        if self.lcFases != '1111110000':   # OJOFPM
           self.pcError = '<DATA><ERROR>ESTADO DE FASES DE PLANILLA NO PERMITE CONTABILIZAR LA PLANILLA</ERROR></DATA>'
           return False
        self.pcData = '<DATA><CCODPLA>' + self.pcCodPla + '</CCODPLA><CDESCRI>' + self.pcDescri.strip() + '</CDESCRI></DATA>'
        self.lcCodCnt = self.pcCodPla + 'PLA';
        return True

    #-----------------------------------------------------------------
    # Contabiliza planilla
    #-----------------------------------------------------------------
    def omContabilizarPlanilla(self):
        lcCodPla = self.pcCodPla
        llOk = self.mxInitContabilizarPlanilla()
        if not llOk:
           return False
        if lcCodPla != self.pcCodPla:
           self.pcError = '<DATA><ERROR>ERROR EN CODIGO DE PLANILLA. REINTENTE Y VERIFIQUE PLANILLA A CONTABILIZAR</ERROR></DATA>'
           return False
        # Conectar base de datos           
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Nro de doc.
        llOk = self.mxNumeroDocumentoOficina()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Inicializa proceso (valida cuentas contables y borra anteriores registros)
        llOk = self.mxInitContabilizar()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Contabiliza conceptos de cada empleado
        llOk = self.mxContabilizarPlanilla()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Graba contabilizacion en tablas contables
        llOk = self.mxGrabarContabilizacion()
        if llOk:
           self.loSql.omCommit()
        self.loSql.omDisconnect()
        self.pcData = '<DATA><MENSAJE>CONTABILIZACION DE PLANILLA CONFORME</MENSAJE></DATA>'
        return True

    # Busca cuenta contable de AFP
    def mxSeekAfp(self, p_cConcep, p_cCodAfp):
        llFind = False
        i = 0
        for x in self.laCtaCnt:
            if x[0] == p_cConcep and x[1] == p_cCodAfp:
               llFind = True
               break
            i += 1
        if not llFind:
           return None
        return i

    # Inicia proceso de contabilizacion de planilla
    def mxInitContabilizar(self):
        # Codigo contable
        llOk = self.loSql.omExec("DELETE FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>NO SE PUDO BORRAR ANTERIOR CONTABILIZACION. AVISE A TI</ERROR></DATA>'
           return False
        # Cuentas contables
        lcCtaPte = '1511010101'   # OJOFPM FALTA PARAMETRIZAR
        j = 0
        # Cuentas contables de AFP
        self.laCtaCnt = []
        RS = self.loSql.omExecRS("SELECT cConcep, cCodAfp, cCtaCnt FROM ADM.f_CuentasContables()")
        for XTMP in RS:
            lcCtaCnt = XTMP[2].strip() + '%'
            RS = self.loSql.omExecRS("SELECT COUNT(cCtaCnt) FROM CNT.D01MCTA WHERE cCtaCnt LIKE '" + lcCtaCnt + "'")
            if RS[0][0] == 0:
               self.pcError = '<DATA><ERROR>CUENTA CONTABLE [' + XTMP[2].strip() + '] NO EXISTE (AFP)</ERROR></DATA>'
               return False
            elif RS[0][0] > 1:
               self.pcError = '<DATA><ERROR>CUENTA CONTABLE [' + XTMP[2].strip() + '] NO ES DE ULTIMO NIVEL (AFP)</ERROR></DATA>'
               return False
            self.laCtaCnt.append([])
            self.laCtaCnt[j].append(XTMP[0])
            self.laCtaCnt[j].append(XTMP[1])
            self.laCtaCnt[j].append(XTMP[2])
            j += 1
        if j == 0:
           self.pcError = '<DATA><ERROR>NO HAY CUENTAS CONTABLES DE CONCEPTOS DEFINIDOS</ERROR></DATA>'
           return False
        return True

    # Contabilizacion de planilla
    def mxContabilizarPlanilla(self):
        j = 0
        RS = self.loSql.omExecRS("SELECT cCodigo, cCodOfi, cCodAfp, cCtaBco FROM ADM.V_E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XEMP in RS:
            lcCodigo = XEMP[0]
            lcCodOfi = XEMP[1]
            RS = self.loSql.omExecRS("SELECT nMonto, cConcep FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND (SUBSTRING(cConcep, 1, 1) IN ('A', 'B', 'C', 'D') OR cConcep IN ('E03', 'N10'))")
            for XTRX in RS:            
                j += 1
                # Numero de documento
                i = self.FindArray(self.laNroDoc, XEMP[1])
                lcNroDoc = self.laNroDoc[i][1]
                lnHaber = lnDebe = 0
                if XTRX[1][:1] == 'A':
                   lnHaber = XTRX[0]
                else:
                   lnDebe = XTRX[0]
                # Cuenta contable
                if XTRX[1] == 'C02' or XTRX[1] == 'C03' or XTRX[1] == 'C04':
                   # Cuentas de AFP
                   i = self.mxSeekAfp(XTRX[1], XEMP[2])
                else:
                   # Otras cuentas
                   i = self.FindArray(self.laCtaCnt, XTRX[1])
                lcCtaCnt = self.laCtaCnt[i][2]
                lcGlosa = 'PAGO SUELDO [' + XEMP[3] + ']'
                lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cGlosa, cCtaCnt, nDebeC, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "',  '" + self.pdFecSis + "', '" + lcGlosa + "', '" + lcCtaCnt + "', " + str(lnDebe) + ", " + str(lnHaber) + ", '" + self.pcCodUsu + "')"
                llOk = self.loSql.omExec(lcSql)
                if not llOk:
                   self.pcError = '<DATA><ERROR>NO SE PUDO GRABAR CONTABILIZACION [E10DCNT]. AVISE A TI</ERROR></DATA>'
                   return False
        if j == 0:
           self.loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>ERROR: NO HAY DATOS PARA CONTABILIZAR</ERROR></DATA>'
           return False
        return True

    # Graba contabilizacion en tablas contables
    def mxGrabarContabilizacion(self):
        # Descripcion de planilla
        lcSql = "SELECT cDescri FROM ADM.E01MPLA WHERE cCodPla = '" + self.lcCodCnt[:5] + "'"
        RS = self.loSql.omExecRS(lcSql)
        if RS[0][0] == None:
           self.loSql.omDisconnect()
           self.pcError = "CODIGO DE PLANILLA [" + lcCodPla[:5] + "] NO EXISTE"
           return False
        lcGlosa = 'PLANILLA - ' + RS[0][0].strip()
        lcNroDoc = '*'
        RS = self.loSql.omExecRS("SELECT cNroDoc, cCtaCnt, nDebeC, nHaberC, cGlosa FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "' ORDER BY cNroDoc, cCtaCnt")
        for XCNT in RS:
            if XCNT[0] != lcNroDoc:
               # Graba cabecera de comprobante contable
               lcNroDoc = XCNT[0]
               lcNroCom = lcNroDoc[:2] + 'PL01'
               lcNroCom = self.mxNroComprobante(lcNroCom)
               # cTipDoc = 'RI' [803]
               lcSql = "INSERT INTO CNT.D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" + lcNroCom + "', '" + lcNroDoc + "', '', '" + lcNroDoc[:2] + "', 'S', 'ADELANTO DE COMISION', 'RI', '', '', '', '', '" + self.pdFecSis + "', '', '', '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>NO SE PUDO GRABAR CABECERA CONTABLE. AVISE A TI</ERROR></DATA>'
                  return False
            # Graba detalle de comprobante contable
            lcGlosa = XCNT[4]
            lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + XCNT[1] + "', '" + lcGlosa + "', 0, 0, " + str(XCNT[2]) + ", " + str(XCNT[3]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
            llOk = self.loSql.omExec(lcSql) 
            if not llOk:
               self.pcError = '<DATA><ERROR>NO SE PUDO GRABAR DETALLE CONTABLE. AVISE A TI</ERROR></DATA>'
               return False
        # Actualiza fase de planillas
        llOk = self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1111111000' WHERE cCodPla = '" + self.pcCodPla + "'") 
        if not llOk:
           self.pcError = '<DATA><ERROR>NO SE PUDO ACTUALIZAR EL ESTADO DE FASE DE LA PLANILLA [E01MPLA]. AVISE A TI</ERROR></DATA>'
           return False
        self.pcMensaje = '<DATA><MENSAJE>CONTABILIZACION DE PLANILLA CONFORME</MENSAJE></DATA>'
        return True

    #-----------------------------------------------------------------
    # Valida si se puede contabilizar pago planilla
    #-----------------------------------------------------------------
    def omInitContabilizarPlanilla(self):
        llOk = self.mxValInit()
        if self.lcFases != '1111111000':   # OJOFPM
           self.pcError = '<DATA><ERROR>ESTADO DE FASES DE PLANILLA NO PERMITE CONTABILIZAR EL PAGO DE PLANILLA</ERROR></DATA>'
           return False
        self.pcData = '<DATA><CCODPLA>' + self.pcCodPla + '</CCODPLA><CDESCRI>' + self.pcDescri.strip() + '</CDESCRI></DATA>'
        return True
    
    #-----------------------------------------------------------------
    # Contabiliza pago de planilla  OJOFPM ES IGUAL A CONTABILIZACION DE CADELANTOS
    #-----------------------------------------------------------------
    def omContabilizarPagoPlanilla(self):
        lcCodPla = self.pcCodPla
        llOk = self.omInitPagoContabilizarPlanilla()
        if not llOk:
           return False
        if lcCodPla != self.pcCodPla:
           self.pcError = '<DATA><ERROR>ERROR EN CODIGO DE PLANILLA. REINTENTE Y VERIFIQUE PLANILLA A CONTABILIZAR</ERROR></DATA>'
           return False
        # Lee todos los pagos de adelanto de quincena
        RS = self.loSql.omExecRS("SELECT cCodOfi, nMonto, cCtaBco FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'N10' ORDER BY cCodOfi")
        for XPAG in RS:
            # Abona en cuenta de ahorros
            print XPAG[2], XPAG[1]
        # Numeros de comprobantes contables por oficinas
        i = 0
        laNroCom = []
        lcSql = "SELECT DISTINCT cCodOfi FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'N10' UNION SELECT DISTINCT SUBSTRING(cCtaBco, 1, 2) AS cCodOfi FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'N10'"
        RS = self.loSql.omExecRS(lcSql)
        for XOFI in RS:
            # Nro documento referencia
            self.lcCodCnt = self.pcCodPla + 'C'
            RS = self.loSql.omExecRS("SELECT cNroDoc FROM cCodCnt = '" + self.lcCodCnt + "' AND SUBSTRING(cNroDoc, 1, 2) = '" + XOFI[0] + "' LIMIT 1")
            if len(RS) == 0:
               RS = self.loSql.omExecRS("SELECT cNroDoc FROM cCodCnt = '" + self.lcCodCnt + "' LIMIT 1")
            lcNroDoc = RS[0][0]
            # Nro Comprobante
            lcNroCom = XOFI[0] + 'AV01'  # OJOFPM FALTA EL MES
            lcNroCom = self.mxNroComprobante(lcNroCom)
            laNroCom.append([])
            laNroCom[i].append(XOFI[0])
            laNroCom[i].append(lcNroCom)
            i += 1
            # cTipDoc = 'RI' [803]
            lcSql = "INSERT INTO CNT.D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" + lcNroCom + "', '" + lcNroDoc + "', '', '" + lcNroCom[:2] + "', 'S', 'ABONO DE QUINCENA', 'RI', '', '', '', '', '" + self.ldFecSis + "', '', '', '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql) 
        if i == 0: ## OJOFPM AQUI ME QUEDE
           self.pcError = '<DATA><ERROR>NO HAY OFICINAS DEFINIDAS</ERROR></DATA>';
           return False
        # Contabiliza pagos de adelanto de quincena
        lcSql = "SELECT cCodOfi, cOfiCod, SUM(nMonto) FROM (SELECT cCodOfi, nMonto, SUBSTRING(cCtaBco, 1, 2) AS cOfiCod FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D01') A GROUP BY cCodOfi, cOfiCod ORDER BY cCodOfi"
        RS = self.loSql.omExecRS(lcSql)
        for XCNT in RS:
            if XCNT[0] == XCNT[1]:
               i = self.FindArray(laNroCom, XCNT[0])
               lcNroCom = laNroCom[i][1]
               #i = int(XCNT[0]) - 1  
               #lcNroCom = laNroCom[i][1]
               # Cuenta puente
               lcCtaCnt = self.self.laCtaCnt[1][0]
               lcDescri = self.self.laCtaCnt[1][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, " + str(XCNT[2]) + ", 0," + str(self.lnTipCam) + "'" + self.pcCodUsu + "')" 
               self.loSql.omExec(lcSql)
               # Cuenta ahorros
               lcCtaCnt = self.self.laCtaCnt[3][0]
               lcDescri = self.self.laCtaCnt[3][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, 0, " + str(XCNT[2]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
            else:
               # Agencia origen
               i = self.FindArray(laNroCom, XCNT[0])
               lcNroCom = laNroCom[i][1]
               #i = int(XCNT[0]) - 1  
               #lcNroCom = laNroCom[i][1]
               # Cuenta puente
               lcCtaCnt = self.self.laCtaCnt[1][0]
               lcDescri = self.self.laCtaCnt[1][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, " + str(XCNT[2]) + ", 0, " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
               # Cuenta interagencias
               lcCtaCnt = self.self.laCtaCnt[2][0]
               lcDescri = self.self.laCtaCnt[2][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, 0, " + str(XCNT[2]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
               # Agencia destino
               i = self.FindArray(laNroCom, XCNT[1])
               lcNroCom = laNroCom[i][1]
               #i = int(XCNT[1]) - 1
               #lcNroCom = laNroCom[i][1]
               # Cuenta interagencias
               lcCtaCnt = self.self.laCtaCnt[2][0]
               lcDescri = self.self.laCtaCnt[2][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, " + str(XCNT[2]) + ", 0, "  + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
               # Cuenta ahorros
               lcCtaCnt = self.self.laCtaCnt[3][0]
               lcDescri = self.self.laCtaCnt[3][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, 0, " + str(XCNT[2]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
        self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1100000000' WHERE cCodPla = '" + self.pcCodPla + "'")
        self.pcData = '<DATA><MENSAJE>PAGO QUINCENA CONFORME</MENSAJE></DATA>';
        return True

