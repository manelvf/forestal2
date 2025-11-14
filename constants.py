# -*- coding: utf-8 -*-
"""
Application constants for Forestal2 project
"""

# Company Types
class CompanyTypes:
    TRANSPORT = "Transporte"
    PARTICULAR = "Particular"

# Pagination Defaults
class PaginationDefaults:
    PAGE_SIZE = 15
    MAX_PAGE_SIZE = 1000
    MIN_PAGE_SIZE = 1

# Deed Types
class DeedTypes:
    COMPRAVENTA = 1
    HERDANZA = 2

# Grid Search Operators
GRID_SEARCH_OPERATORS = {
    'eq': '',           # equals
    'ne': 'ne',        # not equal
    'lt': 'lt',        # less than
    'le': 'lte',       # less than or equal
    'gt': 'gt',        # greater than
    'ge': 'gte',       # greater than or equal
    'bw': 'startswith',  # begins with
    'bn': 'startswith',  # doesn't begin with (negated)
    'ew': 'endswith',    # ends with
    'en': 'endswith',    # doesn't end with (negated)
    'cn': 'contains',    # contains
    'nc': 'contains',    # doesn't contain (negated)
}

# Sort Orders
SORT_ORDERS = ['asc', 'desc']

# Backup Configuration
BACKUP_RETENTION_DAYS = 7
