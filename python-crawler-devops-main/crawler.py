import os


class SnapshotManager:
    """負責截圖管理"""
    def __init__(self, driver):
        self.driver = driver
        self.base_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
        os.makedirs(self.base_directory, exist_ok=True)

    def take_snapshot(self, path):
        full_path = os.path.join(self.base_directory, f"{path}.png")
        try:
            self.driver.save_screenshot(full_path)
            print(f"截圖已保存至：{full_path}")
            return os.path.join("screenshots", f"{path}.png")
        except Exception as e:
            print(f"截圖失敗：{e}")
            return "截圖失敗"
