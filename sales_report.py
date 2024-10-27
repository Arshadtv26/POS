# sales_report.py
import mysql.connector
from datetime import datetime, timedelta
from db_manager import db_config

def get_sales_report():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Today's sales
    today = datetime.now().date()
    cursor.execute("SELECT SUM(total) FROM invoices WHERE DATE(timestamp) = %s", (today,))
    today_sales = cursor.fetchone()[0] or 0

    # Yesterday's sales
    yesterday = today - timedelta(days=1)
    cursor.execute("SELECT SUM(total) FROM invoices WHERE DATE(timestamp) = %s", (yesterday,))
    yesterday_sales = cursor.fetchone()[0] or 0

    conn.close()
    return today_sales, yesterday_sales
