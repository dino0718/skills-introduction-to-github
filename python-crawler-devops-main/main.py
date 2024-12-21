from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from req import APITestManager
from reports import ReportManager
from crawler import SnapshotManager
import os


class WebDriverManager:
    """管理 WebDriver 初始化與生命週期"""
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()


class TestAutomation:
    """自動化測試核心類別"""
    def __init__(self):
        self.driver_manager = WebDriverManager()
        self.driver = self.driver_manager.get_driver()
        self.snapshot_manager = SnapshotManager(self.driver)
        self.report_manager = ReportManager()
        self.api_manager = APITestManager()
        self.test_plan = []

    def setup_directories(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(os.path.join(base_dir, "screenshots"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "report"), exist_ok=True)

    def load_test_plan(self):
        try:
            self.test_plan = self.report_manager.load_test_plan("test_plan.csv")
            print("成功載入測試計畫")
        except Exception as e:
            print(f"讀取測試計畫時發生錯誤: {e}")
            self.driver_manager.quit()
            exit(1)

    def run_tests(self):
        test_results = []
        for index, plan in enumerate(self.test_plan):
            test_item = plan['item']
            test_url = plan['url']
            print(f"正在測試：{test_item}，URL：{test_url}")

            result = {
                "item": test_item,
                "url": test_url,
                "response": "",
                "snapshot": ""
            }

            try:
                self.driver.get(test_url)
                snapshot_name = f"{test_item}_{index}"
                result["snapshot"] = self.snapshot_manager.take_snapshot(snapshot_name)
                result["response"] = self.api_manager.run_api_test(test_url)
            except Exception as e:
                result["response"] = f"測試失敗：{e}"

            test_results.append(result)
        
        return test_results

    def generate_report(self, results):
        try:
            self.report_manager.generate_report(results)
            print("測試報告已生成")
        except Exception as e:
            print(f"生成測試報告時出錯: {e}")

    def run(self):
        self.setup_directories()
        self.load_test_plan()
        results = self.run_tests()
        self.generate_report(results)
        self.driver_manager.quit()


if __name__ == "__main__":
    automation = TestAutomation()
    automation.run()
