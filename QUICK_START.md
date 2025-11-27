# QUICK START GUIDE
# ==================

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Agent
```bash
python dom_extractor_agent.py
```

### Step 3: Enter URL
```
Enter URL to analyze: example.com
```

That's it! The agent will generate 7 files with scripts for all major frameworks.

## 📋 What You Get

After running the agent, you'll have:

```
✓ raw_elements_20250127_143052.txt          # Framework-agnostic
✓ selenium_script_20250127_143052.py        # Python + Selenium
✓ playwright_script_20250127_143052.py      # Python + Playwright
✓ puppeteer_script_20250127_143052.js       # JavaScript + Puppeteer
✓ cypress_script_20250127_143052.js         # JavaScript + Cypress
✓ robot_framework_script_20250127_143052.robot  # Robot Framework
✓ dom_elements_20250127_143052.json         # JSON data
```

## 🎯 Using the Generated Scripts

### Option 1: Use Framework-Specific Script

Pick your framework and run:

**Selenium:**
```bash
python selenium_script_20250127_143052.py
```

**Playwright:**
```bash
python playwright_script_20250127_143052.py
```

**Puppeteer:**
```bash
node puppeteer_script_20250127_143052.js
```

**Cypress:**
```bash
npx cypress run --spec cypress_script_20250127_143052.js
```

### Option 2: Use Raw Locators

Open `raw_elements_*.txt` and copy locators to your existing code:

```python
# From raw_elements file:
# ID = 'submit-btn'
# XPATH = '/html/body/form/button'

# Use in your code:
element = driver.find_element(By.ID, 'submit-btn')
element = driver.find_element(By.XPATH, '/html/body/form/button')
```

### Option 3: Use JSON Data

Load JSON for custom automation:

```python
import json

with open('dom_elements_20250127_143052.json') as f:
    elements = json.load(f)

for elem in elements:
    if elem['type'] == 'buttons':
        print(f"Button found: {elem['id']}")
        # Your custom logic here
```

## 💡 Pro Tips

### Tip 1: Modify Generated Scripts
All scripts have actions commented out. Uncomment what you need:

```python
# Before:
# driver.find_element(By.ID, 'submit-btn').click()

# After:
driver.find_element(By.ID, 'submit-btn').click()
```

### Tip 2: Use Multiple Locator Strategies
If one fails, try another:

```python
# Try ID first (fastest)
try:
    element = driver.find_element(By.ID, 'submit-btn')
except:
    # Fallback to XPath (most reliable)
    element = driver.find_element(By.XPATH, '/html/body/form/button')
```

### Tip 3: Combine Multiple Elements
Chain actions together:

```python
# Fill form and submit
driver.find_element(By.ID, 'email').send_keys('test@example.com')
driver.find_element(By.ID, 'password').send_keys('password123')
driver.find_element(By.ID, 'submit-btn').click()
```

## 🔧 Common Customizations

### Change Browser Mode (Visible/Headless)

Edit `dom_extractor_agent.py`:

```python
def setup_driver(self):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Comment for visible
    ...
```

### Change Element Limit in Scripts

Edit the generation methods:

```python
for i, elem in enumerate(elements[:15], 1):  # Change 15 to any number
    ...
```

### Extract Specific Element Types Only

Modify `extract_interactive_elements()`:

```python
# Only extract buttons
selectors = {
    'buttons': "//button | //input[@type='button']"
}
```

## 🐛 Troubleshooting

### Issue: ChromeDriver not found
**Solution:**
```bash
pip install webdriver-manager
```

### Issue: No elements found
**Solution:** Website might load dynamically. Increase wait time:
```python
WebDriverWait(self.driver, 30).until(...)  # Increase timeout
```

### Issue: Elements not clickable
**Solution:** Add explicit wait before action:
```python
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'submit-btn'))
)
```

## 📚 Learn More

- Read full README.md for detailed documentation
- Check EXAMPLE_OUTPUT.txt for sample output
- Review WORKFLOW_DIAGRAM.txt for architecture

## 🎓 Framework-Specific Setup

### Selenium
```bash
pip install selenium
```

### Playwright
```bash
pip install playwright
playwright install
```

### Puppeteer
```bash
npm install puppeteer
```

### Cypress
```bash
npm install cypress
```

### Robot Framework
```bash
pip install robotframework
pip install robotframework-seleniumlibrary
```

## ✅ Next Steps

1. Run the agent on your target website
2. Review the generated scripts
3. Choose your preferred framework
4. Uncomment the actions you need
5. Add your business logic
6. Run and automate!

---

**Happy Automating! 🚀**
