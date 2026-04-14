import pytest
from typing import List, Generator
from utils.driver_factory import get_driver

@pytest.fixture(scope="function")
def driver() -> Generator:
    """Provides a fresh WebDriver instance for each test function."""
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()

def pytest_html_results_summary(prefix: List[str], summary, postfix: List[str], session: pytest.Session) -> None:
    """Injects a high-fidelity dashboard UI and DOM transformations into the HTML report."""
    
    js_payload = """
    <script>
    /**
     * Professional Automation Dashboard - DOM Transformation Logic
     * Responsibilities: Header/Footer injection, Summary Table conversion, Navigation setup.
     */
    (function() {
        document.addEventListener("DOMContentLoaded", () => {
            const body = document.body;
            
            // 1. Initialize UI Helper Functions
            const createEl = (tag, className, html = '') => {
                const el = document.createElement(tag);
                if (className) el.className = className;
                if (html) el.innerHTML = html;
                return el;
            };

            // 2. Setup Dashboard Header
            const header = createEl("header", "portfolio-header", `
                <div class="header-container">
                    <div class="header-logo">
                        <span class="code-bracket">&lt;/&gt;</span> ANS422 <span>Automation Portfolio</span>
                    </div>
                    <nav class="header-nav">
                        <a href="https://github.com/ans422/ecommerce-automation-framework" target="_blank">GitHub Repo</a>
                        <a href="#portfolio-summary">Report Summary</a>
                        <a href="#results-table">Detailed Results</a>
                    </nav>
                </div>
            `);
            body.insertBefore(header, body.firstChild);
            
            // 3. Encapsulate Main Content
            const main = createEl("main", "portfolio-main");
            Array.from(body.childNodes).forEach(node => {
                if(node !== header && node.tagName !== 'SCRIPT') {
                    main.appendChild(node);
                }
            });
            body.appendChild(main);
            
            // 4. Robust Summary Table Transformation
            const summaryData = document.querySelector(".summary__data");
            if (summaryData) {
                const summaryContainer = document.querySelector(".summary");
                if (summaryContainer) summaryContainer.id = "portfolio-summary";
                
                const spans = Array.from(summaryData.querySelectorAll("span"));
                if (spans.length > 0) {
                    const table = createEl("table", "summary-table");
                    table.id = "summary-results-table";
                    
                    let rowsHTML = "";
                    const fullText = summaryData.innerText || summaryData.textContent;
                    
                    // Extract Global Metrics
                    const tMatch = fullText.match(/(\d+\.?\d*)\s*(seconds|minutes|s|m)/i);
                    const cMatch = fullText.match(/(\d+)\s*tests/i);

                    if (cMatch) rowsHTML += `<tr><td>TOTAL TESTS</td><td class="count-cell">${cMatch[1]}</td></tr>`;
                    if (tMatch) rowsHTML += `<tr><td>TOTAL RUNTIME</td><td class="count-cell">${tMatch[1]} ${tMatch[2]}</td></tr>`;

                    // Extract Status Breakdowns
                    spans.forEach(span => {
                        const text = span.innerText || span.textContent;
                        const parts = text.trim().split(/\s+/);
                        if (parts.length >= 2 && !isNaN(parts[0])) {
                            const count = parts[0];
                            const label = parts.slice(1).join(" ").replace(/[\(\),]/g, "").trim();
                            if (label.toLowerCase() !== "tests") {
                                rowsHTML += `
                                    <tr class="${span.className}">
                                        <td>${label.toUpperCase()}</td>
                                        <td class="count-cell">${count}</td>
                                    </tr>
                                `;
                            }
                        }
                    });

                    if (rowsHTML) {
                        table.innerHTML = `<thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>${rowsHTML}</tbody>`;
                        summaryContainer.innerHTML = `
                            <h2 class="report-summary-heading">Report Summary</h2>
                            ${table.outerHTML}
                        `;
                    }
                }
            }

            // 5. Setup Dashboard Footer
            const footer = createEl("footer", "portfolio-footer", `
                <div class="footer-container">
                    <p>Designed for professional automation excellence. &copy; ${new Date().getFullYear()}</p>
                    <div class="footer-tech">Powered by Pytest &#9889; Selenium &#9889; GitHub Actions</div>
                </div>
            `);
            body.appendChild(footer);
        });
    })();
    </script>
    """
    prefix.append(js_payload)
