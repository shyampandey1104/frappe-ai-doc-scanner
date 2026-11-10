"""Unit tests for DocScannerEngine."""

from scanner.parser import DocScannerEngine


def test_ocr_text_extraction():
    sample_ocr = """
    TAX INVOICE
    Supplier: Acme Industrial Supplies
    GSTIN: 27AABCA1234F1Z5
    Invoice # INV-2026-9042
    Date: 04/11/2026

    Description       Qty   Rate     Amount
    Steel Fasteners   50    120.00   6000.00
    Hexagon Nuts      100   25.00    2500.00

    Grand Total: ₹8,500.00
    """
    engine = DocScannerEngine()
    inv = engine.parse_text(sample_ocr)

    assert inv.supplier_tax_id == "27AABCA1234F1Z5"
    assert inv.invoice_number == "INV-2026-9042"
    assert inv.grand_total == 8500.0
    assert len(inv.items) == 2
