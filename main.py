# main.py
from pos_ui import POSApp
from sales_report import get_sales_report
from db_manager import init_db
import sys
from PyQt5.QtWidgets import QApplication

def main():
    init_db()
    app = QApplication(sys.argv)
    pos = POSApp()

    # Display sales report for today's and yesterday's totals
    today_sales, yesterday_sales = get_sales_report()
    print(f"Today's Sales: ${today_sales}")
    print(f"Yesterday's Sales: ${yesterday_sales}")

    pos.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
