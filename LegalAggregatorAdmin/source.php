<?php
$title = "Sources";
include_once("includes/common.php");
include_once("includes/header.php");
$data_editor_table = "source";
include_once("includes/data_editor.php");
?>

<script src="js/data_editor.js"></script>
<div style="margin-left: 10px;"><a href="javascript:void(0)" onclick="window.data_editor.add_row('#data_table')">Add New</a></div>
<table class="table" id='data_table'>
  <thead><tr><th></th><th>Source</th><th>Category</th><th>Status</th></tr></thead>
  <tbody>
    <tr style="display: none;" class='edit_template'>
      <td data-column='commands'></td>
      <td data-column='source'><input type='text' /></td>
      <td data-column='category'><input type='text' /></td>
      <td data-column='status'><input type='text' /></td>
    </tr>
    <tr style="display: none;" class='view_template'>
      <td data-column='commands'></td>
      <td data-column='source'></td>
      <td data-column='category'></td>
      <td data-column='status'></td>
    </tr>
  </tbody>
</table>

<?php
$conn = conn();
$result = $conn->query("select * from source");
$data = array();
while($record = $result->fetch_assoc())
  $data[] = $record;
print("<script>window.data_editor.init_table('#data_table', " . json_encode($data) . ");</script>");
$conn->close();

include_once("includes/footer.php");
?>

