function updateRowsWithDifferences() {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheets = spreadsheet.getSheets();
    let totalUpdated = 0;
  
    for (let sheet of sheets) {
      const sheetName = sheet.getName();
      if (sheetName !== SUMMARY_SHEET && sheetName !== LOG_SHEET) {
        Logger.log(`Processing sheet: ${sheetName}`);
        const data = sheet.getDataRange().getValues();
        const headers = data[0];
        const idIndex = headers.indexOf("UID");
        const diffIndex = headers.indexOf("isDifferent");
        let sheetUpdatedCount = 0;
  
        for (let i = 1; i < data.length; i++) {
          const row = data[i];
          const id = String(row[idIndex]);
          const isDifferent = row[diffIndex];
  
          if (isDifferent === "YES" && id.length > 3 && id.length < 12) {
            const itemData = extractItemData(row, headers);
            updateKonimboStore(itemData);
            sheetUpdatedCount++;
          }
        }
  
        totalUpdated += sheetUpdatedCount;
        Logger.log(`Updated ${sheetUpdatedCount} rows in sheet: ${sheetName}`);
      }
    }
  
    Logger.log(`Total rows updated across all sheets: ${totalUpdated}`);
  }
  
  
  
  
  function extractItemData(row, headers) {
    const fieldMap = FIELD_MAP;
  
    let itemData = {};
  
    for (let [hebrewField, englishField] of Object.entries(fieldMap)) {
      const fieldIndex = headers.indexOf(hebrewField);
      if (fieldIndex !== -1) {
        itemData[englishField] = row[fieldIndex];
      }
    }
  
    // Special handling for 'visible'
    if (itemData.visible === "כן") {
      itemData.visible = true;
    } else if (itemData.visible === "לא") {
      itemData.visible = false;
    } else if (itemData.visible === "Auto") {
      itemData.visible = itemData.quantity > 0;
    }
  
    return {
      id: itemData.id,
      quantity: itemData.quantity,
      cost: itemData.cost,
      price: itemData.price,
      visible: itemData.visible,
      title: itemData.title,
      desc: itemData.desc,
      discount_prices: {
        field_18653: itemData.field_18653,
        field_18682: itemData.field_18682,
        field_19032: itemData.field_19032
      }
    };
  }
  