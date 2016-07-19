      <table border=5 style="font-size:10px">
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
            {$j = 0}
            {foreach from = $saDatos item = i}
                  <tr>
                  <td><input type="text" name="paDatos[{$j}][0]" value="{$i['0']}" size="10" maxlength="12"/></td>
                  <td><input type="text" name="paDatos[{$j}][1]" value="{$i['1']}" size="10" maxlength="12"/></td>
                  <td><select name="pcTipDoc" id= "pcTipDoc" style="width: 150px">
                        <option value="01">FACTURA</option>
                        <option value="02">RECIBO POR HONORARIOS</option>
                        <option value="03">BOLETA</option>
                        <option value="07">NOTA DE CREDITO</option>
                  </select></td>
                  <td><input type="text" name="paDatos[{$j}][3]" value="{$i['3']}" size="10" maxlength="12" placeholder="****-******"/></td>
                  <td><input type="date" name="paDatos[{$j}][4]" value="{$i['4']}" size="10" maxlength="12"/></td>
                  <td><textarea name="pcGlosa[{$j}][5]" value="{$i['5']}" rows='3' cols='10' style="width: 100px;text-transform:uppercase;text-align: left;" autofocus>Escribe la Descripcion </textarea></td>
                  <td><input type="text" name="paDatos[{$j}][6]" value="{$i['6']}" size="10" maxlength="12"/></td>
                  <td><input type="text" name="paDatos[{$j}][7]" value="{$i['7']}" size="10" maxlength="12" onblur="f_NumFormat(this,2)" placeholder="0.00"/></td>
                  <td><input type="text" name="paDatos[{$j}][8]" value="{$i['8']}" size="10" maxlength="12" onblur="f_NumFormat(this,2)" placeholder="0.00"/></td>
                  <td><input type="text" name="paDatos[{$j}][9]" value="{$i['9']}" size="10" maxlength="12" onblur="f_NumFormat(this,2)" placeholder="0.00"/></td>
                  <td><input type="text" name="paDatos[{$j}][10]" value="{$i['10']}" size="10" maxlength="12" onblur="f_NumFormat(this,2)" placeholder="0.00"/></td>
                  <td><select name="pcTipDoc" id= "pcTipDoc" style="width: 100px">
                        <option value="S">SOLES</option>
                        <option value="D">DOLARES</option>
                  </select></td>
                  <td align="center"><input type="radio" name="pcCheck" value="{$i[0]}"/></td>
                  </tr>
                  {$j = $j + 1}
            {/foreach}
      </table>