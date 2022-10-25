<?php

if(session_status()!=PHP_SESSION_ACTIVE){ session_start();}
header("Location: index.php");

$message = ''; 

if (isset($_FILES['uploadedFile']) && $_FILES['uploadedFile']['error'] === UPLOAD_ERR_OK) {
  // get details of the uploaded file
  $fileTmpPath = $_FILES['uploadedFile']['tmp_name'];
  $fileName = $_FILES['uploadedFile']['name'];
  $fileType = $_FILES['uploadedFile']['type'];
  $fileNameCmps = explode(".", $fileName);
  $fileExtension = strtolower(end($fileNameCmps));

  $finfo = finfo_open(FILEINFO_MIME_TYPE);
  $mime = finfo_file($finfo, $fileTmpPath);

  // Check file size
  if ($_FILES['uploadedFile']['size'] > 25) {
    $message = 'GIF is too big !';
  }
  // Check file extension
  else if (strpos($fileName,'.gif') === false) {
    $message = 'Only .gif plz !';
  }
  // Check MIME
  else if($fileType != 'image/gif') {
    $message = 'MIME is a joke !';
  }
  // Check Magic
  else if($mime != 'image/gif') {
    $message = 'Show me the MAGIC !';
  } else {
    //Prevent someone being nauty
    $file_contents = file_get_contents($fileTmpPath);
    $file_contents = str_replace("<?", "", $file_contents);
    file_put_contents($fileTmpPath, $file_contents);
    // rename
    $newFileName = md5(time() . $fileName) . '.' . $fileExtension;
    // directory in which the uploaded file will be moved
    $uploadFileDir = './uploads/';
    $dest_path = $uploadFileDir . $newFileName;
    if(move_uploaded_file($fileTmpPath, $dest_path)) 
    {
      $message ='File is successfully uploaded at'.$dest_path;
    }
    else 
    {
      $message = 'There is some error in the file upload. Please check the following error.<br>';
      $message .= 'Error:' . $_FILES['uploadedFile']['error'];
    }
  }
}

$_SESSION['message'] = $message;
echo $message;
