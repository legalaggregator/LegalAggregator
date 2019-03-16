<?php
include_once("includes/header.php");
include_once("includes/common.php");
if (isset($_POST["submit"])) {
  mail("legalaggregator@outlook.com", "Website Inquiry", "Name: " . $_POST["your_name"] . "\r\n" . "Email: " . $_POST["your_email"] . "\r\n" . "Message:\r\n" . $_POST["your_message"] . "\r\n-------------------\r\n\r\n");
  print("<div class='alert alert-primary' role='alert'>Your message has been submitted successfully.</div>");
}
?>

<form method="post" action="">
<div class="form-group">
  <label for="your_name">Your name:</label><br />
  <input type="text" class="form-control" id="your_name" name="your_name" />
</div>
<div class="form-group">
  <label for="your_email">Your email:</label><br />
  <input type="email" class="form-control" id="your_email" name="your_email" />
</div>
<div class="form-group">
  <label for="your_message">Your message:</label><br />
  <textarea class="form-control" id="your_message" name="your_message"></textarea>
</div>
<button type="submit" name="submit" value="Submit" class="btn btn-primary">Submit</button>
</form>

<?php
include_once("includes/footer.php");
?>
