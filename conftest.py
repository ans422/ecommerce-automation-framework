import pytest
from utils.driver_factory import get_driver

@pytest.fixture(scope="function")
def driver():
    """Provides a WebDriver instance to a test."""
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()

def pytest_html_results_summary(prefix, summary, postfix, session):
    """Injects a professional header and footer into the test report's DOM using Javascript."""
    js_payload = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        const body = document.body;
        
        // 1. Setup Portfolio Header
        const header = document.createElement("header");
        header.className = "portfolio-header";
        header.innerHTML = `
            <div class="header-container">
                <div class="header-logo"><span class="code-bracket">&lt;/&gt;</span> ANS422 <span>Automation Portfolio</span></div>
                <nav class="header-nav">
                    <a href="https://github.com/ans422/ecommerce-automation-framework" target="_blank">GitHub Repo</a>
                    <a href="#">Report Summary</a>
                </nav>
            </div>
        `;
        body.insertBefore(header, body.firstChild);
        
        // 2. Wrap existing contents in <main>
        const main = document.createElement("main");
        main.className = "portfolio-main";
        // Grab all children except our newly injected header
        const children = Array.from(body.childNodes);
        children.forEach(child => {
            if(child !== header && child.tagName !== 'SCRIPT') {
                main.appendChild(child);
            }
        });
        body.appendChild(main);
        
        // 3. Setup Portfolio Footer
        const footer = document.createElement("footer");
        footer.className = "portfolio-footer";
        footer.innerHTML = `
            <div class="footer-container">
                <p>Designed for professional automation excellence. &copy; ${new Date().getFullYear()}</p>
                <div class="footer-tech">Powered by Pytest &#9889; Selenium &#9889; GitHub Actions</div>
            </div>
        `;
        body.appendChild(footer);
    });
    </script>
    """
    prefix.append(js_payload)
