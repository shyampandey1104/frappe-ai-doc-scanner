"""Converts extracted OCR data into ERPNext Purchase Invoice payload."""

from typing import Dict, Any
from scanner.parser import ExtractedInvoice


class ERPNextBridge:
    @staticmethod
    def to_purchase_invoice_payload(extracted: ExtractedInvoice, default_supplier: str = "Vendor - Standard") -> Dict[str, Any]:
        return {
            "doctype": "Purchase Invoice",
            "supplier": extracted.supplier_name or default_supplier,
            "bill_no": extracted.invoice_number,
            "bill_date": extracted.invoice_date,
            "items": [
                {
                    "item_name": item.item_name,
                    "qty": item.qty,
                    "rate": item.rate,
                    "amount": item.amount,
                }
                for item in extracted.items
            ],
        }
