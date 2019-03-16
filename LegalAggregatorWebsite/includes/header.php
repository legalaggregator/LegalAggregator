<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    <style type="text/css">
      .auto-margin {
        margin: 0px 10%;
      }
      @media all and (max-width: 699px) {
        .auto-margin {
          margin: 0px 10px;
        }
      }
    </style>

    <title>
<?php
$links = array("Home" => "index.php", "Contact" => "contact.php");
foreach ($links as $title => $url)
  if (strpos($_SERVER["SCRIPT_NAME"], $url) !== false) print($title . ", Legal Aggregator");
?>
    </title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light auto-margin">
      <a class="navbar-brand" href="index.php">Legal Aggregator</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
<?php
foreach ($links as $title => $url) {
  $active = "";
  if (strpos($_SERVER["SCRIPT_NAME"], $url) !== false) $active = "active";
  print("<li class='nav-item $active'><a class='nav-link' href='$url'>$title</a></li>");
}
?>
        </ul>
      </div>
    </nav>
    <div class="auto-margin">
      <div style="background-image: url(/images/heros/data2.jpg); width: 100%; background-size: cover; color: #ffffff;">
        <div style="padding: 40px 20px; ">
          <h1 style="font-family: courier new;">Legal Aggregator</h1>
          <h5 style="font-weight: normal;">Gathering and analyzing trends in the legal industry.</h5>
        </div>
      </div>
      <div style="border: solid 1px #dddddd; border-top: none; min-height: 400px; padding: 20px; font-family: serif; font-size: 20px;">
