from playwright.sync_api import sync_playwright

def extract_reviews(page_url):
    reviews = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(page_url, wait_until='networkidle')  # Ensure the page is fully loaded

            # Handle if reviews are inside an iframe
            iframes = page.frames
            for frame in iframes:
                if "reviews" in frame.url:
                    page = frame  # Switch to the frame containing reviews
                    break

            # Extract review elements
            review_elements = page.query_selector_all('.review-class')  # Replace with actual selector
            for element in review_elements:
                title = element.query_selector('.title-class').inner_text() if element.query_selector('.title-class') else "N/A"
                body = element.query_selector('.body-class').inner_text() if element.query_selector('.body-class') else "N/A"
                rating = element.query_selector('.rating-class').inner_text() if element.query_selector('.rating-class') else "N/A"
                reviewer = element.query_selector('.reviewer-class').inner_text() if element.query_selector('.reviewer-class') else "N/A"

                reviews.append({
                    "title": title,
                    "body": body,
                    "rating": int(rating) if rating.isdigit() else 0,
                    "reviewer": reviewer
                })

            # Handle pagination
            while True:
                next_button = page.query_selector('.next-button-class')  # Replace with actual selector
                if next_button and next_button.is_visible():
                    next_button.click()
                    page.wait_for_timeout(2000)  # Wait for the next page to load
                    review_elements = page.query_selector_all('.review-class')  # Replace with actual selector
                    for element in review_elements:
                        title = element.query_selector('.title-class').inner_text() if element.query_selector('.title-class') else "N/A"
                        body = element.query_selector('.body-class').inner_text() if element.query_selector('.body-class') else "N/A"
                        rating = element.query_selector('.rating-class').inner_text() if element.query_selector('.rating-class') else "N/A"
                        reviewer = element.query_selector('.reviewer-class').inner_text() if element.query_selector('.reviewer-class') else "N/A"

                        reviews.append({
                            "title": title,
                            "body": body,
                            "rating": int(rating) if rating.isdigit() else 0,
                            "reviewer": reviewer
                        })
                else:
                    break

        except Exception as e:
            print(f"Error extracting reviews: {e}")
        finally:
            browser.close()

    return reviews