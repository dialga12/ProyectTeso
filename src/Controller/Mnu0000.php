<?php
   require_once 'Libs/Smarty.class.php';
   require_once 'Clases/CLogin.php';
   session_start();
   $loSmarty = new Smarty;
   if (!isset($_REQUEST['pcCodigo']) || !isset($_REQUEST['pcClave'])) {
      if (!fxInitSession()) {
         fxCallIndex('NO HA INICIADO SESION');
      } else {
         $loSmarty->assign('scNombre', $_SESSION['gcNombre']);         
         $loSmarty->assign('scCodigo', $_SESSION['gcCodUsu']);
         $loSmarty->display('Plantillas/Mnu0000.tpl');
      }
   } else {
      // Login
      $lo = new CLogin();
      $lo->paData = array('CCODIGO' => $_REQUEST['pcCodigo'], 'CCLAVE' => $_REQUEST['pcClave']);
      $llOk = $lo->omLogin();
      if (!$llOk) { // Error
         fxCallIndex($lo->pcError);
      } else {
         $_SESSION['gcCodUsu'] = $lo->paData['CCODUSU'];
         $_SESSION['gcNombre'] = $lo->paData['CNOMBRE']; 
         $_SESSION['gcCodOfi'] = $lo->paData['CCODOFI']; 
         if ($lo->pnCambio == 1){
            $loSmarty->assign('scNombre', $lo->pcNombre);
            $loSmarty->display('Plantillas/Mnu1000.tpl');
         } else {
            $loSmarty->assign('scNivel', '2000');
            $loSmarty->assign('scCodigo', $_SESSION['gcCodUsu']);
            $loSmarty->assign('scNombre', $_SESSION['gcNombre']);
            $loSmarty->display('Plantillas/Mnu0000.tpl');
         }
      } 
   }
?>
