function runGetOnRandomThirdSheets() {
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    var allSheets = spreadsheet.getSheets();
    var sheetsToProcess = getRandomThird(allSheets);
  
    var excludeSheets = [SUMMARY_SHEET, LOG_SHEET];
  
    for (var i = 0; i < sheetsToProcess.length; i++) {
      var sheet = sheetsToProcess[i];
      var sheetName = sheet.getName();
      Logger.log('Begins Sheet: %s', sheetName);
      if (excludeSheets.indexOf(sheetName) === -1) {
        // Call your function here
        updateSheetWithItemDetails(sheetName);
      }
      Logger.log('Done Sheet: %s', sheetName);
    }
  }
  
  function getRandomThird(sheets) {
    var totalSheets = sheets.length;
    var numberOfSheetsToProcess = Math.ceil(totalSheets / 3);
    shuffleArray(sheets); // Randomly shuffle the array
    var selectedSheets = sheets.slice(0, numberOfSheetsToProcess);
  
    // Log the names of selected sheets
    var selectedSheetNames = selectedSheets.map(function(sheet) { return sheet.getName(); });
    Logger.log("Selected Sheets: " + selectedSheetNames.join(", "));
  
    return selectedSheets;
  }
  
  function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
  }
  