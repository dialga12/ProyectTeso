<?php /* Smarty version Smarty-3.1.8, created on 2016-02-22 14:08:05
         compiled from "Plantillas\Caja1000.tpl" */ ?>
<?php /*%%SmartyHeaderCode:894956cb051547f0c8-42441976%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    'bbad08e627500a79691371cf2dfbf9d4ba6c76fa' => 
    array (
      0 => 'Plantillas\\Caja1000.tpl',
      1 => 1456146465,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '894956cb051547f0c8-42441976',
  'function' => 
  array (
  ),
  'version' => 'Smarty-3.1.8',
  'unifunc' => 'content_56cb0515551236_55845770',
  'variables' => 
  array (
    'scBehavior' => 0,
    'scCodEnt' => 0,
    'scNombre' => 0,
    'scEntida' => 0,
    'scNroDni' => 0,
    'sdFecha' => 0,
    'scGlosa' => 0,
    'i' => 0,
  ),
  'has_nocache_code' => false,
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_56cb0515551236_55845770')) {function content_56cb0515551236_55845770($_smarty_tpl) {?><!DOCTYPE html>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
<html>
<head>
   <link rel="stylesheet" href="CSS/jquery-ui-1.11.0/jquery-ui.css">
   <script type="text/javascript" src="CSS/jquery-1.10.2.min.js"></script> 
   <script type="text/javascript" src="CSS/jquery-ui-1.11.0/jquery-ui.js"></script>
   <script type="text/javascript" src="CSS/jquery.validate.js"></script>
   <script type="text/javascript" src="CSS/jquery.numeric.js"></script>
   <script type="text/javascript" src="CSS/Libgen.js"></script>
   <link href="CSS/Sixavi.css" media="screen" rel="stylesheet" type="text/css" />
   <title>Rendicion de Cuentas</title>
      <script>

      function f_NumFormat(e, d) {
         e.value = Number(e.value).toFixed(d);
         if (e.value == 'NaN') {
            e.value = Number(0).toFixed(d);
            alert('ERROR EN VALOR NUMERICO')
         }
         return;
      }
    
      function getSelectedButton(buttonGroup){
         for (var i = 0; i < buttonGroup.length; i++) {
            if (buttonGroup[i].checked) {
               return i;
            }
         }
         return 0;
      }

      function NumbersOnly(e)
        {
          var keynum = window.event ? window.event.keyCode : e.which;
          if ((keynum == 8) || (keynum == 46))
          return true;
           
          return /\d/.test(String.fromCharCode(keynum));
        }
      
   </script>
</head>
<body onload="f_Init(<?php echo $_smarty_tpl->tpl_vars['scBehavior']->value;?>
)">
<form action="Caja1000.php#no-back" method="post">
   <div class="wrapper">
   <div id="MH">
      <ul>
      <li style="margin-left: 50px;"><h1>Rendicion de Cuentas</h1></li>
      <li style="float:right;margin-right: 100px;"><a onclick="self.location='index.php'">Cerrar Sesión</a></li>
      </ul>
   </div>
   <div id="topnavbar"></div>
   <div id="navigation">
   <div id="navcontainer">
   <?php if ($_smarty_tpl->tpl_vars['scBehavior']->value=="0"){?>
      <table style="font-size:11px">
         <tr><td>CODIGO ENTIDAD: </td>
             <td>
             <input type="text" id ="pcCodEnt" name="pcCodEnt" value="<?php echo $_smarty_tpl->tpl_vars['scCodEnt']->value;?>
" maxlength="8">
            </td>
            <td><input type="submit" name="Boton2" value="Buscar"/></td>
         </tr>
         <tr><td>NOMBRE: </td>
             <td><font color = "blue"><?php echo $_smarty_tpl->tpl_vars['scNombre']->value;?>
</font>
             <input type="hidden" name="pcNombre" value="<?php echo $_smarty_tpl->tpl_vars['scNombre']->value;?>
" >
             <input type="hidden" name="pcEntida" value="<?php echo $_smarty_tpl->tpl_vars['scEntida']->value;?>
" >
             <input type="hidden" name="pcNroDni" value="<?php echo $_smarty_tpl->tpl_vars['scNroDni']->value;?>
" >
            </td>
         </tr>
         <tr><td>FECHA: </td>
             <td>
             <input  type="date" name="pdFecha" value="<?php echo $_smarty_tpl->tpl_vars['sdFecha']->value;?>
">
             </td>
         </tr>
         <tr><td>GLOSARIO: </td>
         <td><textarea name="pcGlosa" id="pcGlosa" value="<?php echo $_smarty_tpl->tpl_vars['scGlosa']->value;?>
" rows='10' cols='40' style="width: 300px;text-transform:uppercase;text-align: left;" autofocus>Escribe la Descripcion </textarea></td>
         </tr><tr>  
      </table>
      <table>
         <tr>
         <td></td>
         <td><input type="submit" name="Boton2" value="Apertura"/></td>
         <td><input type="submit" name="Boton2" value="Salir" /></td>
         </tr>
      </table>
   <?php }elseif($_smarty_tpl->tpl_vars['scBehavior']->value=="1"){?>
      <div style="overflow:scroll;height:500px;width:800px;overflow:auto;border: 1px">
      <table border=5 style="font-size:10px">
         <th bgcolor="#F29818" width="200">Proveedor</th>
         <th bgcolor="#F29818" width="50">Factura</th>
         <th bgcolor="#F29818" width="50">Glosa</th>
         <th bgcolor="#F29818" width="50">Monto</th>
         <th bgcolor="#F29818" align="center"><img src="CSS/Check.jpg" width="25" height="25"></th>
         <?php  $_smarty_tpl->tpl_vars['i'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['i']->_loop = false;
 $_from = null; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['i']->key => $_smarty_tpl->tpl_vars['i']->value){
$_smarty_tpl->tpl_vars['i']->_loop = true;
?>
            <tr>
            <td><?php echo $_smarty_tpl->tpl_vars['i']->value['1'];?>
</td>
            <td><?php echo $_smarty_tpl->tpl_vars['i']->value['2'];?>
</td>
            <td><?php echo $_smarty_tpl->tpl_vars['i']->value['3'];?>
</td>
            <td><?php echo $_smarty_tpl->tpl_vars['i']->value['4'];?>
</td>
            <td><input type="radio" name="pcCodIfi" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['0'];?>
"/></td>
            </tr>
         <?php } ?>
      </table>
      </div>
      <table>
         <tr>
         <td><input type="submit" name="Boton1" value="Nuevo" /></td>
         <td><input type="submit" name="Boton1" value="Eliminar" /></td>
         <td><input type="submit" name="Boton1" value="Grabar" /></td>
         <td><input type="submit" name="Boton1" value="Salir" /></td>
         </tr>
      </table>
   <?php }?>
   </div>
   </div>
   <div id="content"></div>
   <div id="footer"></div>
   </div>
</form>
</body>
</html>
<?php }} ?>