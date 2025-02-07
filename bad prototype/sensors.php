<?php
session_start();
$curl_handle = curl_init();
curl_setopt( $curl_handle, CURLOPT_URL, 'https://api.aquasensor.co.uk/aq.php?op=status&username='.$_SESSION['username'].'&token='.$_SESSION['token']);
curl_setopt( $curl_handle, CURLOPT_RETURNTRANSFER, true );
$html = curl_exec( $curl_handle );
curl_close( $curl_handle );
$t=explode('</tr><tr><td>',$html);
$r=1;
while($r<sizeof($t)){
	$t[$r]=explode('</td><td>',$t[$r]);
	$out[$r-1]['id']=$t[$r][0];
	$out[$r-1]['name']=$t[$r][1];
	$r=1+$r;
}
$out=json_encode($out);
header('Content-Type: application/json; charset=utf-8');
echo $out;
?>