<?php
if(session_status()!=PHP_SESSION_ACTIVE){ session_start();}
?>
<!DOCTYPE html>
<html>
<head>
  <title>Bankde's GIF Storage</title>
  <!-- Bootstrap -->
  <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
      crossorigin="anonymous"
    />
</head>
<body>
  <div class="container mt-5">
    <h1>Bankde's GIF Storage</h1>
    <?php if (isset($_SESSION['message']) && $_SESSION['message']) { ?>
      <div class="alert alert-danger" role="alert">
        <?=$_SESSION['message']?>
      </div>
    <?php unset($_SESSION['message']); } ?>
      
    <form method="POST" action="upload.php" enctype="multipart/form-data">
      <label class="form-label" for="uploadedFile">Put your GIF here:</label>
      <input type="file" class="form-control" id="uploadedFile" name="uploadedFile" />

      <button type="submit" name="uploadBtn" class="btn btn-primary mt-3">Upload GIF</button>
    </form>
  </div>
</body>
</html>
