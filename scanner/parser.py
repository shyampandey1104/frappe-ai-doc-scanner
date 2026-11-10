"""Vendor bill & receipt OCR parser for ERPNext."""

import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class InvoiceLineItem(BaseModel):
    item_name: str
    qty: float
    rate: float
    amount: float


class ExtractedInvoice(BaseModel):
    supplier_name: Optional[str] = None
    supplier_tax_id: Optional[str] = None  # GSTIN / VAT
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    grand_total: float = 0.0
    tax_amount: float = 0.0
    items: List[InvoiceLineItem] = []


class DocScannerEngine:
    """Parses raw text from OCR / PDF into structured ERPNext Purchase Invoice fields."""

    GSTIN_REGEX = r"\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}\b"
    INV_REGEX = r"(?:Invoice|Bill|Inv)[\s#:]*([A-Za-z0-9\/-]{3,20})"
    DATE_REGEX = r"\b(\d{1,2}[-\/.]\d{1,2}[-\/.]\d{2,4})\b"
    TOTAL_REGEX = r"(?:Total|Grand Total|Net Amount|Payable)[\s:₹$]*([0-9,]+\.[0-9]{2})"

    def parse_text(self, text: str) -> ExtractedInvoice:
        inv = ExtractedInvoice()

        # Extract Tax ID
        gst_match = re.search(self.GSTIN_REGEX, text)
        if gst_match:
            inv.supplier_tax_id = gst_match.group(0)

        # Extract Invoice Number
        inv_match = re.search(self.INV_REGEX, text, re.IGNORECASE)
        if inv_match:
            inv.invoice_number = inv_match.group(1).strip()

        # Extract Date
        date_match = re.search(self.DATE_REGEX, text)
        if date_match:
            inv.invoice_date = date_match.group(1)

        # Extract Grand Total
        tot_match = re.search(self.TOTAL_REGEX, text, re.IGNORECASE)
        if tot_match:
            val_clean = tot_match.group(1).replace(",", "")
            inv.grand_total = float(val_clean)

        # Basic line item detection heuristic
        for line in text.split("\n"):
            # Check pattern: ItemName ... Qty ... Rate ... Amount
            item_match = re.search(r"([A-Za-z0-9\s\-]+)\s+(\d+(?:\.\d+)?)\s+([0-9,]+\.[0-9]{2})\s+([0-9,]+\.[0-9]{2})", line)
            if item_match:
                name = item_match.group(1).strip()
                qty = float(item_match.group(2))
                rate = float(item_match.group(3).replace(",", ""))
                amt = float(item_match.group(4).replace(",", ""))
                inv.items.append(InvoiceLineItem(item_name=name, qty=qty, rate=rate, amount=amt))

        return inv
