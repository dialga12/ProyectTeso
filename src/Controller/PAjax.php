<?php
   require_once 'Libs/Smarty.class.php';
   require_once 'Clases/CBase.php';
   require_once 'Clases/CSql.php';
   session_start();
   $loSmarty = new Smarty;
   $lcNroIde = $_GET['Id'];
   $lcNroStr = $_GET['nombre'];
   if ($lcNroIde == '001') {
      fxProvincias();
   } elseif ($lcNroIde == '100') {
      fxIniciarCampo();
   } elseif ($lcNroIde == '101') {
      fxNuevoCampo();
   } elseif ($lcNroIde == '102') {
      fxEliminarCampo();
   } elseif ($lcNroIde == '003_') {
      // Busca proveedores por descripcion
      $lcDescri = $_GET['des'];
      $laData = null;
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $loSmarty->assign('scShow', '01');
         $loSmarty->assign('saData', $laData);
         $loSmarty->assign('scError', $loSql->pcError);
         $loSmarty->display('Plantillas/Aut9000.tpl');
         return;
      }
      $lcSql = "SELECT * FROM (SELECT DISTINCT TRIM(CPMPNOMPRV) AS CPMPNOMPRV, CPMPNEWRUC FROM CPDMPROV WHERE CPMPNOMPRV LIKE '%$lcDescri%') ORDER BY CPMPNOMPRV";
      $RS = $loSql->omExec($lcSql);
      while ($laFila = $loSql->fetch($RS)) {
         $laData[] = array($laFila[0], $laFila[1]);
      }      
      $loSql->omDisconnect();
      $loSmarty->assign('scShow', '01');
      $loSmarty->assign('saData', $laData);
      $loSmarty->display('Plantillas/Aut9000.tpl');
      return;
   } elseif ($lcNroIde == '002') {
      $pcNomPrv = trim(strtoupper($_REQUEST["des"]));
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      /*if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }*/
      $laData = null;
      $lcSql = "SELECT * FROM (SELECT DISTINCT TRIM(CPMPNOMPRV) AS CPMPNOMPRV, CPMPNEWRUC FROM CPDMPROV WHERE CPMPNOMPRV LIKE '%$pcNomPrv%') ORDER BY CPMPNOMPRV";
      $RS = $loSql->omExec($lcSql);
      while ($laFila = $loSql->fetch($RS)) {
         $laData[] = array($laFila[0], $laFila[1]);
      }      
      $loSql->omDisconnect();
      $loSmarty->assign('saData', $laData);
      $loSmarty->display('Plantillas/Aut9122.tpl');
   }  elseif ($lcNroIde == '006_') {
      $lcMoneda = $_GET['moneda'];
      $lnMonto  = $_GET['monto'] * 1;
      $i = 1;
      $llOk = false;
      foreach($_SESSION['paRangos'] as $laFila) {
         if (($lcMoneda == '2' and $lnMonto <= $laFila[0]) or ($lcMoneda == '1' and $lnMonto <= $laFila[1])) {
            $llOk = true;
            break;
         }
         $i++;
      }
      $lcFlag = ($llOk) ? (string)$i : '0';
      echo "{'CFLAG': '$lcFlag'}";
   }  elseif ($lcNroIde == '007a') {   // ANTIGUO
      // Personal responsable por centro de costo
      $lcCenCos = $_GET['cc'];
      $llFirst = true;
      $lcTexto = "[";
      foreach ($_SESSION['paRepCen'] as $laTmp) {
         Traceo('* '.$laTmp[2].'-'.$lcCenCos);
         if (trim($laTmp[2]) == trim($lcCenCos)) {
            if (!$llFirst) {
               $lcTexto .= ',';
            }
            $llFirst = false;
            $lcTexto .= "{'CCODPER': '$laTmp[0]', 'CNOMBRE': '$laTmp[1]'}";            
         }
      }
      if (!$llFirst) {
         // Hay personal para el centro de costo
         $lcTexto .= ']';
         Traceo($lcTexto);
         echo $lcTexto;
         return;
      }
      // Si no hay personal para centro de costo 
      $llFirst = true;
      $lcTexto = "[";
      foreach ($_SESSION['paRepLg1'] as $laTmp) {
         if (!$llFirst) {
            $lcTexto .= ',';
         }
         $llFirst = false;
         $lcTexto .= "{'CCODPER': '$laTmp[0]', 'CNOMBRE': '$laTmp[1]'}";            
      }
      $lcTexto .= ']';
      echo $lcTexto;
      return;
   } elseif ($lcNroIde == '007') {
      // Personal responsable por centro de costo
      fxPersonalCentroCosto();
      return;
   } elseif ($lcNroIde == '008') {
      // Objeto de contrato
      fxObjetoContrato();
      return;
   }
   
   function fxIniciarCampo() {
      global $loSmarty;
      $vacio = array("","","","","","","","","","",'','');
      $laDatos = array($vacio);
      $_SESSION['paDatos'] = $laDatos;
      $loSmarty->assign('saDatos', $laDatos);
      $loSmarty->display('Plantillas/Caj1011.tpl');
      return;
   }


   function fxNuevoCampo() {
      global $loSmarty;
      $vacio = array(array('','','','','','','','','','','',''));
      $laDatos = $_SESSION['paDatos'];
      $laDatos = array_merge($laDatos,$vacio);
      $_SESSION['paDatos'] = $laDatos;
      $loSmarty->assign('saDatos', $laDatos);
      $loSmarty->display('Plantillas/Caj1011.tpl');
      return;
   }

   function fxEliminarCampo(){
      global $loSmarty;
      $laDatos = $_SESSION['paDatos'];
      $laCheck = $_GET['nombre'];
      echo($laCheck);
      //Eliminacion
      $laData1 = null;
      foreach ($laDatos as $i){
         if($i[0] != $laCheck){
            $laData1[] = array ($i[0],$i[1]);
         }
      }
      $_SESSION['paDatos'] = $laData1;
      $laDatos = $_SESSION['paDatos'];
      $loSmarty->assign('saDatos', $laDatos);
      $loSmarty->display('Plantillas/Caj1011.tpl');
   }

   function fxProvincias() {
      $lcDepart = $_GET['dpt'];
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      /*if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }*/
      $laData = null;
      $lcSql = "SELECT SUBSTR(cUbigeo, 1, 4), cDescri FROM S01TUBG WHERE SUBSTR(cUbigeo, 1, 2) = '$lcDepart' AND cTipo = '2' ORDER BY cDescri";
      $RS = $loSql->omExec($lcSql);
      $lcTexto = "[";
      $llFirst = true;
      while ($laFila = $loSql->fetch($RS)) {
         if (!$llFirst) {
            $lcTexto .= ',';
         }
         $llFirst = false;
         $lcTexto .= "{'CUBIGEO': '$laFila[0]', 'CDESCRI': '$laFila[1]'}";            
      }      
      $lcTexto .= ']';
      $loSql->omDisconnect();
      echo $lcTexto;
      return;
   }
   
   function fxDatosProducto() {
      $lcProduc = $_GET['prd'];
      Traceo($lcProduc);
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      /*if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }*/
      $laData = null;
      $lcSql = "SELECT cDesMon, cDesDes FROM V_C02MPRD WHERE cProduc = '$lcProduc'";
      Traceo($lcSql);
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      $lcDesMon = trim($laFila[0]);
      $lcDesDes = trim($laFila[1]);
      $lcTexto = "[{'CDESMON': '$lcDesMon', 'CDESDES': '$lcDesDes'}]";            
      Traceo($lcTexto);
      $loSql->omDisconnect();
      echo $lcTexto;
      return;
   }

   function fxLineaAhorros() {
      $lcLinea = $_GET['ln'];
      Traceo($lcLinea,'0');
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      /*if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }*/
      $laData = null;
      $lcSql = "SELECT cDesmon, cDesSer FROM V_A01MLIN  WHERE cLinea = '$lcLinea'";
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      $lcDesMon = trim($laFila[0]);
      $lcDesSer = trim($laFila[1]);
      
      $lcSql = "SELECT nTasInt FROM A01MLIN  WHERE cLinea = '$lcLinea'";
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);      
      $lcTasint = trim($laFila[0]);
      $lcTexto = "[{'CDESMON': '$lcDesMon', 'CTASINT': '$lcTasint', 'CDESSER': '$lcDesSer'}]";            
      Traceo($lcTexto);
      $loSql->omDisconnect();
      echo $lcTexto;
      return;
   }

   function fxNuevoCliente() {
      global $loSmarty;
      $laDatos = $_SESSION['paDatos'];
      $lcNroDni = $_GET['str'];
      //Si se repite no hace nada
      foreach ($laDatos as $i){
         if($i[0] == $lcNroDni)
            return;
      }
      //busca dni en C01MIDE
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
      $lcSql = "SELECT cNroDni, cNomCli, cCodCli FROM C01MIDE WHERE cNroDni = '$lcNroDni'";
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      $loSql->omDisconnect();
      if(empty($laFila[0])){
         
      }else{
        $laDatos[] = array ($laFila[0] , $laFila[1], $laFila[2]);
      }    
      $_SESSION['paDatos'] = $laDatos;
      $loSmarty->assign('saDatos', $laDatos);
      $loSmarty->display('Plantillas/Cli1321.tpl');
      // 0: CCODFUE
      // 1: CTIPREL
      // 2: CCARGO
      // 3: CESTADO
      // 4: DINGRES
      // 5: NMONING
      return;
   }

   function fxActualizarCliente() {
      global $loSmarty;
      Traceo("Arribo",0);
      $laDatos = $_SESSION['paDatos'];   
      $loSmarty->assign('saDatos', $laDatos);
      $loSmarty->display('Plantillas/Cli1321.tpl');
      return;
   }

   function fxEliminarCliente() {
      global $loSmarty;
      $laDatos = $_SESSION['paDatos'];
      $laCheck = $_GET['str'];
      //eliminar
      $laData1 = null;
      foreach($laDatos as $i) {
         if ($i[0] != $laCheck){
            $laData1[] = array ($i[0] , $i[1]);
         }
      }
      //print_r($laData1);      
      Traceo('YYY'.$laCheck.'XzX',0);
      $_SESSION['paDatos'] = $laData1;
      $laDatos = $_SESSION['paDatos'];
      $loSmarty->assign('saDatos', $laDatos);
      $loSmarty->display('Plantillas/Cli1321.tpl');
      return;
   }

   function fxNombreCliente() {
      $lcNroDni = $_GET['cl'];
      Traceo($lcNroDni);
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      /*if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }*/
      $laData = null;
      $lcSql = "SELECT cNomCli FROM C01MIDE WHERE cNroDni = '$lcNroDni'";
      Traceo($lcSql);
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      $lcNomCli = (empty($laFila[0])) ? '*** ERROR ***' : trim($laFila[0]);
      $lcTexto = "[{'CNOMCLI': '$lcNomCli'}]";            
      Traceo($lcTexto);
      $loSql->omDisconnect();
      echo $lcTexto;
      return;
   }

   function fxNombreUsuario() {
      $lcNroDni = $_GET['dni'];
      Traceo($lcNroDni);
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      /*if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }*/
      $laData = null;
      $lcSql = "SELECT cNombre FROM S01MPER WHERE cNroDni = '$lcNroDni'";
      Traceo($lcSql);
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      $lcNombre = (empty($laFila[0])) ? '*** ERROR ***' : trim($laFila[0]);
      $lcTexto = "[{'CNOMBRE': '$lcNombre'}]";            
      Traceo($lcTexto);
      $loSql->omDisconnect();
      echo $lcTexto;
      return;
   }
   
   function fxDistritos() {
      $lcProvin = $_GET['prv'];
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      /*if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }*/
      $laData = null;
      $lcSql = "SELECT SUBSTR(cUbigeo, 1, 6), cDescri FROM S01TUBG WHERE SUBSTR(cUbigeo, 1, 4) = '$lcProvin' AND cTipo = '3' ORDER BY cDescri";
      $RS = $loSql->omExec($lcSql);
      $lcTexto = "[";
      $llFirst = true;
      while ($laFila = $loSql->fetch($RS)) {
         if (!$llFirst) {
            $lcTexto .= ',';
         }
         $llFirst = false;
         $lcTexto .= "{'CUBIGEO': '$laFila[0]', 'CDESCRI': '$laFila[1]'}";            
      }      
      $lcTexto .= ']';
      $loSql->omDisconnect();
      echo $lcTexto;
      return;
   }
   
   function fxNuevoAval() {
      global $loSmarty;
      $laDatos = $_SESSION['paDatos'];
      $lcNroDni = $_GET['str'];
      //busca dni en C01MIDE
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
      $lcSql = "SELECT cCodCli, cNroDni, cNomCli FROM C01MIDE WHERE cNroDni = '$lcNroDni'";
      echo $lcSql;
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      $loSql->omDisconnect();
      if(empty($laFila[0])){
         
      }else{
        $laDatos = array ($laFila[0] , $laFila[1],  $laFila[2]);
      }      
      $_SESSION['paDatos'] = $laDatos;
      $loSmarty->assign('saDatos', $laDatos);
      $loSmarty->display('Plantillas/Cli1311.tpl');
      // 0: CCODFUE
      // 1: CTIPREL
      // 2: CCARGO
      // 3: CESTADO
      // 4: DINGRES
      // 5: NMONING
      return;
   }
   
   function fxActualizarAval() {
      global $loSmarty;
      $laDatos = $_SESSION['paCodAva'];      
      $loSmarty->assign('saDatos', $laDatos);
      $loSmarty->display('Plantillas/Cli1311.tpl');
      return;
   }
      
   function fxDniCliente() {
      global $loSmarty;
      $laDatos = $_SESSION['paDatos'];
      if ($_GET['flag']==1){
         $laDatos[] = array('', '', '', 'A', '', 0);
      }
      $_SESSION['paDatos'] = $laDatos;
      print_r($_SESSION['paDatos']);
      $loSmarty->assign('saDatos', $laDatos);
      $loSmarty->assign('saTipRel', $_SESSION['paTipRel']);
      $loSmarty->assign('saEstado', $_SESSION['paEstado']);
      $loSmarty->assign('saCargo', $_SESSION['paCargo']);      
      $loSmarty->assign('saCodFue', $_SESSION['paCodFue']);
      $loSmarty->display('Plantillas/Cli1231.tpl');
      // 0: CCODFUE
      // 1: CTIPREL
      // 2: CCARGO
      // 3: CESTADO
      // 4: DINGRES
      // 5: NMONING
      return;
   }
   //////////////////////   

   function fxPersonalCentroCosto() {
      $lcCenCos = $_GET['cc'];
      $lcCodPer = $_GET['usu'];
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      //if (!$llOk) {
      //   return false;
      //}
      // Saca email de usuario responsable
      $lcSql = "SELECT cEmail FROM S03MPER WHERE cCodPer = '$lcCodPer'";
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      $lcEmail = trim($laFila[0]);
      $lcEmail = ($lcCodPer == '000014') ? 'jnunez@fetrasa.com': $lcEmail;   // OJOFPM
      // Trae personal aprobador de centro de costo
      $laTmp = null;
      $lcSql = "SELECT DISTINCT CORREOA FROM VP_PLNMAETRA, PLNMAETRA
                WHERE CORREOS = '$lcEmail' AND PTRNROLE = CODIGOA AND PTRCENCOS = $lcCenCos";
      $RS = $loSql->omExec($lcSql);
      while ($laFila = $loSql->fetch($RS)) {
         $laTmp[] = array($laFila[0]);
      }
      // Trae codigo de personal aprobador
      $i = 0;
      $laData = null;
      foreach ($laTmp as $j) {
         $lcSql = "SELECT cCodPer, cNombre FROM S03MPER WHERE cEmail = TRIM('$j[0]')";
         $RS = $loSql->omExec($lcSql);
         $laFila = $loSql->fetch($RS);
         if (empty($laFila[0])) {
            continue;
         }
         $laData[] = array($laFila[0], $laFila[1]);
         $i++;
      }
      if ($i == 0) {
         $laData[] = array('*', '[NO HAY APROBADORES]');
      }
      $loSql->omDisconnect();
      // Construye JSON de retorno
      $llFirst = true;
      $lcTexto = "[";
      foreach ($laData as $laTmp) {
         if (!$llFirst) {
            $lcTexto .= ',';
         }
         $llFirst = false;
         $lcTexto .= "{'CCODPER': '$laTmp[0]', 'CNOMBRE': '$laTmp[1]'}";            
      }
      $lcTexto .= ']';
      echo $lcTexto;
      return;
   }

   function fxObjetoContrato() {
      $lcCodUni = $_GET['ctt'];
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      //if (!$llOk) {
      //   return false;
      //}
      // Saca email de usuario responsable
      $lcSql = "SELECT cObjeto FROM S03MCTT WHERE cCodUni = '$lcCodUni'";
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      $loSql->omDisconnect();
      $lcResult = '*** '.$lcCodUni.' *** '.$laFila[0];
      $lcTexto = "{'COBJETO': '$lcResult'}";
      echo $lcTexto;
      return;
   }
   
   function Traceo($p_cTexto, $p_nFlag = 1) {
      $lcTipo = ($p_nFlag == 0) ? 'w' : 'a';
      $loFile = fopen('fpm.txt', $lcTipo);
      fputs($loFile, $p_cTexto);
      fclose($loFile);
  }
  function fxCargaDatos() {
      $lcLinea = $_GET['str'];
      $lnCapita = $_GET['str1'];
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      $lcSql = "SELECT A.nTasInt, A.nTasMor, B.cMoneda, C.cDescri as cDesMon FROM C02DPRD A
                INNER JOIN C02MPRD B ON A.cProduc = B.cproduc
                LEFT OUTER JOIN V_S01TTAB C ON C.CCODTAB = '007' AND C.CCODIGO = B.cMoneda 
                WHERE $lnCapita BETWEEN A.nRango1 AND A.nRango2 AND B.cProduc = '$lcLinea'";
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      if(empty($laFila[0])){
         $lcTexto = "{'NTASINT': '***ERROR***', 'NTASMOR': '***ERROR***', 'CMONEDA': '***ERROR***', 'CDESMON': '***ERROR***'}"; 
      }else{
         $lcTexto = "{'NTASINT': '$laFila[0]', 'NTASMOR': '$laFila[1]', 'CMONEDA': '$laFila[2]', 'CDESMON': '$laFila[3]'}";
      }
      
      echo $lcTexto;
   }
?> 