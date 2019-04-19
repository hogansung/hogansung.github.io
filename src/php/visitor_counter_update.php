<?php
$link = mysqli_connect('localhost', 'root', 'PEZb3qxIpET8', 'website_info', '3306', '/opt/bitnami/mysql/tmp/mysql.sock');

$sql = 'update visitor_counters set num_visits = num_visits + 1 where id = 1;';
$res = mysqli_query($link, $sql);

mysqli_close($link);
?>
