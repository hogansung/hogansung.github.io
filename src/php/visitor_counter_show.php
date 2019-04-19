<?php
$link = mysqli_connect('localhost', 'root', 'PEZb3qxIpET8', 'website_info', '3306', '/opt/bitnami/mysql/tmp/mysql.sock');

$sql = 'select * from visitor_counters';
$res = mysqli_query($link, $sql);
$row = mysqli_fetch_assoc($res);
$num_visits = $row['num_visits'];
echo json_encode($num_visits);

mysqli_close($link);
?>
