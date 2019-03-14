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
  <thead><tr><th></th><th>URL</th><th>Method</th><th>Source</th><th>Each Posting Path</th><th>Source Record ID Path</th><th>Posted Path</th><th>Link Path</th><th>Title Path</th><th>Description Path</th><th>Location Path</th></tr></thead>
  <tbody>
    <tr style="display: none;" class='edit_template'>
      <td data-column='commands'></td>
      <td data-column='url'><textarea style="width: 500px;"></textarea></td>
      <td data-column='method'>
        <select>
          <option value="Custom">Custom</option>
          <option value="JSON">JSON</option>
          <option value="Jobvite">Jobvite</option>
          <option value="Taleo">Taleo</option>
          <option value="viDesktop">viDesktop</option>
          <option value="Silkroad">Silkroad</option>
        </select
      </td>
      <td data-column='source_id'>
        <select>
        <?php
        $conn = conn();
        $result = $conn->query("select * from source");
        while($record = $result->fetch_assoc())
          printf("<option value='%s'>%s</option>", $record["id"], $record["source"]);
        $conn->close();
        ?>
        </select
      </td>
      <td data-column='each_posting_path'><input type='text' /></td>
      <td data-column='source_record_id_path'><input type='text' /></td>
      <td data-column='posted_path'><input type='text' /></td>
      <td data-column='link_path'><input type='text' /></td>
      <td data-column='title_path'><input type='text' /></td>
      <td data-column='description_path'><input type='text' /></td>
      <td data-column='location_path'><input type='text' /></td>
    </tr>
    <tr style="display: none; white-space: nowrap;" class='view_template'>
      <td data-column='commands'></td>
      <td data-column='url'><div style="width: 500px; white-space: nowrap; overflow: hidden;"></div></td>
      <td data-column='method'></td>
      <td data-column='source'></td>
      <td data-column='each_posting_path'></td>
      <td data-column='source_record_id_path'></td>
      <td data-column='posted_path'></td>
      <td data-column='link_path'></td>
      <td data-column='title_path'></td>
      <td data-column='description_path'></td>
      <td data-column='location_path'></td>
    </tr>
  </tbody>
</table>

<?php
$conn = conn();
$result = $conn->query("select job_posting_url.*, source.source from job_posting_url inner join source on job_posting_url.source_id = source.id order by source.source, job_posting_url.url");
$data = array();
while($record = $result->fetch_assoc())
  $data[] = $record;
print("<script>window.data_editor.init_table('#data_table', " . json_encode($data) . ");</script>");
$conn->close();

include_once("includes/footer.php");
?>

