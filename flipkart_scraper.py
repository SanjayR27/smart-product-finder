from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open Flipkart
driver.get("https://www.flipkart.com")

# Optional: Close the login pop-up if it appears
try:
    login_popup_close = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="✕"]'))
    )
    login_popup_close.click()
    print("Login popup closed.")
except Exception as e:
    print("No login popup found.")

# Wait for the page to load fully and the product grid to be present
try:
    # Wait for the first product grid element to load (specific CSS selector)
    product_grid = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div._1AtVbE'))
    )
    print("Product grid loaded successfully.")
except Exception as e:
    print("❌ Failed to detect product grid. Trying alternative method.")

    # Attempt scrolling to load more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Allow time for AJAX loading

    # Retry to locate the product grid
    try:
        product_grid = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div._1AtVbE'))
        )
        print("Product grid loaded after scroll.")
    except Exception as e:
        print("❌ Failed again to detect the product grid.")

# Try locating the products in a specific product container after grid loads
try:
    product_containers = driver.find_elements(By.CSS_SELECTOR, 'div._1AtVbE')
    if len(product_containers) > 0:
        print(f"Found {len(product_containers)} product(s).")
    else:
        print("❌ No products found.")
except Exception as e:
    print("❌ Error while fetching product containers.")

# Check if iframe exists and switch to it if necessary
try:
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    print("Switched to iframe.")
except Exception as e:
    print("No iframe detected.")

# Continue with further scraping logic...
# (Add scraping code here for extracting product details)

# Close the browser after scraping
driver.quit()
