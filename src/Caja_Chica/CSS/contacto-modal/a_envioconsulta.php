<?php 
//QUITO CARACTERES DE PRINCIPIO Y FINAL EN BLANCO
foreach($_POST as $Nombre=>$Valor)
	$_POST[$Nombre]=trim($Valor);

$CamposConTextoInformativo=array();
$CamposConTextoInformativo['NombreContacto']='Ingrese su nombre';
$CamposConTextoInformativo['EmailContacto']='Ingrese su email';
//$CamposConTextoInformativo['TelefonoContacto']='Ingrese su telefono';
$CamposConTextoInformativo['Comentario']='Ingrese su Comentario';

foreach($CamposConTextoInformativo as $Clave=>$Valor)
	if(@$_POST[$Clave]==$Valor or !@$_POST[$Clave]) die("error:::".$Valor);


$cuerpo="";
while (list ($clave, $val) = each ($_POST)) 
	{
	$cuerpo .=  "<b>". $clave . ":</b> " . $val . "<br>";
	} 

//$mail="su-correo@mail.com";
$mail=$_POST['EmailContacto'];

//MAIL PARA EL ADMINISTRADOR DEL SITIO
mail("$mail", "Nueva consulta desde su sitio", "<font face=verdana size=2>" .  nl2br($cuerpo) . "<br></font>",
	"From: {$_POST['NombreContacto']}<{$_POST['EmailContacto']}>\r\n" .
	"Content-type: text/html; charset=utf-8\r\n");

//MAIL PARA EL VISITANTE DEL SITIO
mail($_POST['EmailContacto'], "Consulta Recibida", "<font face=verdana size=2>Hemos recibido su consulta. Gracias por contactarse con nosotros.</font>",
	"From: NombreDeSuSitio<$mail>\r\n" .
	"Content-type: text/html; charset=utf-8\r\n");

die("ok:::Gracias por comunicarse con nosotros");
?>

