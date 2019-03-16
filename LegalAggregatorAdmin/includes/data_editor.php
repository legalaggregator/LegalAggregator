<?php
if ($data_editor_table == "") die("Variable 'data_editor_table' must be set.");
if ($_POST["data_editor_cmd"] == "delete") {
  $conn = conn();
  $conn->query("delete from $data_editor_table where id = " . $_POST["data_editor_cmd_id"]) or die($conn->error);
  $conn->close();
}
if ($_POST["data_editor_cmd"] == "truncate") {
  print("
  <script>
    $(document).ready(function() { 
	  if (confirm('Last chance. Are you sure you wish to truncate table [$data_editor_table]?')) { 
		$('#data_editor_cmd').val('truncate_confirmed'); 
		$('#data_editor_cmd').closest('form').submit(); 
	  }
	});
  </script>");
}
if ($_POST["data_editor_cmd"] == "truncate_confirmed") {
  $conn = conn();
  $conn->query("truncate table $data_editor_table") or die($conn->error . "<br />" . $query);
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
      $query .= "'" + $conn->escape_string($value) + "', ";
    $query = trim($query, " ,") . ")";
    $conn->query($query) or die($conn->error . "<br />" . $query);
    $conn->close();
  } else {
    $query = "update $data_editor_table set ";
    $data = json_decode($_POST["data_editor_cmd_data"]);
    foreach($data as $key => $value)
      $query .= " $key = '" . $conn->escape_string($value) . "', ";
    $query = trim($query, " ,") . " where id = " . $_POST["data_editor_cmd_id"];
    $conn->query($query) or die($conn->error . "<br />" . $query);
    $conn->close();
  }
}
function forgiving_json($result) {
  $data = array();
  while($row = $result->fetch_assoc()) {
    foreach($row as &$value)
      $value = mb_convert_encoding($value, "UTF-8", "Windows-1252");
    unset($value); # safety: remove reference
    $data[] = array_map('utf8_encode', $row );
  }
  return json_encode($data);
}
?>

<style type="text/css">
table tr.view_template, table tr.edit_template {
	display: none;
}
</style>
<form method="post" action="">
  <input type="hidden" name="data_editor_cmd" id="data_editor_cmd" value="" />
  <input type="hidden" name="data_editor_cmd_id" id="data_editor_cmd_id" value="" />
  <input type="hidden" name="data_editor_cmd_data" id="data_editor_cmd_data" value="" />
</form>
