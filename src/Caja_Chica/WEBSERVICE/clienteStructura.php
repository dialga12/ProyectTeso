<?php
include_once("barrister.php");

$barrister = new Barrister();
$client    = $barrister->httpClient("http://localhost:7667/william");
$Calculator      = $client->proxy("Calculator");
$array = array(
    "clase" => "ok",
    "metodo" => "restar",
    "codusuarios" => array("foo", "bar", "hallo", "world")
);

print_r ($Calculator->add($array));

echo "\nIDL metadata:\n";
$meta = $client->getMeta();
$keys = array("barrister_version", "checksum");
foreach ($keys as $i=>$key) {
  echo "$key=$meta[$key]\n";
}

?>
