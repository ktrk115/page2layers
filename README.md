# page2layers
A tool for decomposing a web page into element-wise image layers.

This tool was developed for the following research work.
> Modeling Visual Containment for Web Page Layout Optimization (Pacific Graphics 2021)  
Kotaro Kikuchi, Mayu Otani, Kota Yamaguchi, Edgar Simo-Serra  
[pdf](https://ktrk115.github.io/web_layout/assets/pg21_web.pdf), [project](https://ktrk115.github.io/web_layout/)

The dataset collected using this tool is available [here](https://github.com/ktrk115/web_layout).

## Installation

Install [Chrome](https://www.google.com/chrome/browser/desktop/index.html) and [ChromeDriver](https://chromedriver.chromium.org/downloads) beforehand.

```bash
git clone https://github.com/ktrk115/page2layers.git
conda create -n page2layers python=3.8 graphviz
conda activate page2layers
pip install -r requirements.txt
```


## Tested environments
- Ubuntu 20.04, Chrome 89.0.4389.90, ChromeDriver 89.0.4389.23
- macOS 10.15.7, Chrome 89.0.4389.90, ChromeDriver 89.0.4389.23


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
./page2layers sample.txt
```

Capture with Chrome extensions (e.g., ["I don't care about cookies"](https://www.i-dont-care-about-cookies.eu/))
```bash
./page2layers https://gdpr.eu/ --extension extensions/I_dont_care_about_cookies_3.2.9.crx
```

## Citation

If this tool helps your research, please cite our paper.

```
@article{Kikuchi2021,
    title = {Modeling Visual Containment for Web Page Layout Optimization},
    author = {Kotaro Kikuchi and Mayu Otani and Kota Yamaguchi and Edgar Simo-Serra},
    journal = {Computer Graphics Forum},
    volume = {40},
    number = {7},
    pages = {33--44},
    year = {2021},
    doi = {10.1111/cgf.14399}
}
```
