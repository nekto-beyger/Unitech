function detectChangesInAllSheets() {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheets = spreadsheet.getSheets();
    let totalDifferences = 0;
  
    for (let sheet of sheets) {
      const sheetName = sheet.getName();
      if (sheetName !== SUMMARY_SHEET && sheetName !== LOG_SHEET) {
        const differences = checkDifferences(sheet);
        totalDifferences += differences;
        Logger.log("Sheet: " + sheetName + ", Differences detected: " + differences);
      }
    }
  
    Logger.log("Total differences detected in all sheets: " + totalDifferences);
  }
  
  function checkDifferences(sheet) {
    const data = sheet.getDataRange().getValues();
  
    const fieldMap = FIELD_MAP
  
    const headers = data[0];
    const fieldMapIndices = {};
    const outputColumnIndex = headers.indexOf("isDifferent") > -1 ? headers.indexOf("isDifferent") : headers.length;
  
    if (outputColumnIndex === headers.length) {
      sheet.getRange(1, outputColumnIndex + 1).setValue("isDifferent");
    }
  
    let differencesCount = 0;
  
    for (const field in fieldMap) {
      if (field === "תיאור מקוצר") continue;
      const leftIndex = headers.indexOf(field);
      const rightIndex = headers.indexOf(fieldMap[field]);
      if (leftIndex > -1 && rightIndex > -1) {
        fieldMapIndices[leftIndex] = rightIndex;
      }
    }
  
    // Inside the for loop that iterates over rows
    for (let i = 1; i < data.length; i++) {
      const idIndex = headers.indexOf("UID");
      const mappedIdIndex = headers.indexOf("id");
      const quantityIndex = headers.indexOf("זמינות");
      let isDifferent = "";
      // Check if ID fields are equal and not empty
      if (data[i][idIndex] === data[i][mappedIdIndex] && String(data[i][idIndex]).length >= 3) {
        isDifferent = "NO";
        let differences = [];
        for (const leftIndex in fieldMapIndices) {
          const rightIndex = fieldMapIndices[leftIndex];
          const leftValue = data[i][leftIndex];
          const rightValue = data[i][rightIndex];
  
          // Special handling for the הצגה column visibilty 
          if (headers[leftIndex] === "הצגה") {
            let expectedRightValue;
            if (leftValue === "כן") {
              expectedRightValue = true;
            } else if (leftValue === "לא") {
              expectedRightValue = false;
            } else if (leftValue === "Auto") {
              expectedRightValue = data[i][quantityIndex] > 0;
            }
  
            if (rightValue !== expectedRightValue) {
              isDifferent = "YES";
              differences.push(`Row ${i + 1}: ${headers[leftIndex]} (${leftValue}) != ${headers[rightIndex]} (${rightValue})`);
            }
          } else if (!isNaN(leftValue) && !isNaN(rightValue)) {
            // Numeric comparison with threshold
            const difference = Math.abs(Number(leftValue) - Number(rightValue));
            if (difference > 1) {
              isDifferent = "YES";
              differences.push(`Row ${i + 1}: ${headers[leftIndex]} (${leftValue}) != ${headers[rightIndex]} (${rightValue})`);
            }
          } else if (leftValue !== rightValue) {
            // Standard equality check for non-numeric values
            isDifferent = "YES";
            differences.push(`Row ${i + 1}: ${headers[leftIndex]} (${leftValue}) != ${headers[rightIndex]} (${rightValue})`);
          }
        }
        sheet.getRange(i + 1, outputColumnIndex + 1).setValue(isDifferent);
  
        // Log differences
        if (differences.length > 0) {
          //Logger.log(differences.join(", "));
          differencesCount = differencesCount + 1;
        }
      }
      else {
        sheet.getRange(i + 1, outputColumnIndex + 1).setValue(isDifferent);
      }
    }
  
  
    return differencesCount;
  }
  