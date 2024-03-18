<?php
if (isset($_POST['field1']) && isset($_POST['field2'])) { // Replace 'field1' etc. with your actual field names
    $data = $_POST['field1'] . " - " . $_POST['field2'] . "\n"; 
    $file = "form_data.txt";
    file_put_contents($file, $data, FILE_APPEND);
}
?>