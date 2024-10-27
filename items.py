import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem

# Database connection settings
db_config = {
    'user': 'root',
    'password': 'Inoa2602@',
    'host': 'localhost',
    'database': 'POS'
}

class ItemManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POS - Item Manager")
        self.setGeometry(200, 200, 400, 300)
        self.db_connection = mysql.connector.connect(**db_config)
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout()

        # Fields for item details
        self.item_name_input = QLineEdit(self)
        self.item_name_input.setPlaceholderText("Item Name")
        layout.addWidget(QLabel("Item Name:"))
        layout.addWidget(self.item_name_input)

        self.item_price_input = QLineEdit(self)
        self.item_price_input.setPlaceholderText("Item Price")
        layout.addWidget(QLabel("Item Price:"))
        layout.addWidget(self.item_price_input)

        self.item_quantity_input = QLineEdit(self)
        self.item_quantity_input.setPlaceholderText("Item Quantity")
        layout.addWidget(QLabel("Item Quantity:"))
        layout.addWidget(self.item_quantity_input)

        self.item_description_input = QLineEdit(self)
        self.item_description_input.setPlaceholderText("Item Description")
        layout.addWidget(QLabel("Item Description:"))
        layout.addWidget(self.item_description_input)

        # Buttons for Add and Delete
        self.add_button = QPushButton("Add Item", self)
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Item", self)
        self.delete_button.clicked.connect(self.delete_item)
        layout.addWidget(self.delete_button)

        # Table for displaying items
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Item ID", "Name", "Price", "Quantity"])
        layout.addWidget(self.table)
        self.load_items()

        self.setLayout(layout)

    def add_item(self):
        name = self.item_name_input.text()
        price = self.item_price_input.text()
        quantity = self.item_quantity_input.text()
        description = self.item_description_input.text()

        try:
            cursor = self.db_connection.cursor()
            query = "INSERT INTO items (item_name, item_price, item_quantity, item_description) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, float(price), int(quantity), description))
            self.db_connection.commit()
            cursor.close()
            QMessageBox.information(self, "Success", "Item added successfully!")
            self.clear_inputs()
            self.load_items()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add item: {e}")

    def delete_item(self):
        selected = self.table.currentRow()
        if selected >= 0:
            item_id = self.table.item(selected, 0).text()
            try:
                cursor = self.db_connection.cursor()
                query = "DELETE FROM items WHERE item_id = %s"
                cursor.execute(query, (item_id,))
                self.db_connection.commit()
                cursor.close()
                QMessageBox.information(self, "Success", "Item deleted successfully!")
                self.load_items()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete item: {e}")
        else:
            QMessageBox.warning(self, "Error", "No item selected")

    def load_items(self):
        self.table.setRowCount(0)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT item_id, item_name, item_price, item_quantity FROM items")
        for row, form in enumerate(cursor.fetchall()):
            self.table.insertRow(row)
            for column, data in enumerate(form):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))
        cursor.close()

    def clear_inputs(self):
        self.item_name_input.clear()
        self.item_price_input.clear()
        self.item_quantity_input.clear()
        self.item_description_input.clear()

    def closeEvent(self, event):
        self.db_connection.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemManager()
    window.show()
    sys.exit(app.exec_())
