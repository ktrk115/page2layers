# page2layers
Decompose a web page into element-wise image layers


## Installation

Install [Chrome](https://www.google.com/chrome/browser/desktop/index.html) and [ChromeDriver](https://chromedriver.chromium.org/downloads) beforehand.

```bash
git clone https://github.com/ktrk15/page2layers.git
conda create -n page2layers python=3.8
conda activate page2layers
pip install -r requirements.txt
```


## Tested environments
- Ubuntu 20.04, Chrome 89.0.4389.90, ChromeDriver 89.0.4389.23


## Usage

Capture a single web page
```bash
./page2layers https://example.com
```

Capture with headless mode
```bash
./page2layers https://example.com --headless
```

Capture multiple pages by a text file with URLs on each line
```bash
./page2layers sample_URLs.txt
```

Capture with Chrome extensions (e.g., ["I don't care about cookies"](https://www.i-dont-care-about-cookies.eu/))
```bash
./page2layers https://gdpr.eu/ --extension extensions/I_dont_care_about_cookies_3.2.9.crx
```
