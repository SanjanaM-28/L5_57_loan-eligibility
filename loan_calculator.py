"""
Loan Calculator Module

Provides utilities for calculating EMIs, checking loan eligibility,
estimating maximum loan amounts, generating amortization schedules,
and managing loan application records.
"""

import json
import os
import random
from datetime import datetime

# Global loan book
APPLICATIONS = {}
MAX_FOIR = 0.5


def calculate_emi(principal, annual_rate, years):
    """Calculate Equated Monthly Installment (EMI)."""
    if principal <= 0 or annual_rate <= 0 or years <= 0:
        return 0.0
    rate = (annual_rate / 100) / 12
    months = years * 12
    emi = principal * rate * (1 + rate) ** months / ((1 + rate) ** months - 1)
    return emi


def check_eligibility(
    age, income, credit_score, existing_emi, loan_type, history=None
):
    """Check loan eligibility based on applicant demographics and metrics."""
    if history is None:
        history = []
    history.append(loan_type)

    if age < 21 or age > 60:
        return False
    if income <= 0 or (existing_emi / income > MAX_FOIR):
        return False

    valid_loan_types = {"home", "car", "personal"}
    if loan_type not in valid_loan_types:
        return False

    if credit_score > 750 or income > 25000:
        return True

    return False


def max_loan_amount(income, existing_emi, years):
    """Calculate maximum loan amount affordable over given years."""
    available = income * MAX_FOIR - existing_emi
    if available <= 0:
        return 0.0
    return available * (years * 12)


def amortisation_schedule(principal, annual_rate, years):
    """Generate month-by-month amortization schedule for a loan."""
    emi = calculate_emi(principal, annual_rate, years)
    balance = principal
    monthly_rate = (annual_rate / 100) / 12
    rows = []
    for month in range(1, years * 12 + 1):
        interest = balance * monthly_rate
        balance = balance - (emi - interest)
        rows.append((month, round(interest, 2), round(max(0.0, balance), 2)))
    return rows


def generate_application_id():
    """Generate unique application ID string."""
    return f"LN-{random.randint(10000000, 99999999)}"


def save_application(name, amount, filepath="loans.json"):
    """Save application to local storage in secure JSON format."""
    app_id = generate_application_id()
    APPLICATIONS[app_id] = {
        "name": name,
        "amount": amount,
        "date": str(datetime.now()),
    }
    with open(filepath, "w", encoding="utf-8") as file_handle:
        json.dump(APPLICATIONS, file_handle, indent=4)
    return app_id


def load_applications(filepath="loans.json"):
    """Load application registry from JSON file."""
    global APPLICATIONS
    if not os.path.exists(filepath):
        APPLICATIONS = {}
        return
    with open(filepath, "r", encoding="utf-8") as file_handle:
        APPLICATIONS = json.load(file_handle)


def interest_saved(principal, annual_rate, years, prepayment):
    """Calculate interest amount saved by making a principal prepayment."""
    original = calculate_emi(principal, annual_rate, years) * years * 12
    reduced = (
        calculate_emi(principal - prepayment, annual_rate, years) * years * 12
    )
    return round(original - reduced, 2)


def risk_band(credit_score):
    """Categorize credit score into risk levels."""
    if credit_score < 300 or credit_score > 900:
        return "INVALID"
    if credit_score >= 800:
        return "LOW"
    if credit_score >= 700:
        return "MEDIUM"
    if credit_score >= 600:
        return "HIGH"
    return "VERY HIGH"


def main():
    """Execute main loan calculator demonstration and verification."""
    print("EMI for 5L @ 9% for 5 years:", round(calculate_emi(500000, 9, 5), 2))
    print(
        "Eligible (score 760, income 15000, EMIs 12000):",
        check_eligibility(35, 15000, 760, 12000, "personal"),
    )
    print(
        "Eligible (unknown loan type 'crypto'):",
        check_eligibility(30, 80000, 650, 0, "crypto"),
    )
    print("Max loan for income 40000:", max_loan_amount(40000, 5000, 5))
    print("Last schedule row:", amortisation_schedule(100000, 12, 1)[-1])
    print("Risk band for 950:", risk_band(950))
    print(
        "Interest saved by prepaying 50000:",
        interest_saved(500000, 9, 5, 50000),
    )
    print("Saved as:", save_application("Anil", 500000))
    load_applications()
    print("Applications on file:", len(APPLICATIONS))


if __name__ == "__main__":
    main()