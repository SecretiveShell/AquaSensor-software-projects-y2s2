<?php
session_start();
$url_template='https://api.aquasensor.co.uk/aq.php?op=readings&username='.$_SESSION["username"].'&token='.$_SESSION["token"].'&sensorid=';
$date_append='&fromdate={from}&todate={to}';
$url=$url_template.$_GET["sensor"];
if(isset($_GET["date"])){
	$date_append=str_replace("{from}",$_GET["date"],$date_append);
	$date_append=str_replace("{to}",$_GET["date"],$date_append);
	$url=$url.$date_append;
}elseif(isset($_GET["from"])&&isset($_GET["to"])){
	$date_append=str_replace("{from}",$_GET["from"],$date_append);
	$date_append=str_replace("{to}",$_GET["to"],$date_append);
	$url=$url.$date_append;
}
$curl_handle = curl_init();
curl_setopt( $curl_handle, CURLOPT_URL, $url);
curl_setopt( $curl_handle, CURLOPT_RETURNTRANSFER, true );
$html = curl_exec( $curl_handle );
curl_close( $curl_handle );
$html=substr($html,35);
$row=0;
$token=",\n";
header('Content-Type: application/json; charset=utf-8');
$t=strtok($html,$token);
if($t===false){
	$dt=-1;
	$temp=-1;
	$diox=-1;
	$perc=-1;
}else{
while($t!==false){
	$dt[$row]=$t.' '.strtok($token);
	$temp[$row]=strtok($token);
	$diox[$row]=strtok($token);
	$perc[$row]=strtok($token);
	$t=strtok($token);;
	$row=1+$row;
}}
if($row>125){
	$dt=-1;
	$time=-1;
	$temp=-1;
	$diox=-1;
	$perc=-1;
}
$out=array('dt'=>$dt,'temp'=>$temp,'diox'=>$diox,'perc'=>$perc);
$out=json_encode($out);
echo $out;
?>