<?php
if ($data_editor_table == "") die("Variable 'data_editor_table' must be set.");
if ($_POST["data_editor_cmd"] == "delete") {
  $conn = conn();
  $conn->query("delete from $data_editor_table where id = " . $_POST["data_editor_cmd_id"]) or die($conn->error);
  $conn->close();
}
if ($_POST["data_editor_cmd"] == "update") {
  $conn = conn();
  if ($_POST["data_editor_cmd_id"] == "") {
    $query = "insert into $data_editor_table (";
    $data = json_decode($_POST["data_editor_cmd_data"]);
    foreach($data as $key => $value)
      $query .= "$key, ";
    $query = trim($query, " ,") . ") values (";
    foreach($data as $key => $value)
      $query .= "'$value', ";
    $query = trim($query, " ,") . ")";
    $conn->query($query) or die($conn->error . "<br />" . $query);
    $conn->close();
  } else {
    $query = "update $data_editor_table set ";
    $data = json_decode($_POST["data_editor_cmd_data"]);
    foreach($data as $key => $value)
      $query .= " $key = '$value', ";
    $query = trim($query, " ,") . " where id = " . $_POST["data_editor_cmd_id"];
    $conn->query($query) or die($conn->error . "<br />" . $query);
    $conn->close();
  }
}
?>

<form method="post" action="">
  <input type="hidden" name="data_editor_cmd" id="data_editor_cmd" value="" />
  <input type="hidden" name="data_editor_cmd_id" id="data_editor_cmd_id" value="" />
  <input type="hidden" name="data_editor_cmd_data" id="data_editor_cmd_data" value="" />
</form>
