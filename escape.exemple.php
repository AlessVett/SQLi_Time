<?php

  $dns = 'dblib:host=your_hostname;dbname=your_db;charset=UTF-8';
  $localhost = 'localhost';
  $username = 'username';
  $password = 'password';
  $database = 'database';
  $port = 'port';
  $socket = null;
  $options = null;


  /**
   * Nel caso in cui si utilizzasse la classe PDO
   * (E' uno dei tanti modi in cui si può utilizzare)
   */
  $pdo = new PDO(
      $dns,
      $username,
      $password,
      $options
  );
  //
  $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
  $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  //
  $query = "UPDATE table_name SET column_name1 = :value1 WHERE column_name2 = :value2";
  $request = $pdo->prepare($query);
  //
  $value1 = $_GET['value1'];
  $request->bindParam(":value1", $value1, PDO::PARAM_STR);
  //
  $value2 = $_GET['value2'];
  $request->bindParam(":value2", $value2, PDO::PARAM_STR);
  //
  $request->execute();
  $result = $request->fetchAll(PDO::FETCH_ASSOC);
  print_r($result);


  /**
   * Nel caso in cui si utilizzasse la funzione mysqli_connect
   * (E' uno dei tanti modi in cui si può utilizzare)
   */
  $mysqli = mysqli_connect(
      $localhost,
      $username,
      $password,
      $database,
      $port,
      $socket
  );
  //
  $query = "UPDATE table_name SET column_name1 = :value1 WHERE column_name2 = :value2";
  //
  $value1 = $mysqli->escape_string($_GET['value1']);
  $value2 = $mysqli->escape_string($_GET['value2']);
  $values = array(
      ":value1" => $value1,
      ":value2" => $value2
  );
  //
  $query = strtr($query, $values);
  //
  $request = mysqli_query($mysqli, $query);
  $result = $request->fetch_assoc();
  print_r($result);
?>
