<?php
include_once("barrister.php");

$barrister = new Barrister();
$client    = $barrister->httpClient("http://localhost:7667/lista");
$Lista      = $client->proxy("Lista");

print_r ($Lista->lista(7, 14));
print_r ($Lista->lista(8, 20));

echo "\nIDL metadata:\n";
$meta = $client->getMeta();
$keys = array("barrister_version", "checksum");
foreach ($keys as $i=>$key) {
  echo "$key=$meta[$key]\n";
}

?>
