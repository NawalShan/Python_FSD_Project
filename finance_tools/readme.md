# Personal Finance Tools - Python Module + Django Integration (Minimal)

## Purpose
This repository provides:
 - `finance_tools.py`: 10 independent financial calculators (EMI, SIP, FD, RD, retirement estimator, home loan eligibility, credit card balance simulation, taxable income, budget planner, net worth).
 - `test_finance_tools.py`: unit tests using Python's `unittest`.
 - A minimal Django app scaffold demonstrating how to integrate `finance_tools`.

## Files
 - `finance_tools.py` - finance module
 - `test_finance_tools.py` - unit tests
 - `banking_project/` - (suggested) Django project scaffold (see instructions below)

## Requirements
 - Python 3.8+
 - Django (for web integration) (optional if only running the module)
 - (To run tests) no external libraries required.

## How to run tests
```bash
python -m unittest test_finance_tools.py
