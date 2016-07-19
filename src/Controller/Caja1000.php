<?php
   // Registro y mantenimiento de empleados
   require_once 'Libs/Smarty.class.php';
   require_once 'Clases/CCChica.php';
   session_cache_limiter();
   session_start();
   $loSmarty = new Smarty;

   if (@$_POST['Boton1'] == 'Nuevo') {
      fxScreen1();
   } elseif (@$_POST['Boton1'] == 'Eliminar') {
      $_SESSION['plNuevo'] = false;
      fxEditar();
   } elseif (@$_POST['Boton2'] == 'Apertura') {
      fxApertura();
   } elseif (@$_POST['Boton2'] == 'Buscar') {
      fxBuscar();
   } elseif (@$_POST['Boton2'] == 'Salir') {
      header('Location: Mnu0000.php');
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
      $lo = new CCChica();
      $lo->paDatos = array ('CCODUSU' => $lcCodUsu, 'CNOMBRE' => $lcCodUsu);
      //$llOk = $lo->omInitCuenta();
      $llOk = true;
      if (!$llOk) {
         fxAlert($lo->pcError);
         header('Location: Mnu0000.php?Id=4000');
      } else {
         $_SESSION['paNomEnt']=$lo->paNomEnt;
         fxScreen();
      }
   }
   
   function fxScreen() {
      global $loSmarty;
      $loSmarty->assign('scBehavior', '0');
      $loSmarty->assign('scCodEnt', $_SESSION['paNomEnt'][0]);
      $loSmarty->assign('scNombre', $_SESSION['paNomEnt'][1]);
      $loSmarty->assign('scEntida', $_SESSION['paNomEnt'][2]);
      $loSmarty->assign('scCodEnt', $_SESSION['paNomEnt'][2]);
      $loSmarty->display('Plantillas/Caja1000.tpl');
   }

   function fxBuscar(){
      global $loSmarty;
      $lo = new CCChica();
      $lo->paData = array('CCODENT' => $_REQUEST['pcCodEnt']);
      $llOk = $lo->omBuscarEntidad();
      if (!$llOk){
         fxAlert($lo->pcError);
         fxInit();
      }
      $loSmarty->assign('scBehavior', '0');
      $loSmarty->assign('scNombre', $lo->paData['CNOMENT']);
      $loSmarty->assign('scNroDni', $lo->paData['CNRODNI']);
      $loSmarty->assign('scCodEnt', $lo->paData['CCODENT']);
      $loSmarty->display("Plantillas/Caja1000.tpl");
   } 
   
   function fxApertura(){
      $_SESSION['paData'] = array('CNRODNI' => $_REQUEST['pcNroDni'], 'CCODENT' => $_REQUEST['pcCodEnt'], 
                            'DFECHA' => $_REQUEST['pdFecha'],'CGLOSA' => $_REQUEST['pcGlosa'],
                            'CCODUSU' => 'EPIS');
      $lo = new CCChica();
      $lo->paData = $_SESSION['paData'];
      $llOk = $lo->omAbrirCaja();
      if (!$llOk) {
         echo('*****');
         fxAlert($lo->pcError);
         fxScreen();
      } else {
         fxAlert('LA APERTURA HA SIDO REALIZADA CORRECTAMENTE');
         header('Location: Mnu0000.php');
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
      $loSmarty->display('Plantillas/Caja1000.tpl');
   }
?>