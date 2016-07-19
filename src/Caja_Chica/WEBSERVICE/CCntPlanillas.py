# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from CBase import *
from CBasePlanillas import *
from decimal import *

##############################################################
# Clase que contabiliza planillas
##############################################################
class CCntPlanillas(CPlanillaBase):
    paAnhos  = None
    paNumero = None
    pcNumero = None
    laAfpCnt = None

    #-----------------------------------------------------------------
    # Contabilizar planilla
    #-----------------------------------------------------------------
    def omContabilizar(self):
        # Valida planilla, usuario y estado de fase de planilla
        llOk = self.omInitContabilizarPlanilla()
        if not llOk:
           return False
        # Conectar base de datos           
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Carga parametros (rango para IR y valor de asignacion familiar)
        llOk = self.mxCargarParametros()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Elimina anterior contabilizacion si es reproceso
        llOk = self.mxEliminar()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Parametros de adelanto de quincena
        llOk = self.mxParamCntPlanilla()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Carga cuentas contables
        llOk = self.mxCuentasContables()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Numero de documento por oficina
        llOk = self.mxNumeroDocumentoOficina()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Graba adelanto de quincena
        llOk = self.mxGrabarCntPlanillas()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Graba contabilizacion de adelanto de quincena
#        llOk = self.mxCntPlanillas()
        if llOk:
           # Confirma la grabacion
           self.loSql.omCommit()
        self.loSql.omDisconnect()
        return llOk

    # Verifica planilla y valida si se puede hacer la contabilizacion OK
    def omInitContabilizarPlanilla(self):
        # Valida planilla, usuario y estado de fase de planilla
        llOk = self.mxValInit()
        if self.lcFases != '1111100000':
           self.pcError = '<DATA><ERROR>ESTADO DE FASES DE PLANILLA NO PERMITE CONTABILIZAR LA PLANILLA</ERROR></DATA>'
           return False
        self.pcData = '<DATA><CCODPLA>' + self.pcCodPla + '</CCODPLA><CDESCRI>' + self.pcDescri.strip() + '</CDESCRI></DATA>'
        return True

    # Carga parametros para contabilizar planilla 
    def mxCargarParametros(self):
        # Porcentaje descuento ESSALUD
        self.laAport = None
        i = 0
        RS = self.loSql.omExecRS("SELECT cCodigo, nValor FROM ADM.E10TPAR WHERE cCodigo IN ('PL0006', 'PL0007', 'PL0008')")
        for XCTA in RS:
            RS = self.loSql.omExecRS("SELECT cCtaCnt FROM ADM.E10TCNT WHERE cCodigo = '" + XCTA[0] + "'")   ## OJOFPM PARECE QUE NO ES NECESARIA LA CUENTA CONTABLE
            lcCtaCnt = RS[0][0]
            if lcCtaCnt == None:
               self.pcError = '<DATA><ERROR>NO EXISTE CODIGO CONTABLE PARA DESCUENTO ESSALUD [' + XCTA[0] + ']. INFORME A TI</ERROR></DATA>'
               return False
            self.laAporta.append([])
            self.laAporta[i].append(XCTA[0])
            self.laAporta[i].append(XCTA[1])
            self.laAporta[i].append(lcCtaCnt)
            i+=1
        if i != 3:
           self.pcError = '<DATA><ERROR>NO EXISTEN CODIGOS PARA ESSALUD [PL0003, PL0004, PL0005]. INFORME A TI</ERROR></DATA>'
           return False
        # Monto de asignacion familiar
        self.lnAsiFam = 75.00   # OJOFPM HAY QUE PARAMETRIZARLO
        # Rangos para impuesto a la renta
        self.laImpRen = [[3700*7, 0.15], [3700*14, 0.21], [3700*21, 0.30]]   # OJOFPM HAY QUE PARAMETRIZARLO
        return True

    # Elimina anterior contabilizacion
    def mxEliminar(self): #OJOFPM REVISAR SI SON LOS CONCEPTOS A ELIMINAR
        ''''
        lcSql = "DELETE FROM ADM.E01DTRX WHERE cCodigo IN (SELECT cCodigo FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "') AND (cConcep IN ('A01', 'A02') OR SUBSTRING(cConcep, 1, 1) IN ('C', 'E', 'N'))"
        llOk = self.loSql.omExec(lcSql)
        if not llOk:
           self.pcError = '<DATA><ERROR>NO SE PUDO ELIMINAR DATOS ANTERIORES. INFORME A TI</ERROR></DATA>'
        return llOk
        '''
        return True

    # Parametros de contabilizacion de pago de planilla
    def mxParamCntPlanilla(self):
        self.lcCodCnt = self.pcCodPla + 'PPL';
        RS = self.loSql.omExecRS("SELECT cConVar FROM S01TVAR WHERE cNomVar = 'GDFECSIS'")
        if len(RS) == 0:
           return False
        self.ldFecSis = RS[0][0]
        return True

    # Carga cuentas contables para pago de planilla
    def mxCuentasContables(self):
        i = 0
        self.laAfpCnt = []
        RS = self.loSql.omExecRS("SELECT cCodAfp, cConcep, cCtaCnt FROM ADM.f_CuentasContables() WHERE cConcep IN ('C02', 'C03', 'C04')")
        for XCNT in RS:
            self.laAfpCnt.append([])
            self.laAfpCnt[i].append(XCNT[0]+XCNT[1])
            self.laAfpCnt[i].append(XCNT[2])
            i+=1
        return True

        '''
        self.laCtaCnt = []
        RS = self.loSql.omExecRS("SELECT cCtaCnt, cDescri, cCodigo FROM ADM.E10TCNT WHERE cCodigo LIKE 'PL%' ORDER BY cCodigo")
        i = 0
        for XCNT in RS:
            lcCtaCnt = XCNT[0].strip() + '%'
            RS = self.loSql.omExecRS("SELECT COUNT(cCtaCnt) FROM CNT.D01MCTA WHERE cCtaCnt LIKE '" + lcCtaCnt + "'")
            if RS[0][0] > 1:
               self.pcError = '<DATA><ERROR>CUENTA CONTABLE [' + XCNT[0].strip() + '] NO ES DE ULTIMO NIVEL</ERROR></DATA>'
               return False
            self.laCtaCnt.append([])
            self.laCtaCnt[i].append(XCNT[0].strip())
            self.laCtaCnt[i].append(XCNT[1].strip())
            self.laCtaCnt[i].append(XCNT[2])
            i+=1
        if i == 0:
           self.pcError = '<DATA><ERROR>CUENTAS CONTABLES PARA PLANILLAS NO DEFINIDAS</ERROR></DATA>'
           return False
        '''

    # Genera y graba asiento contable de planillas
    def mxGrabarCntPlanillas(self):
        global lcCodOfi, lcConcep, lcCtaCnt, lcGlosa, lnMonto
        lcGlosa = 'PAGO PLANILLA ' + self.pcCodPla
        lcGlosa = lcGlosa[:90]
        # Elimina anteriores comprobantes contables de pago de planilla
        self.loSql.omExec("DELETE FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "'")
        # Trae pagos, descuentos no obligatorios, descuento r5ta, neto a pagar
        RS = self.loSql.omExecRS("SELECT cCodOfi, cConcep, nMonto, cCtaCnt FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND (SUBSTRING(cConcep, 1, 1) IN ('A', 'B', 'D', 'E') OR cConcep IN ('N10', 'C01')) ORDER BY cCodOfi, cConcep")
#        RS = self.loSql.omExecRS("SELECT cCodOfi, cConcep, nMonto, cCtaCnt FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND (SUBSTRING(cConcep, 1, 1) IN ('A', 'B', 'D', 'E') OR cConcep IN ('N10', 'C01')) AND cCodigo = '000001' ORDER BY cCodOfi, cConcep")
        if len(RS) == 0:
           self.pcError = '<DATA><ERROR>NO HAY EMPLEADOS DEFINIDOS PARA PLANILLA [' + self.pcCodPla + ']</ERROR></DATA>';
           return False
        lnMonto = 0
        lcCodOfi = '*'
        for XTRX in RS:
            if lcCodOfi == '*':
               lnMonto = 0
               lcCodOfi = XTRX[0]
               lcConcep = XTRX[1]
               lcCtaCnt = XTRX[3].strip()
            if lcCodOfi != XTRX[0] or lcConcep != XTRX[1]:
               llOk = self.mxGrabarTrxCnt()
               if not llOk:
                  return False
               lnMonto = XTRX[2]
               lcCodOfi = XTRX[0]
               lcConcep = XTRX[1]
               lcCtaCnt = XTRX[3].strip()
            else:
               lnMonto += XTRX[2]
        llOk = self.mxGrabarTrxCnt()
        if not llOk:
           return False
        # Trae aportaciones AFP
        RS = self.loSql.omExecRS("SELECT cCodOfi, cConcep, nMonto, cCodAfp FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND (cConcep IN ('C02', 'C03', 'C04')) ORDER BY cCodOfi, cCodAfp")
#        RS = self.loSql.omExecRS("SELECT cCodOfi, cConcep, nMonto, cCodAfp FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep IN ('C02', 'C03', 'C04') AND cCodigo = '000001' ORDER BY cCodOfi, cCodAfp")
        if len(RS) == 0:
           self.pcError = '<DATA><ERROR>NO HAY EMPLEADOS DEFINIDOS PARA PLANILLA [' + self.pcCodPla + ']</ERROR></DATA>';
           return False
        lnMonto = 0
        lcCodOfi = '*'
        for XTRX in RS:
            if lcCodOfi == '*':
               i = self.FindArray(self.laAfpCnt, XTRX[3]+XTRX[1])
               lcCtaCnt = self.laAfpCnt[i][1].strip()
               lnMonto = 0
               lcCodOfi = XTRX[0]
               lcCodAfp = XTRX[3]
               lcConcep = XTRX[1]
            if lcCodOfi != XTRX[0] or lcCodAfp != XTRX[3]:
               llOk = self.mxGrabarTrxCnt()
               if not llOk:
                  return False
               i = self.FindArray(self.laAfpCnt, XTRX[3]+XTRX[1])
               lcCtaCnt = self.laAfpCnt[i][1].strip()
               lnMonto = XTRX[2]
               lcCodOfi = XTRX[0]
               lcCodAfp = XTRX[3]
               lcConcep = XTRX[1]
            else:
               lnMonto += XTRX[2]
        llOk = self.mxGrabarTrxCnt()
        if not llOk:
           return False
        llOk = self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1111110000' WHERE cCodPla = '" + self.pcCodPla + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE FASES DE PLANILLAS [E01MPLA]</ERROR></DATA>'
           return False
        return True
        '''
        # Elimina anteriores comprobantes contables de pago de planilla
        self.loSql.omExec("DELETE FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "'")
        # Graba adelantos de quincena
        RS = self.loSql.omExecRS("SELECT cCodigo, cCodOfi, cNombre FROM ADM.V_E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        if len(RS) == 0:
           self.pcError = '<DATA><ERROR>NO HAY EMPLEADOS DEFINIDOS PARA PLANILLA [' + self.pcCodPla + ']</ERROR></DATA>';
           return False
        for XEMP in RS:
            lcCodigo = XEMP[0]
            lcCodOfi = XEMP[1]
            # Glosa
            lcData = 'PAGO PLANILLA ' + XEMP[2]
            lcData = lcData[:90]
            RS = self.loSql.omExecRS("SELECT A.cConcep, A.nMonto, B.cCtaCnt FROM ADM.E01DTRX A INNER JOIN ADM.E01TCON B ON A.cConcep = B.cConcep WHERE cCodigo = '" + lcCodigo + "' ORDER BY cConcep")
            if len(RS) == 0:
               self.pcError = '<DATA><ERROR>EMPLEADO NO TIENE TRANSACCIONES. INFORME A TI</ERROR></DATA>';
               return False
            lnAporta = 0
            for XTRX in RS:
                # Nro documento
                i = self.FindArray(self.laNroDoc, lcCodOfi)
                lcNroDoc = self.laNroDoc[i][1];
                if XTRX[0][:1] == 'A' or XTRX[0][:1] == 'B':
                   lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nDebeC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + XTRX[2] + "', '" + lcData + "', " + str(XTRX[1]) + ", '" + self.pcCodUsu + "')"
 #                  print lcSql
                   llOk = self.loSql.omExec(lcSql)
                   if not llOk:
                      self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE TABLA CONTABLE [ADM.E10DCNT]</ERROR></DATA>'
                      return False
                elif XTRX[0][:1] == 'C' or XTRX[0][:1] == 'D':
                   lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + XTRX[2] + "', '" + lcData + "', " + str(XTRX[1]) + ", '" + self.pcCodUsu + "')"
                   llOk = self.loSql.omExec(lcSql)
                   if not llOk:
                      self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE TABLA CONTABLE [ADM.E10DCNT]</ERROR></DATA>'
                      return False
                elif XTRX[0] == 'N10':
                   lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + XTRX[2] + "', '" + lcData + "', " + str(XTRX[1]) + ", '" + self.pcCodUsu + "')"
                   llOk = self.loSql.omExec(lcSql)
                   if not llOk:
                      self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE TABLA CONTABLE [ADM.E10DCNT]</ERROR></DATA>'
                      return False
                elif XTRX[0][:1] == 'E':
                   lnAporta += XTRX[1]
                   lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + XTRX[2] + "', '" + lcData + "', " + str(lnAporta) + ", '" + self.pcCodUsu + "')"
                   llOk = self.loSql.omExec(lcSql)
                   if not llOk:
                      self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE TABLA CONTABLE [ADM.E10DCNT]</ERROR></DATA>'
                      return False
            lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nDebeC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + XTRX[2] + "', '" + lcData + "', " + str(lnAporta) + ", '" + self.pcCodUsu + "')"
#            print lcSql
            llOk = self.loSql.omExec(lcSql)
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE TABLA CONTABLE [ADM.E10DCNT]</ERROR></DATA>'
               return False
        llOk = self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1111110000' WHERE cCodPla = '" + self.pcCodPla + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE FASES DE PLANILLAS [E01MPLA]</ERROR></DATA>'
           return False
        return True
        '''

    # Graba registro de transaccion contable
#    def mxGrabarTrxCnt(p_cCodOfi, p_cConcep, p_cCtaCnt, p_nMonto, p_cGlosa):
    def mxGrabarTrxCnt(self):
        # Descripcion de cuenta contable
        RS = self.loSql.omExecRS("SELECT cDescri FROM CNT.D01MCTA WHERE cCtaCnt = '" + lcCtaCnt + "'")
        if len(RS) == 0:
           lcGlosa = '*** ERROR ***'
        else:
           lcGlosa = RS[0][0]
        # Nro documento
        i = self.FindArray(self.laNroDoc, lcCodOfi)
        lcNroDoc = self.laNroDoc[i][1];
        if lcConcep[:1] == 'A' or lcConcep[:1] == 'B':
           lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nDebeC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + lcCtaCnt + "', '" + lcGlosa + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
#        elif lcConcep[:1] == 'C' or lcConcep[:1] == 'D':
#           lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + lcCtaCnt + "', '" + lcGlosa + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        elif lcConcep[:1] == 'C':
#           print lcConcep, lnMonto
           lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + lcCtaCnt + "', '" + lcGlosa + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        elif lcConcep[:1] == 'D':
           lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + lcCtaCnt + "', '" + lcGlosa + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        elif lcConcep == 'N10':
           lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + lcCtaCnt + "', '" + lcGlosa + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        elif lcConcep[:1] == 'E':
           lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + lcCtaCnt + "', '" + lcGlosa + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
           llOk = self.loSql.omExec(lcSql)
           if not llOk:
              self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE TABLA CONTABLE [ADM.E10DCNT]</ERROR></DATA>'
              return False
           lcCntCta = '*'
           if lcConcep == 'E01':
              RS = self.loSql.omExecRS("SELECT cCtaCnt FROM ADM.E01TCON WHERE cConcep = 'E02'")
              lcCntCta = RS[0][0]
           elif lcConcep == 'E03':
              RS = self.loSql.omExecRS("SELECT cCtaCnt FROM ADM.E01TCON WHERE cConcep = 'E04'")
              lcCntCta = RS[0][0]
           lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nDebeC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + lcCntCta + "', '" + lcGlosa + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        else:
           return True
        llOk = self.loSql.omExec(lcSql)
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE TABLA CONTABLE [ADM.E10DCNT]</ERROR></DATA>'
           return False
        return True

    # Graba adelanto de quincena en contabilidad
    def mxCntPlanillas(self):
        # Periodo
        lcPeriod = self.pcCodPla[:4]
        lcNroDoc = '*'
        # Trae movimientos contables
        RS = self.loSql.omExecRS("SELECT cNroDoc, cCtaCnt, nDebeC, nHaberC, cGlosa FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "' ORDER BY cNroDoc, cCtaCnt")
        for XCNT in RS:
            if XCNT[0] != lcNroDoc:
               # Documento de referencia
               lcNroDoc = XCNT[0]
               # Numero de comprobante
               lcNroCom = XCNT[0][:2] + 'PL' + lcPeriod
               lcNroCom = self.mxNroComprobante(lcNroCom)
               # Graba cabecera de comprobante contable
               lcSql = "INSERT INTO CNT.D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" + lcNroCom + "', '" + lcNroDoc + "', '', '" + lcNroDoc[:2] + "', 'S', 'ADELANTO DE QUINCENA', 'RI', '', '', '', '', '" + str(self.ldFecSis) + "', '', '', '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql) 
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE CABECERA DE COMPROBANTES CONTABLES [CNT.D01MDIA]</ERROR></DATA>'
                  return False
            # Graba detalle de comprobante contable
            lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + XCNT[1] + "', '" + XCNT[4] + "', 0, 0, " + str(XCNT[2]) + ", " + str(XCNT[3]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
            llOk = self.loSql.omExec(lcSql)
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
               return False
        self.pcData = '<DATA><MENSAJE>GENERACION QUINCENA CONFORME</MENSAJE></DATA>';
        return True

