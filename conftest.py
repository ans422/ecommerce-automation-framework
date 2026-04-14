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
                    <a href="#portfolio-summary">Report Summary</a>
                    <a href="#results-table">Detailed Results</a>
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
        
        // 3. Professional Summary to Table Transformation
        const summaryData = document.querySelector(".summary__data");
        if (summaryData) {
            const summaryContainer = document.querySelector(".summary");
            if (summaryContainer) summaryContainer.id = "portfolio-summary";
            
            // Extract all status spans
            const spans = Array.from(summaryData.querySelectorAll("span"));
            if (spans.length > 0) {
                const table = document.createElement("table");
                table.className = "summary-table";
                table.id = "summary-results-table";
                
                let rowsHTML = "";
                
                // 1. Process main summary text (usually first span or textNode)
                const mainText = summaryData.innerText || summaryData.textContent;
                const timeMatch = mainText.match(/(\d+\.?\d*)\s*(seconds|minutes|s|m)/i);
                const countMatch = mainText.match(/(\d+)\s*tests/i);

                if (countMatch) {
                    rowsHTML += `<tr><td>TOTAL TESTS</td><td class="count-cell">${countMatch[1]}</td></tr>`;
                }
                if (timeMatch) {
                    rowsHTML += `<tr><td>TOTAL RUNTIME</td><td class="count-cell">${timeMatch[1]} ${timeMatch[2]}</td></tr>`;
                }

                // 2. Process status breakdowns
                spans.forEach(span => {
                    const statusText = span.innerText || span.textContent;
                    // Look for patterns like "5 passed", "1 failed" etc
                    const parts = statusText.trim().split(/\s+/);
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
                    table.innerHTML = `
                        <thead>
                            <tr>
                                <th>Test Metric</th>
                                <th>Value / Count</th>
                            </tr>
                        </thead>
                        <tbody>${rowsHTML}</tbody>
                    `;
                    
                    // Transform UI and Inject Heading + Table
                    summaryContainer.innerHTML = `
                        <h2 class="report-summary-heading">Report Summary</h2>
                        ${table.outerHTML}
                    `;
                }
            }
        }

        // 4. Setup Portfolio Footer
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
