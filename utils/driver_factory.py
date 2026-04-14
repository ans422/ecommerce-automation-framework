import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver() -> webdriver.Chrome:
    """
    Factory method to initialize and return a Chrome WebDriver instance.
    
    Automatically configures headless mode for CI environments (GitHub Actions)
    and optimizes browser settings for automation performance.
    
    Returns:
        webdriver.Chrome: A configured Selenium WebDriver instance.
    """
    options = Options()
    
    # Configure production-ready arguments
    if os.environ.get("CI") == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
    # Initialize Service with automatic driver management
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Finalize window setup
    driver.maximize_window()
    return driver
