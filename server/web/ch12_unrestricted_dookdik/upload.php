<?php

if(session_status()!=PHP_SESSION_ACTIVE){ session_start();}

$message = ''; 
if (isset($_POST['uploadBtn']) && $_POST['uploadBtn'] == 'Upload')
{
  if (isset($_FILES['uploadedFile']) && $_FILES['uploadedFile']['error'] === UPLOAD_ERR_OK)
  {
    // get details of the uploaded file
    $fileTmpPath = $_FILES['uploadedFile']['tmp_name'];
    $fileName = $_FILES['uploadedFile']['name'];
    $fileType = $_FILES['uploadedFile']['type'];
    $fileNameCmps = explode(".", $fileName);
    $fileExtension = strtolower(end($fileNameCmps));

    if(strpos($fileName,'.gif')===false)//check file extension
    {
      $message = 'Only .gif plz !';
    }
    else
    {
      if($fileType != 'image/gif')//check MIME
      {
        $message = 'MIME is a joke !';
      }
      else
      {
        $finfo = finfo_open(FILEINFO_MIME_TYPE);
        $mime = finfo_file($finfo, $fileTmpPath);
        if($mime != 'image/gif') //check magic
        {
          $message = 'Show me the MAGIC !';
        }
        else
        {
          //Prevent someone being nauty
          $file_contents = file_get_contents($fileTmpPath);
          $file_contents = str_replace("<?php", "", $file_contents);
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
    }
  }
}
$_SESSION['message'] = $message;
header("Location: index.php");
