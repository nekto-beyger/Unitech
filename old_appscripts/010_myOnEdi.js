function onMyEdit(e) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getActiveSheet();
    var sheetName = sheet.getName();
    
    //checks that we're on the correct sheet.
    if(sheetName !== "Log") {
      var selectedCell = ss.getActiveCell();
      //checks the column to ensure it is on the one we want to cause the date to appear.
      if(selectedCell.getColumn() == COLUMNTOCHECK1) { 
        var dateTimeCell = selectedCell.offset(DATETIMELOCATION1[0],DATETIMELOCATION1[1]);
        dateTimeCell.setValue(new Date());
      }
      handleKonimboUpdate(e);
    }
  }
  