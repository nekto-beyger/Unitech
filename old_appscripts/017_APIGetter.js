function getMultipleKonimboItemDetails(itemIds, token = YOUR_TOKEN) {
    const attributes = [
      "id", "quantity", "cost", "price", "visible", "title", "desc", "discount_prices"
    ];
  
    const attributes_out = [
      "id", "quantity", "cost", "field_18653", 
      "field_18682", "field_19032", "price", "visible",
      "title", "desc"
    ];
  
    let concatenatedResults = [];
  
    for (let itemId of itemIds) {
      const attributesQuery = attributes.join(',');
      const url = `${API_ENDPOINT}/${itemId}?token=${encodeURIComponent(token)}&attributes=${attributesQuery}`;
  
      try {
        const response = UrlFetchApp.fetch(url, { 'method': 'get' });
        const statusCode = response.getResponseCode();
        const content = response.getContentText();
        //Logger.log(`content ${content}`);
  
        if (statusCode === 200) {
          const itemData = JSON.parse(content);
  
          // Constructing the unnested data object
          const unnestedData = {
            id: itemData.id,
            quantity: itemData.quantity,
            cost: itemData.cost,
            price: itemData.price,
            visible: itemData.visible,
            title: itemData.title,
            desc: itemData.desc,
            ...itemData.discount_prices  // Spread the discount_prices object
          };
          //Logger.log(`unnestedData ${JSON.stringify(unnestedData)}`);
  
          // Map the data to the attributes_out order
          const sheetData = attributes_out.map(attr => unnestedData[attr]);
  
          concatenatedResults.push(sheetData);
        } else {
          Logger.log(`Failed to fetch item details for item ID ${itemId}. Status code: ${statusCode}`);
        }
      } catch (error) {
        Logger.log(`Error fetching item details for item ID ${itemId}: %s`, error.toString());
      }
  
      // Waiting for 2 seconds before the next API call
      Utilities.sleep(1000);
    }
  
    return concatenatedResults;
  }
  