from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize Selenium WebDriver
driver = webdriver.Chrome()  # Visible browser instance
base_url = "https://guestpostlinks.net/sites/"
output_file = "websites_links.csv"

# Function to scrape website URLs from the <td> elements
def scrape_links(wait, f):
    try:
        # Find all <td> elements containing the website links
        td_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.col-website_url a.website"))
        )
        
        for td in td_elements:
            # Extract the href attribute (website link)
            link = td.get_attribute("href")
            if link:
                f.write(link + "\n")
    except Exception as e:
        print(f"Error scraping links: {e}")

# Open file to save links
with open(output_file, "w") as f:
    f.write("Website Links\n")  # Header for the file

    driver.get(base_url)
    wait = WebDriverWait(driver, 30)

    for page in range(1, 324):  # Loop through all 323 pages
        print(f"Processing page {page}...")

        # Scrape website links from the current page
        scrape_links(wait, f)

        # Click the next pagination button
        try:
            next_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//a[contains(@class, 'paginate_button') and text()='{page + 1}']")
                )
            )
            next_button.click()
            print(f"Clicked on page {page + 1}. Waiting for data to load...")
            time.sleep(15)  # Wait for the data to load
        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            break

# Close the browser
driver.quit()
print("Scraping complete. Links saved to", output_file)
