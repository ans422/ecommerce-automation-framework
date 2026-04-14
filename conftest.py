import pytest
from utils.driver_factory import get_driver

@pytest.fixture(scope="function")
def driver():
    """Provides a WebDriver instance to a test."""
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()
