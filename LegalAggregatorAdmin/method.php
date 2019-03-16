<?php
$title = "Methods";
include_once("includes/common.php");
include_once("includes/header.php");
$data_editor_table = "method";
include_once("includes/data_editor.php");
?>

<script src="js/data_editor.js"></script>
<div style="margin-left: 10px;"><a href="javascript:void(0)" onclick="window.data_editor.add_row('#data_table')">Add New</a></div>
<table class="table" id='data_table'>
  <thead><tr><th></th><th>Method</th></tr></thead>
  <tbody>
    <tr style="display: none;" class='edit_template'>
      <td data-column='commands'></td>
      <td data-column='method'><input type='text' /></td>
    </tr>
    <tr style="display: none;" class='view_template'>
      <td data-column='commands'></td>
      <td data-column='method'></td>
    </tr>
  </tbody>
</table>

<?php
$conn = conn();
$result = $conn->query("select * from method");
print("<script>window.data_editor.init_table('#data_table', " . forgiving_json($result) . ");</script>");
$conn->close();

include_once("includes/footer.php");
?>

