window.data_editor = {}
window.data_editor.init_table = function(table, data) {
  var $table = $(table);
  $table.prop("data_editor_data", data);
  $template = $table.find(".view_template");
  for(let row of data) {
    $tr = $template.clone().removeClass("view_template").addClass("record");
    for(let cell of $tr.find("td")) {
      var $cell = $(cell);
      var $inner = $cell.find("*");
      if ($inner.length != 0) 
        $inner.text(row[$cell.attr("data-column")]);
      else
        $cell.text(row[$cell.attr("data-column")]);
    }
    $tr.find("td[data-column='commands']").append("<a href='javascript:void(0);' onclick='window.data_editor.edit_row(this);'>Edit</a> | <a href='javascript:void(0);' onclick='window.data_editor.delete_row(this);'>Delete</a>");
    $tr.show().attr("data-id", row["id"]).appendTo($table);
  }
}
window.data_editor.delete_row = function(sender) {
  if (confirm("Are you sure you wish to delete this row?")) {
    $tr = $(sender).closest("tr.record");
    id = $tr.attr("data-id");
    $("#data_editor_cmd").val("delete");
    $("#data_editor_cmd_id").val(id);
    $("#data_editor_cmd").closest("form").submit();
  }
}
window.data_editor.save_row = function(sender) {
  $tr = $(sender).closest("tr.record");
  id = $tr.attr("data-id");
  $("#data_editor_cmd").val("update");
  $("#data_editor_cmd_id").val(id);
  data = {};
  for(let cell of $tr.find("td[data-column]")) {
    var $cell = $(cell);
    var $input = $cell.find(":input");
    if ($input.length != 0) {
      var column = $cell.attr("data-column");
      data[column] = $input.val();
    }
  }
  $("#data_editor_cmd_data").val(JSON.stringify(data));
  $("#data_editor_cmd").closest("form").submit();
}
window.data_editor.cancel_edit_row = function(sender) {
  $tr = $(sender).closest("tr.record");
  id = $tr.attr("data-id");
  if (id) $tr.closest("table").find("tr[data-id='" + id + "']").show();
  $tr.remove();
}
window.data_editor.add_row = function(table) {
  $table = $(table);
  $new_tr = $table.find(".edit_template").clone().removeClass("edit_template").addClass("record").show().appendTo($table);
  $new_tr.find("td[data-column='commands']").append("<a href='javascript:void(0);' onclick='window.data_editor.save_row(this);'>Save</a> | <a href='javascript:void(0);' onclick='window.data_editor.cancel_edit_row(this);'>Cancel</a>");
  $new_tr.find(":input:first").focus();
}
window.data_editor.edit_row = function(sender) {
  $tr = $(sender).closest("tr.record");
  id = $tr.attr("data-id");
  row = null;
  for(var x of $tr.closest("table").prop("data_editor_data"))
    if (x["id"] == id) row = x;
  if (row == null) {
    alert("Cannot find the row with ID " + id);
    return;
  }
  $tr.hide();
  $new_tr = $tr.closest("table").find(".edit_template").clone().removeClass("edit_template").addClass("record").show().attr("data-id", row["id"]).insertAfter($tr);
  for(let cell of $new_tr.find("td")) {
    var $cell = $(cell);
    var $input = $cell.find(":input");
    if ($input.length != 0) {
      var value = row[$cell.attr("data-column")];
      $input.val(value);
    }
  }
  $new_tr.find("td[data-column='commands']").append("<a href='javascript:void(0);' onclick='window.data_editor.save_row(this);'>Save</a> | <a href='javascript:void(0);' onclick='window.data_editor.cancel_edit_row(this);'>Cancel</a>");
}
