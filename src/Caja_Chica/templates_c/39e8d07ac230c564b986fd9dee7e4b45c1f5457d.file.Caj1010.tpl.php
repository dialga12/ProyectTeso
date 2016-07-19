<?php /* Smarty version Smarty-3.1.8, created on 2016-02-20 23:01:57
         compiled from "Plantillas\Caj1010.tpl" */ ?>
<?php /*%%SmartyHeaderCode:219335671d542cffe59-68557881%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '39e8d07ac230c564b986fd9dee7e4b45c1f5457d' => 
    array (
      0 => 'Plantillas\\Caj1010.tpl',
      1 => 1456005495,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '219335671d542cffe59-68557881',
  'function' => 
  array (
  ),
  'version' => 'Smarty-3.1.8',
  'unifunc' => 'content_5671d542f39256_00265936',
  'variables' => 
  array (
    'scBehavior' => 0,
    'saIdenti' => 0,
    'i' => 0,
    'scNombre' => 0,
    'scNroDni' => 0,
    'sdFecReg' => 0,
    'scGlosa' => 0,
    'snMonto' => 0,
  ),
  'has_nocache_code' => false,
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_5671d542f39256_00265936')) {function content_5671d542f39256_00265936($_smarty_tpl) {?><!DOCTYPE html>
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

      function f_IniciarCampo() {
         var xmlhttp = new XMLHttpRequest();
         xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
               document.getElementById("divData").innerHTML = xmlhttp.responseText;
               var d = document.getElementById("wait1");
               d.innerHTML = '';
            } else {
               var d = document.getElementById("wait1");
               d.innerHTML = '<img src="CSS/Cargando.gif" height="12" width="25">';
            }
         }  
         xmlhttp.open("GET", "PAjax.php?Id=100", true);
         xmlhttp.send();
      }

      function f_NuevoCampo(form) {
         /*var str = document.getElementById("pcNroDni").value;
         if (str.length != 8 ){
             alert("Numero de DNI invalido");
             return;
         }*/
         //comprobar q no se repita
         //var str = document.getElementById("pcNroDni").value;
         var xmlhttp = new XMLHttpRequest();
         xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
               document.getElementById("divData").innerHTML = xmlhttp.responseText;
               var d = document.getElementById("wait1");
               d.innerHTML = '';
               //document.getElementById("pcNroDni").value='';
            } else {
               var d = document.getElementById("wait1");
               d.innerHTML = '<img src="CSS/Cargando.gif" height="12" width="25">';
            }
         }  
         xmlhttp.open("GET", "PAjax.php?Id=101", true);
         xmlhttp.send();
      }

      function f_EliminarCampo(form) {
         var i = getSelectedButton(form.pcCheck);
         var str=form.pcCheck[i].value;
         var xmlhttp = new XMLHttpRequest();
         xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
               document.getElementById("divData").innerHTML = xmlhttp.responseText;
               var d = document.getElementById("wait1");
               d.innerHTML = '';
            } else {
               var d = document.getElementById("wait1");
               d.innerHTML = '<img src="CSS/Cargando.gif" height="12" width="25">';
            }
         }  
         xmlhttp.open("GET", "PAjax.php?Id=102&nombre="+str, true);
         xmlhttp.send();
      }

   </script>
   <title>Rendicion de Cuentas</title>
</head>
<body onload="f_IniciarCampo()">
<form action="Caj1010.php#no-back" method="post">
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
      <div style="overflow:scroll;height:500px;width:800px;overflow:auto;border: 1px">
      <table border=5 style="font-size:10px">
         <th bgcolor="#F29818" width="200">Glosa</th>
         <th bgcolor="#F29818" width="50">Fecha Limite</th>
         <th bgcolor="#F29818" align="center"><img src="CSS/Check.jpg" width="25" height="25"></th>
         <?php  $_smarty_tpl->tpl_vars['i'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['i']->_loop = false;
 $_from = $_smarty_tpl->tpl_vars['saIdenti']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['i']->key => $_smarty_tpl->tpl_vars['i']->value){
$_smarty_tpl->tpl_vars['i']->_loop = true;
?>
            <tr>
            <td><?php echo $_smarty_tpl->tpl_vars['i']->value['1'];?>
</td>
            <td><?php echo $_smarty_tpl->tpl_vars['i']->value['2'];?>
</td>
            <td><input type="radio" name="pcIdenti" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['0'];?>
"/></td>
            </tr>
         <?php } ?>
      </table>
      </div>
      <table>
         <tr>
         <td><input type="submit" name="Boton1" value="Abrir" /></td>
         <td><input type="submit" name="Boton1" value="Salir" /></td>
         </tr>
      </table>
   <?php }elseif($_smarty_tpl->tpl_vars['scBehavior']->value=="1"){?>
      <div style="overflow:scroll;height:500px;width:1600px;overflow:auto;border: 1px">
     <table style="font-size:11px">
         <tr><td>Nombre: </td>
             <td><font color = "blue"><?php echo $_smarty_tpl->tpl_vars['scNombre']->value;?>
</font>
         </tr>
         <tr><td>DNI: </td>
             <td><font color = "blue"><?php echo $_smarty_tpl->tpl_vars['scNroDni']->value;?>
</font>
         </tr>
         <tr><td>Fecha de Apertura: </td>
             <td><font color = "blue"><?php echo $_smarty_tpl->tpl_vars['sdFecReg']->value;?>
</font>
         </tr>
         <tr><td>Glosa: </td>
             <td><font color = "blue"><?php echo $_smarty_tpl->tpl_vars['scGlosa']->value;?>
</font>
         </tr>
         <tr><td>Monto: </td>
             <td><font color = "blue"><?php echo $_smarty_tpl->tpl_vars['snMonto']->value;?>
</font>
         </tr>
         </table>
            <p><span id="divData"></span></p>
         <table>
      </table>
      </div>
      <table>
         <tr>
         <td><input type="button" class="boton" name="Boton1" value="Nuevo" onclick="f_NuevoCampo(this.form);"/></td>
         <td><input type="button" class="boton" name="Boton1" value="Eliminar" onclick="f_EliminarCampo(this.form);"/></td>
         <tr></tr>
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