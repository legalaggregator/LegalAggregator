<?php
$title = "Job Posting URLs";
include_once("includes/common.php");
include_once("includes/header.php");
$data_editor_table = "job_posting_url";
include_once("includes/data_editor.php");
?>

<script src="js/data_editor.js"></script>
<div style="margin-left: 10px;"><a href="javascript:void(0)" onclick="window.data_editor.add_row('#data_table')">Add New</a></div>
<table class="table data_table" id='data_table'>
  <thead><tr><th></th><th>URL</th><th>Method</th><th>Source</th></tr></thead>
  <tbody>
    <tr style="display: none;" class='edit_template'>
      <td colspan="4">
        <table class="table">
          <tr><td colspan="2" data-column='commands'></td></tr>
          <tr><td>URL: </td><td data-column='url'><textarea style="width: 100%; height: 100px;"></textarea></td></tr>
          <tr><td>Method: </td><td data-column='method'>
            <select style='width: 100%;'>
              <option value="Custom">Custom</option>
              <option value="JSON">JSON</option>
              <option value="Jobvite">Jobvite</option>
              <option value="Taleo">Taleo</option>
              <option value="viDesktop">viDesktop</option>
              <option value="Silkroad">Silkroad</option>
            </select>
          </td></tr>
          <tr><td>Source: </td><td data-column='source_id'>
            <select style='width: 100%;'>
            <?php
            $conn = conn();
            $result = $conn->query("select * from source");
            while($record = $result->fetch_assoc())
              printf("<option value='%s'>%s</option>", $record["id"], $record["source"]);
            $conn->close();
            ?>
            </select
          </td></tr>
          <tr><td>Each Posting Path: </td><td data-column='each_posting_path'><input type='text' style='width: 100%;' /></td></tr>
          <tr><td>Source Record ID Path: </td><td data-column='source_record_id_path'><input type='text' style='width: 100%;' /></td></tr>
          <tr><td>Posted Path: </td><td data-column='posted_path'><input type='text' style='width: 100%;' /></td></tr>
          <tr><td>Link Path: </td><td data-column='link_path'><input type='text' style='width: 100%;' /></td></tr>
          <tr><td>Title Path: </td><td data-column='title_path'><input type='text' style='width: 100%;' /></td></tr>
          <tr><td>Description Path:</td><td data-column='description_path'><input type='text' style='width: 100%;' /></td></tr>
          <tr><td>Location Path: </td><td data-column='location_path'><input type='text' style='width: 100%;' /></td></tr>
          <tr><td colspan="2" data-column='commands'></td></tr>
        </table>
      </td>
    </tr>
    <tr style="display: none; white-space: nowrap;" class='view_template'>
      <td data-column='commands'></td>
      <td data-column='url'><div style="width: 500px; white-space: nowrap; overflow: hidden;"></div></td>
      <td data-column='method'></td>
      <td data-column='source'></td>
    </tr>
  </tbody>
</table>

<?php
$conn = conn();
$result = $conn->query("select job_posting_url.*, source.source from job_posting_url inner join source on job_posting_url.source_id = source.id order by source.source, job_posting_url.url");
print("<script>window.data_editor.init_table('#data_table', " . forgiving_json($result) . ");</script>");
$conn->close();

include_once("includes/footer.php");
?>

