import openai

def get_dynamic_css_selector(html_content, prompt):
    openai.api_key = "YOUR_OPENAI_API_KEY"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n\nHTML Content:\n{html_content}",
        max_tokens=100,
        temperature=0.3,
    )
    return response.choices[0].text.strip()

def extract_reviews_with_llm(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(page_url, wait_until='networkidle')

        # Pass the page content to OpenAI to identify CSS selectors
        html_content = page.content()
        review_selector = get_dynamic_css_selector(html_content, "Identify the CSS selector for reviews:")
        title_selector = get_dynamic_css_selector(html_content, "Identify the CSS selector for review titles:")
        body_selector = get_dynamic_css_selector(html_content, "Identify the CSS selector for review bodies:")
        rating_selector = get_dynamic_css_selector(html_content, "Identify the CSS selector for review ratings:")
        reviewer_selector = get_dynamic_css_selector(html_content, "Identify the CSS selector for reviewers:")

        reviews = []
        try:
            review_elements = page.query_selector_all(review_selector)
            for element in review_elements:
                title = element.query_selector(title_selector).inner_text() if element.query_selector(title_selector) else "N/A"
                body = element.query_selector(body_selector).inner_text() if element.query_selector(body_selector) else "N/A"
                rating = element.query_selector(rating_selector).inner_text() if element.query_selector(rating_selector) else "N/A"
                reviewer = element.query_selector(reviewer_selector).inner_text() if element.query_selector(reviewer_selector) else "N/A"

                reviews.append({
                    "title": title,
                    "body": body,
                    "rating": int(rating) if rating.isdigit() else 0,
                    "reviewer": reviewer
                })
        except Exception as e:
            print(f"Error with dynamic selectors: {e}")
        finally:
            browser.close()

        return reviews