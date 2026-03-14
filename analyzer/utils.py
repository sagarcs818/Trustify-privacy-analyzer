# analyzer/utils.py
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def fetch_privacy_policy(url: str) -> str:
    """
    Fetches privacy policy using an invincible 4-Engine setup.
    Engine 1: Jina AI (Bypasses 99% of Cloudflare/Meta blockers, renders JS)
    Engine 2: Requests (Fast fallback for basic sites)
    Engine 3: Playwright (Local rendering with stealth mode)
    Engine 4: Archive.org (The ultimate Wayback Machine fallback)
    """
    print(f"\n[Scraper] Attempting to fetch: {url}")
    
    # --- ENGINE 1: Jina AI Proxy (The Magic Bullet) ---
    print("[Scraper] Firing Engine 1 (Jina AI Reader)...")
    text = _fetch_with_jina(url)
    if text and len(text) > 300:
        print("[Scraper] Success! Fetched using Engine 1 (Jina).")
        return text

    # --- ENGINE 2: Direct Requests ---
    print("[Scraper] Engine 1 blocked. Firing Engine 2 (Direct Requests)...")
    text = _fetch_with_requests(url)
    if text and len(text) > 300:
        print("[Scraper] Success! Fetched using Engine 2 (Requests).")
        return text
    
    # --- ENGINE 3: Playwright (With Stealth) ---
    print("[Scraper] Engine 2 failed. Firing Engine 3 (Playwright Stealth)...")
    text = _fetch_with_playwright(url)
    if text and len(text) > 300:
        print("[Scraper] Success! Fetched using Engine 3 (Playwright).")
        return text
        
    # --- ENGINE 4: Archive.org ---
    print("[Scraper] Engine 3 blocked. Firing Engine 4 (Archive.org Fallback)...")
    text = _fetch_with_archive(url)
    if text and len(text) > 300:
        print("[Scraper] Success! Fetched using Engine 4 (Archive).")
        return text

    print(f"[Scraper] Failed to extract meaningful text from {url}. All 4 engines blocked.")
    return None


def _fetch_with_jina(url: str) -> str:
    """Uses the free Jina AI Reader to bypass JS traps and extract raw markdown."""
    try:
        headers = {"Accept": "text/plain", "User-Agent": USER_AGENT}
        jina_url = f"https://r.jina.ai/{url}"
        response = requests.get(jina_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            text = response.text
            # Ensure we didn't just scrape a Cloudflare CAPTCHA page
            if "Just a moment..." not in text and "Access Denied" not in text:
                return text
    except Exception as e:
        print(f"[Jina Error] {e}")
    return None


def _clean_html(html: str) -> str:
    """Cleans raw HTML if fetched via standard means."""
    if not html: 
        return None
    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "svg", "button", "form", "meta", "link", "iframe"]):
        element.extract()
    full_text = soup.get_text(separator="\n", strip=True)
    return full_text if len(full_text) > 200 else None


def _fetch_with_requests(url: str) -> str:
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            text = _clean_html(response.text)
            if text and "enable JavaScript" not in text and "Access Denied" not in text:
                return text
    except Exception as e:
        print(f"[Requests Error] {e}")
    return None


def _fetch_with_playwright(url: str) -> str:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent=USER_AGENT,
                viewport={"width": 1920, "height": 1080}
            )
            
            # STEALTH MODE: Hides the fact that it's a bot from basic JS firewalls
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            page = context.new_page()
            page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"] else route.continue_())
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            
            # Wait for content to render
            page.wait_for_timeout(3000) 
            
            html = page.content()
            browser.close()
            
            text = _clean_html(html)
            if text and "enable JavaScript" not in text:
                return text
    except Exception as e:
        print(f"[Playwright Error] {e}")
    return None


def _fetch_with_archive(url: str) -> str:
    """Uses the Internet Archive to bypass enterprise firewalls as a last resort."""
    archive_url = f"https://web.archive.org/web/20240101000000/{url}"
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(archive_url, headers=headers, timeout=15)
        if response.status_code == 200:
            text = _clean_html(response.text)
            if text and "enable JavaScript" not in text:
                return text
    except Exception as e:
        print(f"[Archive Error] {e}")
    return None