"""
AI Auto Repair Package
=======================
Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from .engine import (
    AutoRepairEngine,
    IssueType,
    get_repair_engine,
    diagnose_and_repair
)

__all__ = [
    'AutoRepairEngine',
    'IssueType',
    'get_repair_engine',
    'diagnose_and_repair'
]
