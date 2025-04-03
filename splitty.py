import csv
from collections import defaultdict
from datetime import datetime
import heapq

class ExpenseSplitter:
    def __init__(self):
        self.balances = defaultdict(float)
        self.transactions = []
        self.total_processed = 0

    def load_expenses_from_csv(self, filename):
        print("Loading transactions...")  # Debug line
        
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            # Clear any existing data
            self.balances.clear()
            self.transactions.clear()
            self.total_processed = 0
            
            for row in reader:
                try:
                    # Parse amount (handle negative values correctly)
                    amount = float(row['amount'].strip())
                    
                    # Get creditor and clean it
                    creditor = row['creditor'].strip()
                    
                    # Get participants and clean them
                    participants = [p.strip() for p in row['participants'].split('/') if p.strip()]
                    
                    # Get date
                    date = row['date'].strip()
                    
                    # Get subject
                    subject = row['subject'].strip()
                    
                    # Only process if we have valid participants
                    if participants:
                        # Calculate share per person
                        share_per_person = amount / len(participants)
                        
                        # Add the full amount to creditor's balance
                        self.balances[creditor] += amount
                        
                        # Subtract each participant's share
                        for participant in participants:
                            self.balances[participant] -= share_per_person
                        
                        # Store transaction
                        transaction = {
                            'date': date,
                            'creditor': creditor,
                            'subject': subject,
                            'amount': amount,
                            'participants': participants.copy(),  # Make a copy to avoid reference issues
                            'share_per_person': share_per_person
                        }
                        self.transactions.append(transaction)
                        self.total_processed += abs(amount)  # Use absolute value for total processed
                        
                        # Debug print
                        print(f"Processed: {date} - {creditor} - {subject} - {amount:.2f}")
                    
                except Exception as e:
                    print(f"Error processing row: {row}")
                    print(f"Error details: {str(e)}")
                    continue

    def verify_balances(self):
        total_balance = sum(self.balances.values())
        is_valid = abs(total_balance) < 0.01  # Account for floating point imprecision
        return {
            'is_valid': is_valid,
            'total_balance': total_balance,
            'total_processed': self.total_processed,
            'total_transactions': len(self.transactions)
        }

    def get_summary(self):
        # Sort balances by amount
        sorted_balances = sorted(self.balances.items(), key=lambda x: x[1])
        
        # Format the results
        summary = "\nFinal Balances:\n"
        summary += "=" * 50 + "\n"
        
        positive_balance = 0
        negative_balance = 0
        
        for person, balance in sorted_balances:
            if abs(balance) >= 0.01:  # Only show non-zero balances
                if balance > 0:
                    summary += f"{person} should receive €{balance:.2f}\n"
                    positive_balance += balance
                else:
                    summary += f"{person} should pay €{abs(balance):.2f}\n"
                    negative_balance += abs(balance)
        
        # Add verification information
        verification = self.verify_balances()
        summary += "\nVerification:\n"
        summary += "=" * 50 + "\n"
        summary += f"Number of transactions: {verification['total_transactions']}\n"
        summary += f"Total money exchanged: €{self.total_processed:.2f}\n"
        summary += f"Total to be paid: €{negative_balance:.2f}\n"
        summary += f"Total to be received: €{positive_balance:.2f}\n"
        summary += f"Balance check difference: €{verification['total_balance']:.2f}\n"
        summary += f"Balance check: {'✓ Valid' if verification['is_valid'] else '✗ Invalid'}\n"
        
        return summary

    def get_recent_transactions(self, limit=5):
        # Sort transactions by date (most recent first)
        sorted_transactions = sorted(
            self.transactions,
            key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'),
            reverse=True
        )
        
        summary = f"\nMost Recent {limit} Transactions:\n"
        summary += "=" * 50 + "\n"
        
        shown_transactions = []
        for transaction in sorted_transactions:
            # Check if this transaction is already shown
            transaction_key = f"{transaction['date']}_{transaction['creditor']}_{transaction['amount']}"
            if transaction_key in shown_transactions:
                continue
                
            shown_transactions.append(transaction_key)
            
            if len(shown_transactions) > limit:
                break
                
            summary += (f"Date: {transaction['date']}\n"
                       f"Paid by: {transaction['creditor']}\n"
                       f"Subject: {transaction['subject']}\n"
                       f"Amount: €{transaction['amount']:.2f}\n"
                       f"Split between ({len(transaction['participants'])} people): {', '.join(transaction['participants'])}\n"
                       f"Share per person: €{transaction['share_per_person']:.2f}\n"
                       f"{'-' * 30}\n")
        
        return summary

    def calculate_debt_resolution(self):
        """Calculate the optimal way to resolve all debts."""
        # Create lists of debtors and creditors with their amounts
        debtors = []  # people who need to pay (negative balance)
        creditors = []  # people who need to receive (positive balance)
        
        for person, balance in self.balances.items():
            if abs(balance) >= 0.01:  # Only consider non-zero balances
                if balance < 0:
                    heapq.heappush(debtors, (balance, person))  # negative values
                elif balance > 0:
                    heapq.heappush(creditors, (-balance, person))  # negative values for heap
        
        # Generate resolution steps
        resolution_steps = []
        
        while debtors and creditors:
            debt_amount, debtor = heapq.heappop(debtors)
            credit_amount, creditor = heapq.heappop(creditors)
            
            # Convert to positive values
            debt_amount = abs(debt_amount)
            credit_amount = abs(credit_amount)
            
            # Calculate the transfer amount
            transfer_amount = min(debt_amount, credit_amount)
            
            if abs(transfer_amount) >= 0.01:  # Only include non-zero transfers
                resolution_steps.append({
                    'from': debtor,
                    'to': creditor,
                    'amount': transfer_amount
                })
            
            # If there's remaining balance, push back to heap
            remaining_debt = debt_amount - transfer_amount
            remaining_credit = credit_amount - transfer_amount
            
            if remaining_debt >= 0.01:
                heapq.heappush(debtors, (-remaining_debt, debtor))
            if remaining_credit >= 0.01:
                heapq.heappush(creditors, (-remaining_credit, creditor))
        
        return resolution_steps

    def get_resolution_summary(self):
        """Generate a formatted summary of debt resolution steps."""
        resolution_steps = self.calculate_debt_resolution()
        
        summary = "\nDebt Resolution Steps:\n"
        summary += "=" * 50 + "\n"
        
        if not resolution_steps:
            summary += "No debts to resolve!\n"
            return summary
        
        total_movements = 0
        summary += "To resolve all debts, the following payments should be made:\n\n"
        
        for step in resolution_steps:
            summary += f"➤ {step['from']} should pay €{step['amount']:.2f} to {step['to']}\n"
            total_movements += step['amount']
        
        summary += "\n" + "-" * 50 + "\n"
        summary += f"Total money to be transferred: €{total_movements:.2f}\n"
        summary += f"Number of transactions needed: {len(resolution_steps)}\n"
        
        return summary

def main():
    print(f"Expense Report generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 50)
    
    splitter = ExpenseSplitter()
    splitter.load_expenses_from_csv('expenses.csv')
    
    # Print the summaries
    print(splitter.get_summary())
    print(splitter.get_resolution_summary()) 
    print(splitter.get_recent_transactions())

if __name__ == "__main__":
    main()
