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

1. **Python 3.8+** (including Python 3.11 and 3.12)
2. **Google Chrome** browser installed
3. **ChromeDriver** (managed automatically by webdriver-manager)

### Setup

#### Option 1: Install as a Package (Recommended)

```bash
# Clone the repository
git clone https://github.com/rohitsharma007/raw_locator_generator.git
cd raw_locator_generator

# Install the package
pip install -e .

# Run the agent using the command
raw-locator-generator
```

#### Option 2: Install Dependencies Only

```bash
# Clone the repository
git clone https://github.com/rohitsharma007/raw_locator_generator.git
cd raw_locator_generator

# Install dependencies
pip install -r requirements.txt

# Run the agent directly
python -m raw_locator_generator
```

#### Option 3: Install from PyPI (Coming Soon)

```bash
pip install raw-locator-generator
raw-locator-generator
```

## 🚀 Usage

### Basic Usage

Simply run the command and provide a URL:

```bash
# If installed as package
raw-locator-generator

# Or run directly
python -m raw_locator_generator
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
from raw_locator_generator import DOMExtractorAgent

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

## 📁 Project Structure

```
raw_locator_generator/
├── src/
│   └── raw_locator_generator/
│       ├── __init__.py
│       └── dom_extractor_agent.py
├── docs/
│   ├── DOCUMENTATION_INDEX.txt
│   ├── EXAMPLE_OUTPUT.txt
│   ├── FRAMEWORK_COMPARISON.md
│   ├── GETTING_STARTED.txt
│   ├── QUICK_START.md
│   ├── START_HERE.txt
│   └── WORKFLOW_DIAGRAM.txt
├── examples/
│   └── (generated output files will appear here)
├── tests/
│   └── (test files)
├── README.md
├── requirements.txt
├── setup.py
├── pyproject.toml
└── .gitignore
```

## 📝 License

Free to use and modify for your projects.

issue :
PS C:\Automation\tools\raw_locator_generator> python -m raw_locator_generator.dom_extractor_agent
<frozen runpy>:128: RuntimeWarning: 'raw_locator_generator.dom_extractor_agent' found in sys.modules after import of package 'raw_locator_generator', but prior to execution of 'raw_locator_generator.dom_extractor_agent'; this may result in unpredictable behaviour

DevTools listening on ws://127.0.0.1:58745/devtools/browser/054b9d63-f6c8-4c91-a84a-1e559a0b55c5
✓ WebDriver initialized successfully
============================================================
DOM ELEMENT EXTRACTOR AGENT - ASSIST MODE
============================================================

This agent will navigate to your URL and extract all DOM elements.
Raw scripts will be generated for multiple automation frameworks.

Enter URL to analyze: [18404:23836:1127/151911.151:ERROR:google_apis\gcm\engine\registration_request.cc:292] Registration response error message: DEPRECATED_ENDPOINT
[18404:23836:1127/151911.158:ERROR:google_apis\gcm\engine\connection_factory_impl.cc:434] Failed to connect to MCS endpoint with error -111
Created TensorFlow Lite XNNPACK delegate for CPU.
[18404:23836:1127/151932.059:ERROR:google_apis\gcm\engine\connection_factory_impl.cc:434] Failed to connect to MCS endpoint with error -111
[18404:23836:1127/151941.080:ERROR:google_apis\gcm\engine\registration_request.cc:292] Registration response error message: DEPRECATED_ENDPOINT
[18404:23836:1127/152018.268:ERROR:google_apis\gcm\engine\connection_factory_impl.cc:434] Failed to connect to MCS endpoint with error -111
[18404:23836:1127/152036.209:ERROR:google_apis\gcm\engine\registration_request.cc:292] Registration response error message: DEPRECATED_ENDPOINT
[18404:23836:1127/152151.059:ERROR:google_apis\gcm\engine\connection_factory_impl.cc:434] Failed to connect to MCS endpoint with error -111

