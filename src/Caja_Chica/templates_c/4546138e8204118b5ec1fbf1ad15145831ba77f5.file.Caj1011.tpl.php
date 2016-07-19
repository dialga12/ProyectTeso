<?php /* Smarty version Smarty-3.1.8, created on 2016-02-20 21:52:01
         compiled from "Plantillas\Caj1011.tpl" */ ?>
<?php /*%%SmartyHeaderCode:286165698796dc38bd9-58751764%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '4546138e8204118b5ec1fbf1ad15145831ba77f5' => 
    array (
      0 => 'Plantillas\\Caj1011.tpl',
      1 => 1456001493,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '286165698796dc38bd9-58751764',
  'function' => 
  array (
  ),
  'version' => 'Smarty-3.1.8',
  'unifunc' => 'content_5698796dc928c7_86370809',
  'variables' => 
  array (
    'saDatos' => 0,
    'j' => 0,
    'i' => 0,
  ),
  'has_nocache_code' => false,
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_5698796dc928c7_86370809')) {function content_5698796dc928c7_86370809($_smarty_tpl) {?>      <table border=5 style="font-size:10px">
            <th bgcolor="#F29818" width="100">RUC</th>
            <th bgcolor="#F29818" width="100">Razon Social</th>
            <th bgcolor="#F29818" width="100">Tipo de Documento</th>
            <th bgcolor="#F29818" width="100">Factura</th>
            <th bgcolor="#F29818" width="100">Fecha</th>
            <th bgcolor="#F29818" width="100">Descripcion</th>
            <th bgcolor="#F29818" width="100">Tipo de Gasto</th>
            <th bgcolor="#F29818" width="100">Imponible</th>
            <th bgcolor="#F29818" width="100">IGV</th>
            <th bgcolor="#F29818" width="100">Renta</th>
            <th bgcolor="#F29818" width="100">No Gravado</th>
            <th bgcolor="#F29818" width="100">Moneda</th>
            <th bgcolor="#F29818" align="center"><img src="CSS/Check.jpg" width="25" height="25"></th>
            <?php $_smarty_tpl->tpl_vars['j'] = new Smarty_variable(0, null, 0);?>
            <?php  $_smarty_tpl->tpl_vars['i'] = new Smarty_Variable; $_smarty_tpl->tpl_vars['i']->_loop = false;
 $_from = $_smarty_tpl->tpl_vars['saDatos']->value; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array');}
foreach ($_from as $_smarty_tpl->tpl_vars['i']->key => $_smarty_tpl->tpl_vars['i']->value){
$_smarty_tpl->tpl_vars['i']->_loop = true;
?>
                  <tr>
                  <td><input type="text" name="paDatos[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][0]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['0'];?>
" size="10" maxlength="12"/></td>
                  <td><input type="text" name="paDatos[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][1]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['1'];?>
" size="10" maxlength="12"/></td>
                  <td><select name="pcTipDoc" id= "pcTipDoc" style="width: 150px">
                        <option value="01">FACTURA</option>
                        <option value="02">RECIBO POR HONORARIOS</option>
                        <option value="03">BOLETA</option>
                        <option value="07">NOTA DE CREDITO</option>
                  </select></td>
                  <td><input type="text" name="paDatos[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][3]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['3'];?>
" size="10" maxlength="12" placeholder="****-******"/></td>
                  <td><input type="date" name="paDatos[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][4]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['4'];?>
" size="10" maxlength="12"/></td>
                  <td><textarea name="pcGlosa[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][5]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['5'];?>
" rows='3' cols='10' style="width: 100px;text-transform:uppercase;text-align: left;" autofocus>Escribe la Descripcion </textarea></td>
                  <td><input type="text" name="paDatos[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][6]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['6'];?>
" size="10" maxlength="12"/></td>
                  <td><input type="text" name="paDatos[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][7]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['7'];?>
" size="10" maxlength="12" onblur="f_NumFormat(this,2)" placeholder="0.00"/></td>
                  <td><input type="text" name="paDatos[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][8]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['8'];?>
" size="10" maxlength="12" onblur="f_NumFormat(this,2)" placeholder="0.00"/></td>
                  <td><input type="text" name="paDatos[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][9]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['9'];?>
" size="10" maxlength="12" onblur="f_NumFormat(this,2)" placeholder="0.00"/></td>
                  <td><input type="text" name="paDatos[<?php echo $_smarty_tpl->tpl_vars['j']->value;?>
][10]" value="<?php echo $_smarty_tpl->tpl_vars['i']->value['10'];?>
" size="10" maxlength="12" onblur="f_NumFormat(this,2)" placeholder="0.00"/></td>
                  <td><select name="pcTipDoc" id= "pcTipDoc" style="width: 100px">
                        <option value="S">SOLES</option>
                        <option value="D">DOLARES</option>
                  </select></td>
                  <td align="center"><input type="radio" name="pcCheck" value="<?php echo $_smarty_tpl->tpl_vars['i']->value[0];?>
"/></td>
                  </tr>
                  <?php $_smarty_tpl->tpl_vars['j'] = new Smarty_variable($_smarty_tpl->tpl_vars['j']->value+1, null, 0);?>
            <?php } ?>
      </table><?php }} ?>