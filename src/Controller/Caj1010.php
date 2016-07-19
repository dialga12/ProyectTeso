<?php
   // Registro y mantenimiento de empleados
   require_once 'Libs/Smarty.class.php';
   require_once 'Clases/CRCuentas.php';
   session_cache_limiter();
   session_start();
   $loSmarty = new Smarty;
   if (@$_POST['Boton1'] == 'Abrir') {
      fxAbrir();
   } elseif (@$_POST['Boton1'] == 'Eliminar') {
      $_SESSION['plNuevo'] = false;
      fxEditar();
   } elseif (@$_POST['Boton2'] == 'Grabar') {
      fxGrabar();
   } elseif (@$_POST['Boton1'] == 'Salir') {
      header('Location: Mnu0000.php?Id=4000');
   } elseif (@$_POST['Boton2'] == 'Cancelar') {
      fxScreen();
   }  else {
      fxInit();
   }
   
   // Funciones auxiliares
   function fxInit() {
      global $loSmarty;
      $lcCodUsu = $_SESSION['gcCodUsu'];
      $lcNombre = $_SESSION['gcNombre'];
      $lo = new CRCuentas();
      $llOk = $lo->omBuscarRendicion();
      if (!$llOk) {
         fxAlert($lo->pcError);
         header('Location: Mnu0000.php?Id=4000');
      } else {
         echo('$lo->paIdenti');
         $_SESSION['paIdenti']=$lo->paIdenti;
         fxScreen();
      }
   }

   function fxAbrir(){
      global $loSmarty;
      $_SESSION['pcIdenti'] = $_REQUEST['pcIdenti'];
      $lo = new CRCuentas();
      $lo->paData = array('CIDENTI' => $_REQUEST['pcIdenti']);
      $llOk = $lo->omIniciarRegistro();
      if (!$llOk) {
         fxAlert($lo->pcError);
         header('Location: Mnu0000.php?Id=4000');
      } else {
         $_SESSION['paIdenti']=$lo->paData;
         fxScreen1();
      }
   }
   
   function fxScreen() {
      global $loSmarty;
      $loSmarty->assign('scBehavior', '0');
      $loSmarty->assign('saIdenti', $_SESSION['paIdenti']);
      $loSmarty->display('Plantillas/Caj1010.tpl');
   }
   
   function fxScreen1() {
      global $loSmarty;
      $loSmarty->assign('scNombre', $_SESSION['paIdenti']['CNOMPER']);
      $loSmarty->assign('scNroDni', $_SESSION['paIdenti']['CNRODNI']);
      $loSmarty->assign('sdFecReg', $_SESSION['paIdenti']['DFECREG']);
      $loSmarty->assign('scGlosa', $_SESSION['paIdenti']['CGLOSA']);
      $loSmarty->assign('snMonto', $_SESSION['paIdenti']['NMONTO']);
      $loSmarty->assign('scBehavior', '1');
      $loSmarty->display('Plantillas/Caj1010.tpl');
   }
   
   function fxGrabar(){
      $_SESSION['paData'] = array('CCODIFI' => $_REQUEST['pcCodIfi'], 'CNOMIFI' => strtoupper($_REQUEST['pcNomIfi']), 
                            'CESTADO' => $_REQUEST['pcEstado'], 'CCODUSU' => '9999');
      $lo = new CIFinanciera();
      $lo->paData = $_SESSION['paData'];
      $lo->plNuevo  = $_SESSION['plNuevo'];
      $llOk = $lo->omGrabarFinanciera();
      if (!$llOk) {
         fxScreen1();
         fxAlert($lo->pcError);
      } else {
         fxInit();
      }
   }
   
   function fxEditar() {
      $_SESSION['pcCodIfi'] = $_REQUEST['pcCodIfi'];
      $lo = new CIFinanciera();
      $lo->paData = array('CCODIFI' => $_REQUEST['pcCodIfi']);
      $llOk = $lo->omEditarFinanciera();
      if (!$llOk) {
         fxScreen();
         fxAlert($lo->pcError);
      } else {
         $lo->plNuevo  = $_SESSION['plNuevo'];
         $_SESSION['paData'] = $lo->paData;
         fxScreen2();
      }
   }
   function fxScreen2() {
      global $loSmarty;
      $laData = $_SESSION['paData'];
      $loSmarty->assign('scflag', 1);
      $loSmarty->assign('scCodIfi', $_SESSION['paData']['CCODIFI']);
      $loSmarty->assign('scNomIfi', $_SESSION['paData']['CNOMIFI']); 
      $loSmarty->assign('scEstado', $laData['CESTADO']);
      $loSmarty->assign('saEstado', $_SESSION['paEstado']);
      $loSmarty->assign('scBehavior', '1');
      $loSmarty->display('Plantillas/Caj1010.tpl');
   }
?>