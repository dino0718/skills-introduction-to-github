import csv
import os
from datetime import datetime


class ReportManager:
    """負責讀取測試計畫和生成報告"""
    def load_test_plan(self, file_path):
        abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"找不到測試計畫文件: {abs_path}")
        with open(abs_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def generate_report(self, test_results):
        base_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report")
        os.makedirs(base_directory, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name = f"report-{timestamp}.csv"
        file_path = os.path.join(base_directory, file_name)

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["item", "url", "response", "snapshot"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(test_results)
        print(f"測試報告已生成：{file_path}")
