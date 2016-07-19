<?php
   // Registro y mantenimiento de empleados
   require_once 'Libs/Smarty.class.php';
   require_once 'Clases/CContabilidad.php';
   session_cache_limiter();
   session_start();
   $loSmarty = new Smarty;
   if (@$_POST['Boton1'] == 'Editar') {
      fxScreen1();
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
      //$lo = new CRCuentas();
      //$llOk = $lo->omInitCuentas();
      if (0) {
         fxAlert($lo->pcError);
         header('Location: Mnu0000.php?Id=4000');
      } else {
         //$_SESSION['paNomIfi']=$lo->paNomIfi;
         //$_SESSION['paEstado']=$lo->paEstado;
         fxScreen();
      }
   }
   
   function fxScreen() {
      global $loSmarty;
      $loSmarty->assign('scBehavior', '0');
      //$loSmarty->assign('saNomIfi', $_SESSION['paNomIfi']);
      $loSmarty->display('Plantillas/Caj1010.tpl');
   }
   
   function fxScreen1() {
      global $loSmarty;
      $loSmarty->assign('scflag', 0);
      $loSmarty->assign('scEstado', '');
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