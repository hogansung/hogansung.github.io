<?php
$link = mysqli_connect('localhost', 'root', 'PEZb3qxIpET8', 'website_info', '3306', '/opt/bitnami/mysql/tmp/mysql.sock');

$sql = 'update visitor_counters set num_visits = num_visits + 1 where id = 1;';
$res = mysqli_query($link, $sql);

$sql = 'select * from visitor_counters';
$res = mysqli_query($link, $sql);
$row = mysqli_fetch_assoc($res);
$num_visits = $row['num_visits'];
echo json_encode($num_visits);

mysqli_close($link);
?>
