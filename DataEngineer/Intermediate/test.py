import unittest
import sqlite3


class TransactionTest(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect('retail.db')

    def test_number_of_transactions_on_15_01_2022(self):
        expected_nb_transactions = 54
        query = "SELECT COUNT(*) FROM transactions WHERE transaction_date = '2022-01-15'"
        result = self.conn.execute(query).fetchone()[0]

        self.assertEqual(result, expected_nb_transactions, f"Number of transactions on 2022-01-15 should be {expected_nb_transactions}")
    
    def test_unique_transaction_ids(self):
        query = "SELECT COUNT(*) FROM transactions"
        result = self.conn.execute(query).fetchone()[0]
        query = "SELECT COUNT(DISTINCT id) FROM transactions"
        result_distinct = self.conn.execute(query).fetchone()[0]

        self.assertEqual(result, result_distinct, "Transaction IDs should be unique")

    def test_quantity_positive(self):
        query = "SELECT id, quantity FROM transactions"
        result = self.conn.execute(query).fetchall()
        for res in result:
            self.assertNotEqual(res[1], "", "Quantity should not be empty")
            self.assertGreater(res[1], 0, "Quantity should be greater than 0")

    def test_transactions_type(self):
        query = "SELECT id, category FROM transactions"
        result = self.conn.execute(query).fetchall()
        for res in result:
            self.assertIn(res[1], ['SELL', 'BUY'], "Transaction type should be 'SELL' or 'BUY'")

    def test_transaction_date_format(self):
        from datetime import datetime

        query = "SELECT id, transaction_date FROM transactions"
        result = self.conn.execute(query).fetchall()

        for res in result:
            transaction_date = res[1]
            try:
                datetime.strptime(transaction_date, '%Y-%m-%d')
            except ValueError:
                self.fail(f"Transaction date '{transaction_date}' is not in the format 'YYYY-MM-DD'")

    def test_empty_description(self):
        query = "SELECT id, name FROM transactions"
        result = self.conn.execute(query).fetchall()

        for res in result:
            self.assertNotEqual(res[1], "", "Description should not be empty")
            
    def test_invalid_amount_excl_tax(self):
        query = "SELECT id, amount_excl_tax FROM transactions"
        result = self.conn.execute(query).fetchall()

        for res in result:
            self.assertNotEqual(res[1], "", "Amount excl. tax should not be empty")
            self.assertGreater(res[1], 0, "Amount excl. tax should be greater than 0")
            
    def test_invalid_amount_inc_tax(self):
        query = "SELECT id, amount_inc_tax FROM transactions"
        result = self.conn.execute(query).fetchall()

        for res in result:
            self.assertNotEqual(res[1], "", "Amount incl. tax should not be empty")
            self.assertGreater(res[1], 0, "Amount incl. tax should be greater than 0")

    def tearDown(self):
        self.conn.close()


if __name__ == '__main__':
    unittest.main()