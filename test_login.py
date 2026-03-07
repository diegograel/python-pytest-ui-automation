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
            error_banner = page.locator("#error")
            assert error_banner.is_visible(), "FAIL: Error banner did not appear."
    
    # EXACT MATCH CHECK
            actual_message = error_banner.inner_text()
            assert actual_message == data["expected_message"], \
            f"FAIL: Wrong error message shown! Expected: '{data['expected_message']}', but got: '{actual_message}'"
        else:
    # Check the header on the success page
            success_header = page.locator("h1.post-title")
            assert success_header.inner_text() == data["expected_message"]
            
        browser.close()

# --- Your existing load_test_data and login test remain at the top ---

def test_user_logout():
    """Test 3: Verify the logout functionality works for a valid user"""
    # 1. Manually get the valid user from our JSON list
    all_data = load_test_data()
    valid_user = all_data[0] # Grabs the first entry ("student")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 2. Perform Login first
        page.goto("https://practicetestautomation.com/practice-test-login/")
        page.fill("#username", valid_user["username"])
        page.fill("#password", valid_user["password"])
        page.click("#submit")
        
        # 3. Click the 'Log out' button
        logout_button = page.get_by_role("link", name="Log out")
        logout_button.wait_for(state="visible")
        logout_button.click()
        
        # 4. ASSERTION: Verify we are back on the login page
        # We check the URL and that the 'submit' button is visible again
        assert "/practice-test-login/" in page.url
        assert page.locator("#submit").is_visible(), "FAIL: Login button not visible after logout"
        
        browser.close()