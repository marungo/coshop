<!DOCTYPE HTML>
<html>
<head>
<style>
.error {color: #FF0000;}
</style>
</head>
<body>

<?php
  // define variables and set to empty values
  $emailErr = "";
  $website = "";


  if (empty($_POST["website"])) {
    $website = "";
  } else {
    $website = test_input($_POST["website"]);
    // check if URL address syntax is valid
    if (!preg_match("/\b(?:(?:https?|ftp):\/\/|www\.)[-a-z0-9+&@#\/%?=~_|!:,.;]*[-a-z0-9+&@#\/%=~_|]/i",$website)) {
      $websiteErr = "Invalid URL";
    }
  }

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}
?>

<h2>PHP Form Validation Example</h2>
<p><span class="error">* required field.</span></p>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
  Amazon URL: <input type="text" name="website">
  <span class="error"><?php echo $websiteErr;?></span>
  <br><br>
  <input type="submit" name="submit" value="Submit">
</form>

<?php
echo "<h2>Your Product's ID:</h2>";
$ItemId = explode("/", explode ("dp/" , $website)[1])[0];
// $ItemId = explode ("/", $website[1]);
echo $ItemId;

//Enter your IDs
define("Access_Key_ID", "AKIAILT6XJREK4ITJJZA");
define("Associate_tag", "coshopsmaymng-20");

ItemLoopup($ItemId);

//Set up the operation in the request
function ItemLookup($ItemId){

  //Set the values for some of the parameters
  $Operation = "ItemLookup”;
  $Version = "2013-08-01";
  $ResponseGroup = "ItemAttributes,OfferFull,Images”;
  //User interface provides values
  //for $SearchIndex and $Keywords

  //Define the request
  $request=
    "http://webservices.amazon.com/onca/xml"
     . "?Service=AWSECommerceService"
     . "&AssociateTag=" . Associate_tag
     . "&AWSAccessKeyId=" . Access_Key_ID
     . "&Operation=" . $Operation
     . “&ItemId=" . $ItemId
     . "&ResponseGroup=" . $ResponseGroup;

  //Catch the response in the $response object
  $response = file_get_contents($request);
  $parsed_xml = simplexml_load_string($response);
  printSearchResults($parsed_xml, $SearchIndex);
}

function printSearchResults($parsed_xml, $SearchIndex){
   print("<table>");
  API Version 2013-08-01
  27
  Product Advertising API Getting Started Guide
  PHP
   if($numOfItems>0){
   foreach($parsed_xml->Items->Item as $current){
   print("<td><font size='-1'><b>".$current->ItemAttributes->Title."</b>");
   if (isset($current->ItemAttributes->Title)) {
   print("<br>Title: ".$current->ItemAttributes->Title);
   } elseif(isset($current->ItemAttributes->Author)) {
   print("<br>Author: ".$current->ItemAttributes->Author);
   } elseif
   (isset($current->Offers->Offer->OfferListing->Price->FormattedPrice)){
   print("<br>Price:
   ".$current->Offers->Offer->OfferListing->Price->FormattedPrice);
   }else{
   print("<center>No matches found.</center>");
   }
   }
 }
}
?>

</body>
</html>
