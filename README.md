# DOM Element Extractor Agent - Multi-Framework Support

A Python-based agent that operates in assist mode to navigate to URLs and extract DOM elements, then generates **raw scripts for ANY automation framework**.

## 🎯 Features

- **Assist Mode**: Simple interface - just provide a URL
- **Automatic Navigation**: Navigates to the provided URL using Selenium WebDriver
- **Complete DOM Extraction**: Extracts all interactive elements from the page
- **Multi-Framework Support**: Generates ready-to-use scripts for:
  - ✅ **Selenium** (Python)
  - ✅ **Playwright** (Python)
  - ✅ **Puppeteer** (JavaScript)
  - ✅ **Cypress** (JavaScript)
  - ✅ **Robot Framework**
  - ✅ **Raw Element Locators** (Framework-agnostic)
- **Multiple Locator Strategies**: XPath, CSS Selectors, ID, Name, Class
- **JSON Export**: Structured data for custom integrations

## 📦 Installation

### Prerequisites

1. **Python 3.8+** installed
2. **Google Chrome** browser installed
3. **ChromeDriver** (managed automatically)

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent
python dom_extractor_agent.py
```

## 🚀 Usage

### Basic Usage

Simply run the script and provide a URL:

```bash
python dom_extractor_agent.py
```

**Example Session:**

```
============================================================
DOM ELEMENT EXTRACTOR AGENT - ASSIST MODE
============================================================

Enter URL to analyze: example.com

→ Navigating to: https://example.com
✓ Successfully loaded: Example Domain

→ Extracting interactive elements...
✓ Found 45 interactive elements

→ Generating framework-specific scripts...
  ✓ RAW_ELEMENTS: raw_elements_20250127_143052.txt
  ✓ SELENIUM: selenium_script_20250127_143052.py
  ✓ PLAYWRIGHT: playwright_script_20250127_143052.py
  ✓ PUPPETEER: puppeteer_script_20250127_143052.js
  ✓ CYPRESS: cypress_script_20250127_143052.js
  ✓ ROBOT_FRAMEWORK: robot_framework_script_20250127_143052.robot
```

## 📄 Generated Files

The agent generates **7 files** for each URL:

### 1. Raw Element Locators (Framework-Agnostic)
```
ID = 'submit-btn'
XPATH = '/html/body/div[1]/form/button'
CSS = 'button#submit-btn'
```

### 2. Selenium Script
```python
driver.find_element(By.ID, 'submit-btn').click()
```

### 3. Playwright Script
```python
page.locator('#submit-btn').click()
```

### 4. Puppeteer Script
```javascript
await page.click('#submit-btn');
```

### 5. Cypress Script
```javascript
cy.get('#submit-btn').click();
```

### 6. Robot Framework Script
```robot
Click Element    ${ELEMENT_1}
```

### 7. JSON Data
```json
{"id": "submit-btn", "xpath": "...", "css": "..."}
```

## 🎯 Use Cases

1. **Quick Test Automation** - Start automating immediately
2. **Framework Migration** - Easily switch between frameworks
3. **Cross-Framework Testing** - Compare different frameworks
4. **Web Scraping** - Get all element locators
5. **Learning** - See how different frameworks work

## 🔧 Advanced Usage

### Programmatic Usage

```python
from dom_extractor_agent import DOMExtractorAgent

agent = DOMExtractorAgent()
agent.navigate_to_url("https://example.com")
elements = agent.extract_interactive_elements()

# Generate for specific framework
scripts = agent.generate_raw_script(elements, framework='selenium')

# Or all frameworks
all_scripts = agent.generate_raw_script(elements, framework='all')

agent.save_results(elements)
agent.cleanup()
```

## 📝 License

Free to use and modify for your projects.
