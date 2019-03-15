<?php
$title = "Sources";
include_once("includes/common.php");
include_once("includes/header.php");
$data_editor_table = "job_posting";
include_once("includes/data_editor.php");
?>

<script src="js/data_editor.js"></script>
<div style="margin-left: 10px;">
  <a href="javascript:void(0)" onclick="window.data_editor.add_row('#data_table')">Add New</a>
  &nbsp;|&nbsp;
  <a href="javascript:void(0)" onclick="window.data_editor.truncate_table()">Delete All Rows</a>
</div>
<table class="table" id='data_table'>
  <thead><tr><th></th><th>Source</th><th>ID</th><th>Title</th><th>Link</th><th>Location</th><th>Posted</th><th>Inserted</th><th>Description</th></tr></thead>
  <tbody>
    <tr class='edit_template'>
      <td data-column='commands'></td>
      <td data-column='source'><input type='text' /></td>
      <td data-column='source_record_id'><input type='text' /></td>
      <td data-column='title'><input type='text' /></td>
      <td data-column='link'><input type='text' /></td>
      <td data-column='location'><input type='text' /></td>
      <td data-column='posted'><input type='text' /></td>
      <td data-column='inserted'><input type='text' /></td>
      <td data-column='description'><input type='text' /></td>
    </tr>
    <tr class='view_template'>
      <td data-column='commands'></td>
      <td data-column='source'></td>
      <td data-column='source_record_id'></td>
      <td data-column='title'></td>
      <td data-column='link'></td>
      <td data-column='location'></td>
      <td data-column='posted'></td>
      <td data-column='inserted'></td>
      <td data-column='description'></td>
    </tr>
  </tbody>
</table>

<?php
$conn = conn();
$result = $conn->query("select job_posting.*, source.source from job_posting inner join source on job_posting.source_id = source.id where source.source like '%mla%'");
print("<script>window.data_editor.init_table('#data_table', " . forgiving_json($result) . ");</script>");
$conn->close();

include_once("includes/footer.php");
?>

