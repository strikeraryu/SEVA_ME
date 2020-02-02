<?php
if (isset($_POST['submit'])){
    $file = $_FILES['image'];
    print_r($file);
}