/**
* Creates a Date Stamp if a column is edited.
*/
 
//CORE VARIABLES
// The column you want to check if something is entered.
var COLUMNTOCHECK1 = 10; //
// Where you want the date time stamp offset from the input location. [row, column]
var DATETIMELOCATION1 = [0,-9]; //התזוזה 
// Sheet you are working on


function onOpen(){

}


function onEdit(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  //checks that we're on the correct sheet.
    var selectedCell = ss.getActiveCell();
    //checks the column to ensure it is on the one we want to cause the date to appear.
    if( selectedCell.getColumn() == COLUMNTOCHECK1) { 
      var dateTimeCell = selectedCell.offset(DATETIMELOCATION1[0],DATETIMELOCATION1[1]);
      dateTimeCell.setValue(new Date());
      }
  //handleKonimboUpdate(e)
}

