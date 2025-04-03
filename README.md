# Splitty - Expense Splitter
*Last updated: 2025-04-03 20:04:31 UTC*  
*Author: Andres-Briones*

A Python script for managing and splitting shared expenses among groups.

## Features

- Load and process expenses from CSV files
- Calculate individual balances
- Show recent transactions
- Generate optimal debt resolution steps
- Verify that all balances sum to zero
- Support special characters in names
- Handle negative amounts (reimbursements)

## CSV File Format Guide

Your expenses.csv file must contain these columns in order, separated by semicolons:

creditor;subject;participants;date;amount

Each column explained:

1. creditor: 
   - Who paid for the expense
   - Example: Sophie, Erik, Mathilde

2. subject:
   - Description of the expense
   - Example: Groceries, Internet Bill, House Supplies
   - Use "Settled up" for direct reimbursements

3. participants:
   - Who shares the expense
   - Names separated by forward slashes
   - No spaces around slashes
   - Must include the creditor if they share the expense
   - Example: Sophie/Erik/Mathilde

4. date:
   - When the expense occurred
   - Format: YYYY-MM-DD
   - Example: 2025-04-03

5. amount:
   - Cost of the expense
   - Use period or comma for decimal separator
   - Can be negative for reimbursements
   - Example: 45.30 or -20.50

## Usage Guide

1. Prepare your CSV file:
   - Name it expenses.csv
   - Use semicolons as separators
   - Include the header row exactly as shown above
   - Save with UTF-8 encoding

2. Example of valid entries:
   
   Sophie;Groceries;Sophie/Erik/Mathilde;2025-04-02;45.30  
   Erik;Internet Bill;Erik/Sophie/Mathilde/Lou;2025-04-01;55.00  
   Mathilde;Reimbursement;Sophie/Mathilde;2025-04-01;-20.50

3. Place the CSV file in same directory as splitty.py

4. Run the script:
   python splitty.py

## Output Sections

The script will generate three sections:

1. Current Balances
   - Shows who owes money and who should receive
   - All amounts in euros (€)
   - Only shows non-zero balances

2. Debt Resolution Steps
   - Lists the optimal payments to settle all debts
   - Minimizes the number of transactions needed
   - Shows total money to be transferred
   - Shows number of transactions needed

3. Recent Transactions
   - Shows the most recent expenses
   - Includes date, creditor, subject, amount
   - Shows how the expense was split
   - Shows individual shares

## Troubleshooting

Common issues and their solutions:

1. File Encoding
   - Make sure to save your CSV as UTF-8
   - Avoid special characters in file name

2. Date Format
   - Always use YYYY-MM-DD
   - Leading zeros required for days/months

3. Number Format
   - Use either dots (45.30) or commas (45,30)
   - No currency symbols in the amount field
   - No spaces in numbers

4. Participant Names
   - Be consistent with spelling and capitalization
   - No spaces around the forward slashes
   - No empty participants

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Feel free to submit issues and enhancement requests!

## Support

For help and support:
1. Check the troubleshooting section
2. Submit an issue on GitHub
3. Contact the author
