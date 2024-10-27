# pos_ui.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from db_manager import save_invoice,get_item_data

class POSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POS Billing System")
        self.current_quantity = 1
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel(f"Quantity: {self.current_quantity}")
        layout.addWidget(self.label)
        items = get_item_data()
        # Add item buttons
        # for item_name, price in [("Item 1", 10), ("Item 2", 15),("Item 3", 15),("Item 4", 15), ("Item 5", 15),("Item 6", 15)]:
        for item_name, item_price in items:
            button = QPushButton(f"{item_name} - ${item_price}")
            button.clicked.connect(lambda _, name=item_name, p=item_price: self.add_item(name, p))
            layout.addWidget(button)

        self.setLayout(layout)

    def add_item(self, item_name, price):
        save_invoice(item_name, self.current_quantity, price)
        print(f"Added {self.current_quantity} of {item_name} at ${price} each")

    def increase_quantity(self):
        self.current_quantity += 1
        self.label.setText(f"Quantity: {self.current_quantity}")

    def decrease_quantity(self):
        if self.current_quantity > 1:
            self.current_quantity -= 1
            self.label.setText(f"Quantity: {self.current_quantity}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pos = POSApp()
    pos.show()
    sys.exit(app.exec_())
