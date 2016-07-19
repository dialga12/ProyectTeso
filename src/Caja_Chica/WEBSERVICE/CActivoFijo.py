# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from decimal import *
from CBase import *

#########################################################
## Clase que procesa los activos fijos
#########################################################
class CActivoFijo(CBase):
    pcTermId = None
    lcCodCnt = None
    lcCtaAde = None
    lcCtaInt = None
    lcDescri = None
    ldFecSis = None
    lcPeriod = None
    lnTipCam = None
    laCtaCnt = []
    laNroDoc = []
        
    # Genera la depreciacion
    def omDepreciacion(self):
        if self.pcCodUsu == None or self.pcCodUsu.strip() == '':
           self.pcError = 'CODIGO DE USUARIO NO DEFINIDO'
           return False
        elif self.pcTermId == None or self.pcTermId.strip() == '':
           self.pcError = 'IDENTIFICACION DE TERMINAL NO DEFINIDO'
           return False
        # Conectar base de datos
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Verifica si se puede realizar la depreciacion
        llOk = self.mxVerificar()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Carga y valida cuentas contables
        llOk = self.mxCuentasContables()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Realiza la depreciacion
        llOk = self.mxDepreciacion()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Genera los movimientos contables
        llOk = self.mxCntDepreciacion()
        if llOk:
           # Confirma la grabacion
           self.loSql.omCommit()
        self.loSql.omDisconnect()
        return llOk

    # Verifica si se puede realizar la depreciacion
    def mxVerificar(self):
        # Carga fecha de proceso
        RS = self.loSql.omExecRS("SELECT cConVar FROM S01TVAR WHERE cNomVar = 'GDFECSIS'")
        if RS == None:
           self.pcError = '<DATA><ERROR>NO HAY FECHA DE PROCESO DEFINIDA [GDFECSIS]</ERROR></DATA>'
           return False
        # Periodo
        self.ldFecSis = RS[0][0]
        self.lcPeriod = self.ldFecSis[:4] + self.ldFecSis[5:7]
        self.lcCodCnt = self.lcPeriod[2:] + 'DP'
        RS = self.loSql.omExecRS("SELECT cCodAfj FROM ADM.E03DDEP WHERE cPeriod = '" + self.lcPeriod[2:] + "'")
        if RS != None:
           self.pcError = '<DATA><ERROR>DEPRECIACION DE PERIODO YA HA SIDO REALIZADA</ERROR></DATA>'
           return False
        # Carga tipo de cambio
        RS = self.loSql.omExecRS("SELECT nTipFij FROM CNT.D01DCAM WHERE dCambio = '" + self.ldFecSis + "' ORDER BY tModifi DESC LIMIT 1")
        if RS == None:
           self.pcError = '<DATA><ERROR>NO HAY TIPO DE CAMBIO PARA FECHA [' + self.ldFecSis + ']</ERROR></DATA>'
           return False
        self.lnTipCam = RS[0][0]
        return True
    '''
    PARA ELIMINAR DEPRECIACION
    DELETE FROM CNT.D01DMOV WHERE cNroCom IN (SELECT cNroCom FROM CNT.D01MDIA WHERE cDocRef IN 
   (SELECT DISTINCT cNroDoc FROM ADM.E10DCNT WHERE cCodCnt = '1301DP'));
DELETE FROM CNT.D01MDIA WHERE cDocRef IN 
   (SELECT DISTINCT cNroDoc FROM ADM.E10DCNT WHERE cCodCnt = '1301DP');
delete from adm.e10dcnt where ccodcnt = '1301DP';
delete from adm.e03ddep where cperiod = '1301';

    '''
        
    # Recupera y valida las cuentas contables
    def mxCuentasContables(self):
        return True
        
    # Realiza la depreciacion
    def mxDepreciacion(self):
        # Numero de documento por oficina
        llOk = self.mxNumeroDocumentoOficina()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Cuenta de depreciacion
        lcCtaDep = '1619010201'   ## OJOFPM HAY QUE PARAMETRIZAR
        # Trae activos fijos para depreciar
        RS = self.loSql.omExecRS("SELECT cCodAfj, nTasDep, nPrecio, dFecIng, cDescri, '01' AS cCodOfi, TRIM(cCtaCnt) FROM ADM.E03MAFJ WHERE cEstado = 'A'")
        if RS == None:
           self.pcError = '<DATA><ERROR>NO HAY ACTIVOS FIJOS PARA DEPRECIAR</ERROR></DATA>';
           return False
        # Fecha de referencia del mes para depreciar el AF
        ldFecha = self.mxValDate(self.ldFecSis[:8] + '15')
        if ldFecha == None:
           self.pcError = '<DATA><ERROR>NO SE PUDO CONSTRUIR FECHA DE REFERENCIA DEL MES PARA DEPRECIAR [' + self.ldFecSis[:8] + '15]. AVISE A TI</ERROR></DATA>';
           return False
        for XAFJ in RS:
            # Verifica fecha de ingreso
            if XAFJ[3] > ldFecha:
               loop
            # Valida la cuenta contable
            lcCtaCnt = XAFJ[6].strip() + '%'
            RS = self.loSql.omExecRS("SELECT cCtaCnt FROM CNT.D01MCTA WHERE cCtaCnt LIKE '" + lcCtaCnt + "'")
            if RS == None:
               self.pcError = '<DATA><ERROR>CUENTA CONTABLE NO ESTA DEFINIDA [' + XAFJ[6].strip() + ']</ERROR></DATA>';
               return False
            elif len(RS) == 0:
               self.pcError = '<DATA><ERROR>CUENTA CONTABLE NO ES DE ULTIMO NIVEL [' + XAFJ[6].strip() + ']</ERROR></DATA>';
               return False
            # Si es mes 12 deprecia por diferencia
            if self.lcPeriod[-2:] == '12':
               # Halla meses a depreciar
               if XAFJ[3] <= self.ldFecSis[:5] + '01-15':
                  lnMeses = 12
               else:
                  lnMeses = 12 - int(XAFJ[3][5:][:2])
                  if XAFJ[3][-2:] < '15':
                     lnMeses = 12 + 1
               # Total depreciacion del anho
               lnDeprec = XAFJ[1] * XAFJ[2] * lnMeses / 1200
               # Depreciacion acumulada del anho
               lnDepAcu = 0
               RS = self.loSql.omExecRS("SELECT SUM(nMonDep) FROM ADM.E03DDEP WHERE cCodAfj = '" + XAFJ[0] + "' AND SUBSTRING(cPeriod, 1, 2) = '" + self.pcPeriod[:2] + "'")
               if RS != None:
                  lnDepAcu = RS[0][0]
               # Depreciacion del mes
               lnDeprec = lnDeprec - lnDepAcu   ## OJOFPM QUE PASA SI ES NEGATIVOS
            else:
               lnDeprec = XAFJ[1] * XAFJ[2] / 1200
            # Graba depreciacion
            llOk = self.loSql.omExec("INSERT INTO ADM.E03DDEP (cCodAfj, cPeriod, nMonDep, cCodUsu) VALUES ('" + XAFJ[0] + "', '" + self.lcCodCnt[:4] + "', " + str(lnDeprec) + ", '" + self.pcCodUsu + "')")
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR AL GRABAR TABLA DE DEPRECIACION [E03DDEP]. AVISE A TI</ERROR></DATA>';
               return False
            # Oficina
            i = self.FindArray(self.laNroDoc, XAFJ[5])
            lcNroDoc = self.laNroDoc[i][1]
            lcGlosa = 'DEPRECIACION [' + XAFJ[0] + '] [' + self.lcPeriod + ']'
            # Asiento de adelanto de quincena por oficina
            self.loSql.omExec("INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nDebeC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + self.ldFecSis + "', '" + XAFJ[6] + "', '" + lcGlosa + "', " + str(lnDeprec) + ", '" + self.pcCodUsu + "')")
            self.loSql.omExec("INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + self.ldFecSis + "', '" + lcCtaDep + "', '" + lcGlosa + "', " + str(lnDeprec) + ", '" + self.pcCodUsu + "')")
        self.loSql.omCommit()
        return True
        
    # Graba los movimientos contables de depreciacion
    def mxCntDepreciacion(self):
        lcNroDoc = '*'
        RS = self.loSql.omExecRS("SELECT cNroDoc, cCtaCnt, nDebeC, nHaberC, cGlosa FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "' ORDER BY cNroDoc, cCtaCnt")
        for XCNT in RS:
            if XCNT[0] != lcNroDoc:
               # Graba cabecera de comprobante contable
               lcNroDoc = XCNT[0]
               lcNroCom = lcNroDoc[:2] + 'AF01'
               lcNroCom = self.mxNroComprobante(lcNroCom)
               # cTipDoc = 'RI' [803]
               lcSql = "INSERT INTO CNT.D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" + lcNroCom + "', '" + lcNroDoc + "', '', '" + lcNroDoc[:2] + "', 'S', 'ADELANTO DE COMISION', 'RI', '', '', '', '', '" + self.ldFecSis + "', '', '', '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
            # Graba detalle de comprobante contable
            lcGlosa = XCNT[4]
            lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + XCNT[1] + "', '" + lcGlosa + "', 0, 0, " + str(XCNT[2]) + ", " + str(XCNT[3]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql) 
        self.loSql.omCommit()
        self.pcData = '<DATA><MENSAJE>GENERACION DE DEPRECIACION CONFORME</MENSAJE></DATA>';
        return True

    def mxNumeroDocumentoOficina(self):
        j = 0
        RS = self.loSql.omExecRS('SELECT cCodOfi FROM S01TOFI ORDER BY cCodOfi')
        for XOFI in RS:
            lcCodigo = XOFI[0] + self.pcTermId + '10'
            lcSql = "SELECT MAX(cNroDoc) FROM ADM.E10DCNT WHERE SUBSTRING(cNroDoc, 1, 7) = '" + lcCodigo + "'"
            RS1 = self.loSql.omExecRS(lcSql)
            if RS1 == None or RS1[0][0] == None:
               lcNumero = '00000'
            else:
               lcNumero = RS1[0][0]
               lcNumero = lcNumero[-5:]   # 6 digitos de la derecha
            i = int(lcNumero) + 1
            lcNumero = '0000' + str(i)
            lcNumero = lcNumero[-5:]
            self.laNroDoc.append([])
            self.laNroDoc[j].append(XOFI[0])
            self.laNroDoc[j].append(XOFI[0] + self.pcTermId + '09' + lcNumero)
            self.laNroDoc[j].append(0)
            j += 1
        # Verifica si hay oficinas            
        if j == 0:
           self.pcError = '<DATA><ERROR>NO HAY OFICINAS DEFINIDASŗ</ERROR></DATA>'
           return False
        return True

# python fer.py <DATA><CLASS>CACTIVOFIJO</CLASS><METHOD>DEPRECIACION</METHOD><CCODUSU>9999</CCODUSU><CTERMID>0001</CTERMID></DATA>



