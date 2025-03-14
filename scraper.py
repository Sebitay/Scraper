import argparse
from playwright.sync_api import sync_playwright

# Step 1: Define your login credentials
EMAIL = "seba123612@gmail.com"
PASSWORD = "Seb@0811"

def open_easycancha_with_dynamic_date_and_hours(day, hours):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to True if you want headless mode
        context = browser.new_context()
        page = context.new_page()

        # Go to target URL
        target_url = "https://www.easycancha.com/book/clubs/59/sports/1/filter"
        page.goto(target_url)

        print("🌐 Page loaded. Checking for country selection modal...")

        # Step 2: Select Chile if necessary
        try:
            page.wait_for_selector("text=Chile", timeout=5000)
            page.click("text=Chile")
            print("✅ Chile selected!")
        except:
            print("⚠️ No country selection detected (or Chile auto-selected).")

        # Step 3: Dismiss instructions popup
        print("🕵️‍♂️ Checking for instructions popup...")
        try:
            page.wait_for_selector("text=OK", timeout=5000)
            page.click("text=OK")
            print("✅ Instructions popup dismissed!")
        except:
            print("⚠️ No instructions popup detected.")

        # Step 4: Login
        print("🔑 Attempting to login...")
        try:
            page.wait_for_selector('input[name="email"]', timeout=5000)
            page.fill('input[name="email"]', EMAIL)
            page.fill('input[name="password"]', PASSWORD)
            page.click('button:has-text("Ingresar")')
            print("✅ Login form submitted!")

            page.wait_for_selector("text=Siguiente", timeout=8000)
            print("🎉 Logged in successfully!")
        except Exception as e:
            print(f"❌ Error during login: {e}")

        # Step 5: Click on date provided as argument
        print(f'🗓️ Looking for the date "{day}"...')
        try:
            date_element = page.locator(f'div.cds-day:has(span.cds-day-number:has-text("{day}"))')
            date_element.click()
            print(f'✅ Clicked on date "{day}"!')
        except Exception as e:
            print(f'❌ Failed to click on date "{day}": {e}')
            browser.close()
            return  # Stop execution if date is not found

        # Step 6: Try clicking on the first available hour from the list
        print("⏰ Looking for preferred hours...")
        hour_clicked = False

        # Wait for previous hours to disappear
        page.wait_for_selector('div.hour_item', state='detached', timeout=10000)  # waits for previous ones to disappear

        # Wait for hours to be loaded to avoid searching too early
        page.wait_for_selector('div.hour_item', timeout=10000)  # Wait up to 10 seconds

        for hour in hours:
            print(f'🔍 Searching for hour: {hour}')
            try:
                # Locate visible hour_item containing the hour text
                hour_elements = page.locator(f'div.hour_item:has-text(" {hour} ")')

                count = hour_elements.count()
                print(f'🔢 Found {count} elements for hour {hour}')

                if count > 0:
                    hour_elements.nth(0).click()
                    print(f'✅ Clicked on available hour: {hour}')
                    hour_clicked = True
                    break  # Stop after clicking the first available hour
                else:
                    print(f'❌ Hour {hour} not found or not visible.')
            except Exception as e:
                print(f'❌ Error while searching for hour {hour}: {e}')

        if not hour_clicked:
            print("⚠️ No preferred hours were available to click.")

        print("🟢 Trying to click the 'Siguiente' button...")
        try:
            siguiente_button = page.locator('a.btn-success:has-text("Siguiente")')
            siguiente_button.click()
            print("✅ Clicked 'Siguiente' button successfully!")
        except Exception as e:
            print(f'❌ Error while clicking the "Siguiente" button: {e}')

        # Get all court-slug elements
        page.wait_for_selector('div.court-slug', timeout=10000) 
        court_elements = page.locator('div.court-slug')

        # Count how many courts are listed
        count = court_elements.count()
        print(f'ℹ️ Found {count} court elements.')

        # Loop through them
        clicked_court = False
        for i in range(count):
            court = court_elements.nth(i)
            # Find the nested title
            title = court.locator('div.court-slug-title').inner_text().strip().lower()
            print(f'➡️ Court {i + 1}: "{title}"')

            # If it does NOT contain "main court", click it
            if "main court" not in title:
                court.click()
                print(f'✅ Clicked on court: "{title}"')
                clicked_court = True
                break


        print("🟢 Trying to click the 'Reservar' button...")
        try:
            siguiente_button = page.locator('button.reserva_btn_terceary')
            siguiente_button.click()
            print("✅ Clicked 'Reservar' button successfully!")
        except Exception as e:
            print(f'❌ Error while clicking the "Reservar" button: {e}')

        # Optional pause to review visually
        input("✅ Process completed. Press Enter to close the browser...")

        # Close browser
        #browser.close()

# Argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EasyCancha Auto Date & Hour Selector")
    parser.add_argument('--d', type=str, required=True, help='Day of the month to select (e.g., 17)')
    parser.add_argument('--h', nargs='+', required=True, help='List of preferred hours, e.g., 08:00 09:00 10:00')
    args = parser.parse_args()

    open_easycancha_with_dynamic_date_and_hours(args.d, args.h)
