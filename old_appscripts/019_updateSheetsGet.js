function updateSheetWithItemDetails(sheetName) {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    const columnBRange = sheet.getRange('B1:B' + sheet.getLastRow());
    const columnBValues = columnBRange.getValues();
  
    let itemIdsToRowsMap = {};
    columnBValues.forEach((value, index) => {
      let itemId = value[0];
      if (itemId) {
        itemId = itemId.toString().trim(); // Convert to string and trim whitespace
        if (itemId.length >= 5 && !isNaN(itemId)) { // Check if the string is a valid number
          itemIdsToRowsMap[itemId] = index + 1; // Map the string ID to the row number
        }
      }
    });
  
    const itemIds = Object.keys(itemIdsToRowsMap);
    if (itemIds.length === 0) {
      Logger.log("No valid item IDs found in column B.");
      return;
    }
  
    const token = YOUR_TOKEN; // Replace with your actual token
    const attributes = RELEVANT_FIELDS;
    const itemDetails = getMultipleKonimboItemDetails(itemIds, token);
  
    if (itemDetails.length === 0) {
      Logger.log("No item details fetched.");
      return;
    }
   //Logger.log("itemDetails: %s", JSON.stringify(itemDetails));
    // Writing headers
    const headersRange = sheet.getRange(1, 28, 1, attributes.length);
    headersRange.setValues([attributes]);
  
    //Logger.log("Item IDs to Rows Map: %s", JSON.stringify(itemIdsToRowsMap));
    itemDetails.forEach(details => {
      let itemId = details[0].toString().trim();
      //Logger.log("Current Item ID: %s", itemId);
      let row = itemIdsToRowsMap[itemId];
      //Logger.log("Row found: %s", row);
      if (row) {
  
        const dataRange = sheet.getRange(row, 28, 1, attributes.length);
        dataRange.setValues([details]);
      } else {
        //Logger.log("No row found for item ID %s", itemId);
      }
    });
  
  }
  