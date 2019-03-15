<?php
function conn() {
  $servername = "localhost";
  $username = "username";
  $password = "password";
  $dbname = "database";
  if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
  }
  return new mysqli($servername, $username, $password, $dbname);
}
?>
