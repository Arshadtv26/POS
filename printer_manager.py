# printer_manager.py
from escpos.printer import Usb

def print_invoice(invoice_id):
    p = Usb(0x04b8, 0x0e15)  # Use your printer's vendor/product IDs
    p.text(f"Invoice ID: {invoice_id}\n")
    # Print other invoice details as needed
    p.cut()
