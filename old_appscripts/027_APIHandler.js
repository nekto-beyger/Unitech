
function updateKonimboStore(itemData) {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(SUMMARY_SHEET);
    /*
    const rowForItem = findRowById(sheet, itemData.id);
  
    if (!rowForItem) {
        Logger.log(`Row for item ID: ${itemData.id} not found.`);
        return { success: false, statusCode: 0, content: 'Row not found' };
    }
    */
  
    console.log("itemData:", itemData);
  
    const discount_prices = {
      field_18653: itemData.discount_prices.field_18653,
      field_18682: itemData.discount_prices.field_18682,
      field_19032: itemData.discount_prices.field_19032
    };
    console.log("discount_prices:", discount_prices);
    // Construct the payload based on the provided structure
    const payload = {
      token: YOUR_TOKEN,
      item: {
        id: itemData.id,
        quantity: itemData.quantity,
        cost: itemData.cost,
        price: itemData.price,
        visible: itemData.visible,
        //title: itemData.title, // new field
        desc: itemData.desc,
        discount_prices: discount_prices,
        inventory: [
          {
            code: "",
            free: itemData.quantity // Assuming "free" should match the "quantity"
          }
        ]
      }
    };
  
  
    // Logging the payload for cloud logs
    //Logger.log('Sending payload to Konimbo: %s', JSON.stringify(payload));
  
    // Setting up the options for the API call
    const options = {
      method: "PUT",
      contentType: "application/json",
      headers: {
        'Authorization': `Bearer ${YOUR_TOKEN}`
      },
      payload: JSON.stringify(payload)
    };
  
    // Rest of your code...
  
    try {
        // Make the API call
        const beginTime = new Date().toISOString();
        const response = UrlFetchApp.fetch(API_ENDPOINT + itemData.id, options);
        const statusCode = response.getResponseCode();
        const content = response.getContentText();
        /*
        if (rowForItem) {
          const endTime = new Date().toISOString();
          
          // Update Begin Time, End Time, and Response Code in the correct columns
          sheet.getRange(rowForItem, 21).setValue(beginTime); // Column U
          sheet.getRange(rowForItem, 22).setValue(endTime);   // Column V
          sheet.getRange(rowForItem, 23).setValue(statusCode); // Column W
        }
        */
        // Update old values if the API call was successful
        if (statusCode === 200) {
            Logger.log(`API call returned statusCode: ${statusCode}`);
        } else {
            Logger.log(`API call returned statusCode: ${statusCode}`);
        }
        return { success: true, statusCode: statusCode, content: content };
  
    } catch (error) {
        Logger.log('Error updating Konimbo: %s', error.toString());
        return { success: false, statusCode: 0 , content: '' };
    }
  
  // Rest of your code...
  
  }
  
  function initializeSummaryHeaders(sheet) {
    const headers = ["Begin Time", "End Time", "Response Code"];
    
    // Fetch the current headers from the sheet
    const currentHeaders = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    
    // Check if each of the headers already exists
    const allHeadersExist = headers.every(header => currentHeaders.includes(header));
  
    // If not all headers exist, append them to the end
    if (!allHeadersExist) {
      const lastColumn = sheet.getLastColumn();
      sheet.getRange(1, lastColumn + 1, 1, headers.length).setValues([headers]);
    }
  }
  
  
  // Find the row number for a specific ID in the sheet
  function findRowById(sheet, id) {
    const data = sheet.getDataRange().getValues();
    for (let i = 0; i < data.length; i++) {
      if (data[i][0] === id) {
        return i + 1; // Rows are 1-indexed
      }
    }
    return null;
  }
  
  function updateMultipleKonimboStore(itemsToUpdate, sheet) {
    if (!Array.isArray(itemsToUpdate) || itemsToUpdate.length === 0) {
      Logger.log("No items to update.");
      return;
    }
  
    const delayMs = Math.ceil((10 * 60 * 1000) / 500); // Delay calculation
    const baseHeaderCount = 10; // Match this with your column count
    const oldValuesStartCol = baseHeaderCount + 1; // Column index where old values start
  
    for (const item of itemsToUpdate) {
      const result = updateKonimboStore(item.data);
      
      if (result.success) {
        // Update the old values with the new values
      for (let i = 0; i < baseHeaderCount; i++) {
          const header = sheet.getRange(1, i + 1).getValue();
          const newValue = item.data[header];
          sheet.getRange(item.rowIndex, i + oldValuesStartCol).setValue(newValue);
      }
  
        // Update timestamps and response code
        const timestamp = new Date();
        sheet.getRange(item.rowIndex, 21).setValue(timestamp); // Begin Time
        sheet.getRange(item.rowIndex, 22).setValue(timestamp); // End Time
        sheet.getRange(item.rowIndex, 23).setValue(result.statusCode); // Response Code
      }
  
      Utilities.sleep(delayMs);
    }
  }
  
  