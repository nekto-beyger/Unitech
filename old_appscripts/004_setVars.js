const LOG_SHEET = "Log";
const SUMMARY_SHEET = "KonimboSheet";
const YOUR_TOKEN = "8aab6d778cfc4e3450fc5c44e272790e81355d338ed55b7659d1a673d0ebe716";
const API_ENDPOINT = "https://api.konimbo.co.il/v1/items/";
const baseHeaderCount = 10; // Ensure this matches the number of columns before old values

const FIELD_MAP = {
  "UID": "id",
  "זמינות": "quantity",
  "עלות": "cost",
  "דילר 1": "field_18653",
  "דילר 2": "field_18682",
  "דילר 3": "field_19032",
  "ס.לפני": "price",
  "הצגה": "visible",
  "תיאור מקוצר": "title", // new field
  "תיאור": "desc" // new field
};

RELEVANT_FIELDS = [
  "id", "quantity", "cost", "field_18653", 
  "field_18682", "field_19032", "price", "visible",
  "title", // new field
  "desc" // new field
];
