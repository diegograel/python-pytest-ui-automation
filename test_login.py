import pytest
import json
from playwright.sync_api import sync_playwright

# 1. Load the data from our JSON file
def load_test_data():
    with open('test_data.json') as f:
        return json.load(f)

# 2. The "Magic" - Parametrize tells Pytest to run this function 3 times
@pytest.mark.parametrize("data", load_test_data())
def test_login_scenarios(data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Set to True for GitHub/CI
        page = browser.new_page()
        
        # Navigate to a common practice login page
        page.goto("https://practicetestautomation.com/practice-test-login/")
        
        # Action: Type credentials
        page.fill("#username", data["username"])
        page.fill("#password", data["password"])
        page.click("#submit")
        
        # Validation: Check if we expect an error or a success message
        if data["expected_error"]:
            # We expect an error message to appear
            error_msg = page.locator("#error")
            assert error_msg.is_visible()
        else:
            # We expect a success URL or message
            assert "logged-in-successfully" in page.url
            
        browser.close()