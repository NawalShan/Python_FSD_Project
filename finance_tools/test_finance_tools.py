import unittest
from finance_tools import (
    calculate_emi,
    calculate_sip,
    calculate_fd,
    calculate_rd,
    estimate_retirement_corpus,
    estimate_home_loan_eligibility,
    calculate_credit_card_balance,
    calculate_taxable_income,
    plan_budget,
    calculate_net_worth,
)


class TestFinanceTools(unittest.TestCase):
    # EMI tests
    def test_calculate_emi_normal(self):
        emi = calculate_emi(100000, 10, 1)  # 1 year, 10% p.a.
        self.assertIsInstance(emi, float)
        # approximate expected EMI (manual calc)
        self.assertAlmostEqual(emi, 8791.59, places=2)

    def test_calculate_emi_zero_interest(self):
        emi = calculate_emi(120000, 0, 1)
        self.assertEqual(emi, 10000.0)  # 120000 / 12

    # SIP tests
    def test_calculate_sip_normal(self):
        amount = calculate_sip(1000, 12, 1)
        self.assertIsInstance(amount, float)
        # positive amount greater than contributions
        self.assertGreater(amount, 12000.0)

    def test_calculate_sip_zero_return(self):
        amount = calculate_sip(1000, 0, 2)
        self.assertEqual(amount, 24000.0)

    # FD tests
    def test_calculate_fd_normal(self):
        fd = calculate_fd(10000, 6, 2)  # yearly compounding
        self.assertGreater(fd, 10000.0)

    def test_calculate_fd_invalid_principal(self):
        with self.assertRaises(ValueError):
            calculate_fd(0, 5, 1)

    # RD tests
    def test_calculate_rd_normal(self):
        rd = calculate_rd(2000, 6, 1)
        self.assertGreater(rd, 24000.0)

    def test_calculate_rd_invalid_negative(self):
        with self.assertRaises(ValueError):
            calculate_rd(-100, 5, 1)

    # Retirement estimator
    def test_estimate_retirement_corpus_normal(self):
        corpus = estimate_retirement_corpus(50000, 2000, 8, 10)
        self.assertIsInstance(corpus, float)
        self.assertGreater(corpus, 50000.0)

    def test_estimate_retirement_invalid_years(self):
        with self.assertRaises(ValueError):
            estimate_retirement_corpus(10000, 100, 5, 0)

    # Home loan eligibility
    def test_estimate_home_loan_eligibility_normal(self):
        loan = estimate_home_loan_eligibility(50000, 20000, 8, 20)
        self.assertIsInstance(loan, float)
        self.assertGreater(loan, 0)

    def test_estimate_home_loan_invalid_percent(self):
        with self.assertRaises(ValueError):
            estimate_home_loan_eligibility(50000, 10000, 8, 20, max_emi_percent=200)

    # Credit card balance
    def test_calculate_credit_card_balance_reduction(self):
        bal = calculate_credit_card_balance(10000, 2, 5, 1)  # 1 month
        self.assertIsInstance(bal, float)
        self.assertLess(bal, 10000.0)

    def test_calculate_credit_card_balance_invalid_months(self):
        with self.assertRaises(ValueError):
            calculate_credit_card_balance(1000, 2, 5, 0)

    # Taxable income
    def test_calculate_taxable_income_normal(self):
        tax = calculate_taxable_income(100000, 50000, 5000)
        self.assertEqual(tax, 45000.0)

    def test_calculate_taxable_income_negative(self):
        with self.assertRaises(ValueError):
            calculate_taxable_income(-1000, 100, 50)

    # Budget planner
    def test_plan_budget_recommendation(self):
        rec = plan_budget(50000, 30000)
        self.assertEqual(rec["recommended_savings_percent"], 20.0)

    def test_plan_budget_zero_income(self):
        rec = plan_budget(0, 0)
        self.assertEqual(rec["recommended_savings_percent"], 0.0)

    # Net worth
    def test_calculate_net_worth_normal(self):
        nw = calculate_net_worth([100000, 50000], [20000])
        self.assertEqual(nw, 130000.0)

    def test_calculate_net_worth_negative_asset(self):
        with self.assertRaises(ValueError):
            calculate_net_worth([-100], [50])


if __name__ == "__main__":
    unittest.main()
