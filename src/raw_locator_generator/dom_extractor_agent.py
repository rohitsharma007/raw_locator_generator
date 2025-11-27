#!/usr/bin/env python3
"""
DOM Element Extractor Agent
Assist mode: User provides URL, agent navigates and extracts DOM elements
"""

import sys
import json
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class DOMExtractorAgent:
    def __init__(self):
        """Initialize the agent with Chrome webdriver"""
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with headless options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # Suppress DevTools and logging errors
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✓ WebDriver initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing WebDriver: {e}")
            sys.exit(1)
    
    def navigate_to_url(self, url):
        """Navigate to the provided URL"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"\n→ Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print(f"✓ Successfully loaded: {self.driver.title}")
            return True
            
        except Exception as e:
            print(f"✗ Error navigating to URL: {e}")
            return False
    
    def extract_all_elements(self):
        """Extract all DOM elements from the page"""
        try:
            # Get page source
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            elements_data = []
            
            # Extract all elements with their attributes
            for element in soup.find_all(True):  # True finds all tags
                element_info = {
                    'tag': element.name,
                    'id': element.get('id', ''),
                    'classes': element.get('class', []),
                    'attributes': dict(element.attrs),
                    'text': element.get_text(strip=True)[:100] if element.get_text(strip=True) else '',
                    'xpath': self._generate_xpath(element)
                }
                elements_data.append(element_info)
            
            return elements_data
            
        except Exception as e:
            print(f"✗ Error extracting elements: {e}")
            return []
    
    def extract_interactive_elements(self):
        """Extract interactive elements (buttons, links, inputs, etc.)"""
        try:
            interactive_elements = []
            
            # Find all interactive elements using Selenium
            selectors = {
                'buttons': "//button | //input[@type='button'] | //input[@type='submit']",
                'links': "//a[@href]",
                'inputs': "//input | //textarea | //select",
                'clickable': "//*[@onclick or @role='button']"
            }
            
            for element_type, xpath in selectors.items():
                elements = self.driver.find_elements(By.XPATH, xpath)
                
                for element in elements:
                    try:
                        element_info = {
                            'type': element_type,
                            'tag': element.tag_name,
                            'id': element.get_attribute('id') or '',
                            'class': element.get_attribute('class') or '',
                            'name': element.get_attribute('name') or '',
                            'text': element.text[:100] if element.text else '',
                            'href': element.get_attribute('href') if element.tag_name == 'a' else '',
                            'xpath': self._get_element_xpath(element),
                            'css_selector': self._get_css_selector(element)
                        }
                        interactive_elements.append(element_info)
                    except:
                        continue
            
            return interactive_elements
            
        except Exception as e:
            print(f"✗ Error extracting interactive elements: {e}")
            return []
    
    def _get_element_xpath(self, element):
        """Generate XPath for a Selenium element"""
        try:
            return self.driver.execute_script("""
                function getXPath(element) {
                    if (element.id !== '')
                        return '//*[@id="' + element.id + '"]';
                    if (element === document.body)
                        return '/html/body';
                    
                    var ix = 0;
                    var siblings = element.parentNode.childNodes;
                    for (var i = 0; i < siblings.length; i++) {
                        var sibling = siblings[i];
                        if (sibling === element)
                            return getXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
                            ix++;
                    }
                }
                return getXPath(arguments[0]);
            """, element)
        except:
            return ""
    
    def _get_css_selector(self, element):
        """Generate CSS selector for a Selenium element"""
        try:
            css = element.tag_name
            if element.get_attribute('id'):
                css += f"#{element.get_attribute('id')}"
            elif element.get_attribute('class'):
                classes = element.get_attribute('class').split()
                css += '.' + '.'.join(classes[:2])  # Limit to first 2 classes
            return css
        except:
            return ""
    
    def _generate_xpath(self, soup_element):
        """Generate XPath for a BeautifulSoup element"""
        components = []
        child = soup_element if soup_element.name else soup_element.parent
        
        for parent in child.parents:
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if len(siblings) == 1 
                else f"{child.name}[{siblings.index(child) + 1}]"
            )
            child = parent
        
        components.reverse()
        return '/' + '/'.join(components) if components else ''
    
    def generate_raw_script(self, elements, framework='all'):
        """Generate framework-agnostic raw scripts that can be used with any automation framework"""
        
        scripts = {}
        
        # Generate raw element data script (framework-agnostic)
        scripts['raw_elements'] = self._generate_raw_elements_script(elements)
        
        # Generate framework-specific scripts
        if framework in ['all', 'selenium']:
            scripts['selenium'] = self._generate_selenium_script(elements)
        
        if framework in ['all', 'playwright']:
            scripts['playwright'] = self._generate_playwright_script(elements)
        
        if framework in ['all', 'puppeteer']:
            scripts['puppeteer'] = self._generate_puppeteer_script(elements)
        
        if framework in ['all', 'cypress']:
            scripts['cypress'] = self._generate_cypress_script(elements)
        
        if framework in ['all', 'robot']:
            scripts['robot_framework'] = self._generate_robot_framework_script(elements)
        
        return scripts
    
    def _generate_raw_elements_script(self, elements):
        """Generate raw element locators in a framework-agnostic format"""
        script = []
        script.append("# RAW ELEMENT LOCATORS - Framework Agnostic")
        script.append("# ==========================================")
        script.append("# Use these locators with any automation framework\n")
        script.append(f"# URL: {self.driver.current_url}")
        script.append(f"# Page Title: {self.driver.title}\n")
        
        script.append("# ELEMENT LOCATORS")
        script.append("# ================\n")
        
        for i, elem in enumerate(elements, 1):
            script.append(f"# Element {i}: {elem['type'].upper()}")
            script.append(f"# Description: {elem['text'][:80] if elem['text'] else 'No text'}")
            script.append(f"# Tag: {elem['tag']}")
            
            # Provide all possible locator strategies
            if elem['id']:
                script.append(f"ID = '{elem['id']}'")
            if elem['name']:
                script.append(f"NAME = '{elem['name']}'")
            if elem['class']:
                script.append(f"CLASS = '{elem['class']}'")
            if elem['xpath']:
                script.append(f"XPATH = '{elem['xpath']}'")
            if elem['css_selector']:
                script.append(f"CSS = '{elem['css_selector']}'")
            if elem['href']:
                script.append(f"HREF = '{elem['href']}'")
            
            script.append("")
        
        return '\n'.join(script)
    
    def _generate_selenium_script(self, elements):
        """Generate Selenium-specific script"""
        script = []
        script.append("# SELENIUM AUTOMATION SCRIPT")
        script.append("# ==========================\n")
        script.append("from selenium import webdriver")
        script.append("from selenium.webdriver.common.by import By")
        script.append("from selenium.webdriver.support.ui import WebDriverWait")
        script.append("from selenium.webdriver.support import expected_conditions as EC")
        script.append("from selenium.webdriver.common.keys import Keys\n")
        script.append("# Setup")
        script.append("driver = webdriver.Chrome()")
        script.append(f"driver.get('{self.driver.current_url}')\n")
        
        for i, elem in enumerate(elements[:15], 1):
            script.append(f"# {elem['type'].upper()}: {elem['text'][:50]}")
            
            if elem['id']:
                locator = f"driver.find_element(By.ID, '{elem['id']}')"
            elif elem['name']:
                locator = f"driver.find_element(By.NAME, '{elem['name']}')"
            elif elem['xpath']:
                locator = f"driver.find_element(By.XPATH, '{elem['xpath']}')"
            else:
                locator = f"driver.find_element(By.CSS_SELECTOR, '{elem['css_selector']}')"
            
            if elem['type'] in ['buttons', 'links']:
                script.append(f"# {locator}.click()")
            elif elem['type'] == 'inputs':
                script.append(f"# {locator}.send_keys('your_value')")
            
            script.append("")
        
        script.append("# driver.quit()")
        return '\n'.join(script)
    
    def _generate_playwright_script(self, elements):
        """Generate Playwright-specific script"""
        script = []
        script.append("# PLAYWRIGHT AUTOMATION SCRIPT")
        script.append("# ============================\n")
        script.append("from playwright.sync_api import sync_playwright\n")
        script.append("with sync_playwright() as p:")
        script.append("    browser = p.chromium.launch()")
        script.append("    page = browser.new_page()")
        script.append(f"    page.goto('{self.driver.current_url}')\n")
        
        for i, elem in enumerate(elements[:15], 1):
            script.append(f"    # {elem['type'].upper()}: {elem['text'][:50]}")
            
            if elem['id']:
                locator = f"page.locator('#{elem['id']}')"
            elif elem['xpath']:
                locator = f"page.locator('xpath={elem['xpath']}')"
            elif elem['css_selector']:
                locator = f"page.locator('{elem['css_selector']}')"
            else:
                locator = f"page.locator('text={elem['text'][:30]}')"
            
            if elem['type'] in ['buttons', 'links']:
                script.append(f"    # {locator}.click()")
            elif elem['type'] == 'inputs':
                script.append(f"    # {locator}.fill('your_value')")
            
            script.append("")
        
        script.append("    # browser.close()")
        return '\n'.join(script)
    
    def _generate_puppeteer_script(self, elements):
        """Generate Puppeteer-specific script"""
        script = []
        script.append("// PUPPETEER AUTOMATION SCRIPT")
        script.append("// ============================\n")
        script.append("const puppeteer = require('puppeteer');\n")
        script.append("(async () => {")
        script.append("  const browser = await puppeteer.launch();")
        script.append("  const page = await browser.newPage();")
        script.append(f"  await page.goto('{self.driver.current_url}');\n")
        
        for i, elem in enumerate(elements[:15], 1):
            script.append(f"  // {elem['type'].upper()}: {elem['text'][:50]}")
            
            if elem['id']:
                selector = f"'#{elem['id']}'"
            elif elem['xpath']:
                selector = f"'xpath/{elem['xpath']}'"
            elif elem['css_selector']:
                selector = f"'{elem['css_selector']}'"
            else:
                continue
            
            if elem['type'] in ['buttons', 'links']:
                script.append(f"  // await page.click({selector});")
            elif elem['type'] == 'inputs':
                script.append(f"  // await page.type({selector}, 'your_value');")
            
            script.append("")
        
        script.append("  // await browser.close();")
        script.append("})();")
        return '\n'.join(script)
    
    def _generate_cypress_script(self, elements):
        """Generate Cypress-specific script"""
        script = []
        script.append("// CYPRESS AUTOMATION SCRIPT")
        script.append("// =========================\n")
        script.append("describe('Automated Test', () => {")
        script.append("  it('should perform actions', () => {")
        script.append(f"    cy.visit('{self.driver.current_url}');\n")
        
        for i, elem in enumerate(elements[:15], 1):
            script.append(f"    // {elem['type'].upper()}: {elem['text'][:50]}")
            
            if elem['id']:
                selector = f"'#{elem['id']}'"
            elif elem['xpath']:
                selector = f"'xpath={elem['xpath']}'"  # Note: Cypress needs xpath plugin
            elif elem['css_selector']:
                selector = f"'{elem['css_selector']}'"
            else:
                continue
            
            if elem['type'] in ['buttons', 'links']:
                script.append(f"    // cy.get({selector}).click();")
            elif elem['type'] == 'inputs':
                script.append(f"    // cy.get({selector}).type('your_value');")
            
            script.append("")
        
        script.append("  });")
        script.append("});")
        return '\n'.join(script)
    
    def _generate_robot_framework_script(self, elements):
        """Generate Robot Framework-specific script"""
        script = []
        script.append("# ROBOT FRAMEWORK AUTOMATION SCRIPT")
        script.append("# ==================================\n")
        script.append("*** Settings ***")
        script.append("Library    SeleniumLibrary\n")
        script.append("*** Variables ***")
        script.append(f"${{URL}}    {self.driver.current_url}\n")
        
        # Add element locators as variables
        for i, elem in enumerate(elements[:15], 1):
            if elem['id']:
                script.append(f"${{ELEMENT_{i}}}    id:{elem['id']}")
            elif elem['xpath']:
                script.append(f"${{ELEMENT_{i}}}    xpath:{elem['xpath']}")
        
        script.append("\n*** Test Cases ***")
        script.append("Automated Test Scenario")
        script.append("    Open Browser    ${URL}    chrome")
        
        for i, elem in enumerate(elements[:15], 1):
            if elem['id'] or elem['xpath']:
                script.append(f"    # {elem['type'].upper()}: {elem['text'][:50]}")
                if elem['type'] in ['buttons', 'links']:
                    script.append(f"    # Click Element    ${{ELEMENT_{i}}}")
                elif elem['type'] == 'inputs':
                    script.append(f"    # Input Text    ${{ELEMENT_{i}}}    your_value")
        
        script.append("    # Close Browser")
        return '\n'.join(script)
    
    def save_results(self, elements, output_format='json'):
        """Save extracted elements and generate scripts for all frameworks"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        saved_files = []

        # Create organized folder structure
        output_base = Path("output")
        folders = {
            'json_data': output_base / 'json_data',
            'raw_elements': output_base / 'raw_elements',
            'selenium': output_base / 'selenium',
            'playwright': output_base / 'playwright',
            'puppeteer': output_base / 'puppeteer',
            'cypress': output_base / 'cypress',
            'robot_framework': output_base / 'robot_framework'
        }

        # Create all folders
        for folder in folders.values():
            folder.mkdir(parents=True, exist_ok=True)

        # Save JSON data
        if output_format == 'json':
            filename = folders['json_data'] / f"dom_elements_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(elements, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Elements saved to: {filename}")
            saved_files.append(str(filename))

        # Generate scripts for all frameworks
        print("\n→ Generating framework-specific scripts...")
        scripts = self.generate_raw_script(elements, framework='all')

        # Save each framework script in its respective folder
        framework_mapping = {
            'raw_elements': (folders['raw_elements'], f"raw_elements_{timestamp}.txt"),
            'selenium': (folders['selenium'], f"selenium_script_{timestamp}.py"),
            'playwright': (folders['playwright'], f"playwright_script_{timestamp}.py"),
            'puppeteer': (folders['puppeteer'], f"puppeteer_script_{timestamp}.js"),
            'cypress': (folders['cypress'], f"cypress_script_{timestamp}.js"),
            'robot_framework': (folders['robot_framework'], f"robot_framework_script_{timestamp}.robot")
        }

        for framework_name, script_content in scripts.items():
            if framework_name in framework_mapping:
                folder, filename = framework_mapping[framework_name]
                filepath = folder / filename

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                print(f"  ✓ {framework_name.upper()}: {filepath}")
                saved_files.append(str(filepath))

        return saved_files
    
    def print_summary(self, elements):
        """Print a summary of extracted elements"""
        print(f"\n{'='*60}")
        print(f"EXTRACTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total elements found: {len(elements)}")
        
        # Count by type
        type_counts = {}
        for elem in elements:
            elem_type = elem.get('type', 'other')
            type_counts[elem_type] = type_counts.get(elem_type, 0) + 1
        
        print(f"\nBreakdown by type:")
        for elem_type, count in sorted(type_counts.items()):
            print(f"  - {elem_type}: {count}")
        
        print(f"\n{'='*60}\n")
    
    def run_assist_mode(self):
        """Run the agent in assist mode"""
        print("="*60)
        print("DOM ELEMENT EXTRACTOR AGENT - ASSIST MODE")
        print("="*60)
        print("\nThis agent will navigate to your URL and extract all DOM elements.")
        print("Raw scripts will be generated for multiple automation frameworks.\n")
        
        try:
            # Get URL from user
            url = input("Enter URL to analyze: ").strip()
            
            if not url:
                print("✗ No URL provided. Exiting.")
                return
            
            # Navigate to URL
            if not self.navigate_to_url(url):
                return
            
            # Extract elements
            print("\n→ Extracting interactive elements...")
            interactive_elements = self.extract_interactive_elements()
            print(f"✓ Found {len(interactive_elements)} interactive elements")
            
            # Print summary
            self.print_summary(interactive_elements)
            
            # Save results and generate all framework scripts
            saved_files = self.save_results(interactive_elements)
            
            # Show sample of extracted elements
            print("\nSample of extracted elements (first 5):")
            print("-" * 60)
            for i, elem in enumerate(interactive_elements[:5], 1):
                print(f"\n{i}. {elem['type'].upper()} - {elem['tag']}")
                print(f"   ID: {elem['id']}")
                print(f"   Class: {elem['class']}")
                print(f"   Text: {elem['text'][:50]}...")
                print(f"   XPath: {elem['xpath'][:80]}...")
            
            print("\n" + "="*60)
            print("✓ Extraction completed successfully!")
            print(f"✓ Generated {len(saved_files)} files with framework-specific scripts")
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n\n✗ Operation cancelled by user")
        except Exception as e:
            print(f"\n✗ An error occurred: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()
            print("\n✓ WebDriver closed")


def main():
    """Main entry point"""
    agent = DOMExtractorAgent()
    agent.run_assist_mode()


if __name__ == "__main__":
    main()
