# expense-tracker
A simple web app to log daily expenses

## Features
- Add expenses
- Track date
- Track price
- Track item

## Tech Stack
- Python
- Flask
- MongoDB
- HTML
- CSS

# Expense Schema
Each expense stored in MongoDB will contain:

- date (String)
- item (String)
- amount (Number)

Example:

```json
{
  "date": "23-07-2026",
  "item": "Pizza",
  "amount": 350
}
