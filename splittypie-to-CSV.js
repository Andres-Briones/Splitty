/**
 * Usage: Copy this entire snippet and paste it into the developer console in the transactions page of SplittyPie.
 * A link will appear on the top just above the event title (on Desktop view).
 * Just click it to get a CSV containing the expenses.
 *
 * This version uses semicolons (;) as separators and replaces commas in fields with spaces
 * to avoid CSV parsing issues.
 */

function collect() {
  const selectors = Object.entries({
    month: '.month',
    day: '.day',
    creditor: '.transaction-list-item-description strong',
    subject: '.transaction-list-item-description em',
    participants: '.transaction-list-item-description small',
    amount: '.transaction-list-item-amount strong',
  });

  const expenses = [];
  let year = undefined;
  for (let div of document.querySelectorAll('.transaction-list-item')) {
    const previousSibling = div.previousElementSibling;
    if (previousSibling?.classList.contains('transaction-list-date')) {
      const yearStr = previousSibling.querySelector('strong').innerText;
      year = parseInt(yearStr.replace(/^\D*/g, ''), 10);
    }

    const expense = Object.fromEntries(selectors.map(([field, selector]) => {
      let value = div.querySelector(selector)?.innerText?.trim() || '';
      // Replace commas with spaces in all fields except participants
      if (field !== 'participants') {
        value = value.replace(/,/g, ' ');
      }
      return [field, value];
    }));

    const timestamp = Date.parse(`${expense.month} ${expense.day} ${year}`);
    const date = Number.isNaN(timestamp)
      ? null
      : new Date(timestamp).toISOString().substring(0, 10);
    
    if (!expense.participants && /settled up/i.test(div.innerText)) {
      expense.subject = 'Settled up';
      expense.participants = div.querySelector('strong:last-child').innerText.trim();
    }

    expenses.push({
      creditor: expense.creditor,
      subject: expense.subject,
      // For participants, we still use "/" as separator between names
      participants: expense.participants?.split(/\s*,\s*/).join('/'),
      date,
      amount: parseFloat(expense.amount),
    });
  }

  return expenses;
}

const link = document.createElement('a');
document.querySelector('main .container').prepend(link);
link.innerText = 'Scrapping…';

const csvFields = ['creditor', 'subject', 'participants', 'date', 'amount'];

// Create CSV content with semicolon separator
const csvContent = [
  // Header row
  csvFields.join(';'),
  // Data rows
  ...collect().map(expense => 
    csvFields.map(field => {
      // Ensure all fields are properly escaped if they contain semicolons
      const value = String(expense[field] || '');
      return value.includes(';') ? `"${value}"` : value;
    }).join(';')
  )
].join('\n');

const url = window.URL.createObjectURL(new Blob([csvContent], { type: 'text/csv' }));
link.setAttribute('href', url);
link.setAttribute('download', 'expenses.csv');
link.innerText = 'Download expenses as CSV';
