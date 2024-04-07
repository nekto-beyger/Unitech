
function isColumnOfInterest(columnNumber) {
    const columnsOfInterest = [7, 8, 10, 11, 16, 17, 18, 20, 21, 22]; // Added 7 and 8 for title and desc
    return columnsOfInterest.includes(columnNumber);
  }
  
  function getMappedHeaders(headers) {
    var fieldMap = FIELD_MAP;
    return headers.map(header => fieldMap[header] || header);
  }
  
  function getMappedData(row, mappedHeaders) {
    var relevantFields = RELEVANT_FIELDS;
    Logger.log('rowIn: %s', row);
    let itemData = {};
  
    for (let i = 0; i < row.length; i++) {
      const header = mappedHeaders[i];
      if (relevantFields.includes(header)) {
        itemData[header] = row[i];
      }
    }
  
    // Convert specific fields if needed
    if (itemData.id) {
      itemData.id = Number(itemData.id);
    }
  
    // Adjust visibility based on the new rules
    switch(itemData.visible) {
      case "כן":
        itemData.visible = true;
        break;
      case "לא":
        itemData.visible = false;
        break;
      default: // This will catch "אוטו" or any other value
        itemData.visible = itemData.quantity > 0;
        break;
    }
    return itemData;
  }
  