"""
Enum for department types.
"""
from enum import Enum

class Department(Enum):
    IT = 'IT'
    HR = 'HR'
    MARKETING = 'Marketing'
    SALES = 'Sales'
    FINANCE = 'Finance'
    LEGAL = 'Legal'
    OTHER = 'Other'
