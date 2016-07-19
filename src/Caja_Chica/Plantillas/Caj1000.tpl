<!DOCTYPE html>
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
<body onload="f_Init({$scBehavior})">
<form action="Caj1000.php#no-back" method="post">
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
   {if $scBehavior eq "0"}
      <table style="font-size:11px">
         <tr><td>DNI: </td>
             <td>
              <!-- adasds -->
             <!--<input type="text" id ="pcNroDni" name="pcNroDni" value="{$scNroDni}" onKeyPress="return NumbersOnly(event);"  maxlength="8">-->
             <input type="text" id ="pcNroDni" name="pcNroDni" value="{$scNroDni}" maxlength="8">
            </td>
            <td><input type="submit" name="Boton2" value="Buscar"/></td>
         </tr>
         <tr><td>NOMBRE: </td>
             <td><font color = "blue">{$scNombre}</font>
             <input type="hidden" name="pcNombre" value="{$scNombre}" >
            </td>
         </tr>
         <tr><td>FECHA: </td>
             <td>
             <input  type="date" name="pdFecha" value="{$sdFecha}">
             </td>
         </tr>
         <tr><td>ENTIDAD: </td>
             <td><font color = "blue">{$scEntida}</font>
             <input type="hidden" name="pcEntida" value="{$scEntida}" >
             <input type="hidden" name="pcCodEnt" value="{$scCodEnt}" >
            </td>
         </tr> 
         <tr><td>GLOSARIO: </td>
         <td><textarea name="pcGlosa" id="pcGlosa" value="{$scGlosa}" rows='10' cols='40' style="width: 300px;text-transform:uppercase;text-align: left;" autofocus>Escribe la Descripcion </textarea></td>
         </tr><tr> 
         <tr><td>MONTO: </td>
         <td><input type="text" id ="pcMonto" name="pcMonto" onblur="f_NumFormat(this,2)" placeholder="0.00"></td>
         </tr><tr>      
      </table>
      <table>
         <tr>
         <td></td>
         <td><input type="submit" name="Boton2" value="Apertura"/></td>
         <td><input type="submit" name="Boton2" value="Salir" /></td>
         </tr>
      </table>
   {elseif $scBehavior eq "1"}
      <div style="overflow:scroll;height:500px;width:800px;overflow:auto;border: 1px">
      <table border=5 style="font-size:10px">
         <th bgcolor="#F29818" width="200">Proveedor</th>
         <th bgcolor="#F29818" width="50">Factura</th>
         <th bgcolor="#F29818" width="50">Glosa</th>
         <th bgcolor="#F29818" width="50">Monto</th>
         <th bgcolor="#F29818" align="center"><img src="CSS/Check.jpg" width="25" height="25"></th>
         {foreach from = null item = i}
            <tr>
            <td>{$i['1']}</td>
            <td>{$i['2']}</td>
            <td>{$i['3']}</td>
            <td>{$i['4']}</td>
            <td><input type="radio" name="pcCodIfi" value="{$i['0']}"/></td>
            </tr>
         {/foreach}
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
   {/if}
   </div>
   </div>
   <div id="content"></div>
   <div id="footer"></div>
   </div>
</form>
</body>
</html>
