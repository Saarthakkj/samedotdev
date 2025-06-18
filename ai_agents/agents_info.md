# AnalyzerAgent

Analyzes a website screenshot (optionally with raw HTML) and produces a
**structured JSON spec** describing framework, layout, colours, typography,
components, etc.

| Key points | |
| ---------- | ------------------------------------------------------------- |
| Source     | `ai_agents/agents/analyzer_agent.py`                          |
| Depends on | Google Gemini (Vision / Text), BeautifulSoup, optional OCR    |
| Config     | `SystemConfig.gemini_api_key`                                 |

## Public interface

| Method | Purpose |
| ------ | ------- |
| `async analyze_screenshot(image_path, html_content="")` | Main asynchronous entry point. Returns a `dict` with the analysis JSON. |
| `analyze_screenshot_sync(...)` | Thin sync wrapper around the async API. |
| `batch_analyze(image_paths, html_contents=None)` | Convenience coroutine for analysing many screenshots concurrently. |
| `save_analysis(analysis, output_path)` / `load_analysis(path)` | Persist / restore analysis JSON. |
| `get_analysis_summary(analysis)` | Extracts a concise summary for reporting. |

### Output

Returns a **Python `dict`** that follows the analysis-JSON schema described in the README (framework, layout, colors, typography, components, etc.).

### How it works

1. Loads the PNG/JPEG screenshot and optional HTML.
2. Detects framework hints directly from HTML (`_detect_framework_from_html`).
3. If a Gemini key is configured:
   * Tries **vision** analysis (screenshot + prompt).  
   * Falls back to **text-only** analysis on failure.
4. If Gemini is unavailable, uses a **fallback analysis** based on heuristics,
   optional OCR via Tesseract, and HTML parsing.
5. Post-processes and validates the JSON (`_validate_and_enhance_analysis`).

### Example

```python
from ai_agents.config.system_config import SystemConfig
from ai_agents.agents.analyzer_agent import AnalyzerAgent

config  = SystemConfig(gemini_api_key="GEMINI_API_KEY")
agent   = AnalyzerAgent(config)
result  = await agent.analyze_screenshot("cloned_sites/original_*.png")
print(result["framework"]["primary"])
```
---

### docs/agents/screenshot_agent.md
```md
# ScreenshotAgent

Captures full-page screenshots for both **public** URLs (via Firecrawl) and
(local-only fallback optional).

| Key points | |
| ---------- | ------------------------------------------------------- |
| Source     | `ai_agents/agents/screenshot_agent.py`                  |
| Depends on | Firecrawl REST API (+ aiohttp/requests), asyncio        |
| Config     | `FIRECRAWL_API_KEY`, `SystemConfig.output_dir`          |

## Public interface

| Method | Purpose |
| ------ | ------- |
| `async capture_full_page(page, output_path)` | Pass a Playwright `page` object. |
| `async capture_full_page_url(url, output_path)` | URL-based capture (most used). |
| `capture_full_page_sync(url, output_path)` | Synchronous fallback. |
| `async capture_with_options(url, output_path, **opts)` | Same as above but lets you tweak the `wait` time & Firecrawl params. |

Internally these call `_firecrawl_screenshot` (async) or a requests-based sync
variant, then `_save_screenshot` for disk IO.

### Output

All capture methods resolve to a **`str` – the file path** of the saved PNG screenshot.

### Typical usage

```python
agent = ScreenshotAgent(config)
await agent.capture_full_page_url("https://netflix.com", "./cloned_sites/netflix.png")
```

> Note: Firecrawl **cannot reach `localhost`**; supply a public tunnel URL or
> add a local screenshot fallback (see docs/FAQ).
```
---

### docs/agents/generator_agent.md
```md
# GeneratorAgent

Turns the **analysis JSON** from `AnalyzerAgent` into an on-disk project
(currently React/Vite).  
(Implementation stub; extend for more frameworks.)

| Key points | |
| ---------- | --------------------------------------------- |
| Source     | `ai_agents/agents/generator_agent.py`         |
| Produces   | folder `cloned_sites/project_<timestamp>/…`   |

## Public interface

| Method | Purpose |
| ------ | ------- |
| `async generate_code(analysis, output_dir)` | Returns `{"status": "success", "generated_files": [...], "output_directory": ...}` |

### Output

`dict` with at minimum the following keys:
* `status` – "success" | "error"
* `generated_files` – `List[str]` of relative paths
* `output_directory` – `str` absolute path to the root of the generated project
* `error` – optional `str` when status ≠ success

Steps inside:

1. Decide template + file extensions from `analysis["framework"]`.
2. Create directory tree and populate `package.json`, `src/App.jsx`, assets…
3. Return a manifest so `WebsiteCloneOrchestrator` can validate.

### Minimal example

```python
gp = await generator.generate_code(analysis_json, "cloned_sites/project_...")
subprocess.run(["npm", "install"], cwd=gp["output_directory"])
```
```
---

### docs/agents/detector_agent.md
```md
# DetectorAgent

Computes **visual similarity** between two screenshots using
SSIM (structural similarity index).

| Key points | |
| ---------- | ---------------- |
| Source     | `ai_agents/agents/detector_agent.py` |
| Depends on | OpenCV + scikit-image |

## Public interface

| Method | Purpose |
| ------ | ------- |
| `async validate_similarity(original_path, generated_path)` → `float` | 0 ↔ 1 score (1 = identical). |

### Output

A **`float`** similarity score between 0.0 and 1.0 (falls back to 0.5 on errors).

Algorithm:

1. Load both images in grayscale.
2. Resize generated to original's size (if needed).
3. `ssim(img1, img2)` ➜ score.

Returns `0.5` on any failure so the pipeline can still continue.
```
---

### docs/agents/website_clone_orchestrator.md
```md
# WebsiteCloneOrchestrator

High-level pipeline that stitches all agents together to:

```
url → screenshot → analysis → code-gen → local build → generated screenshot → similarity → (optional) Lighthouse
```

| Key points | |
| ---------- | ----------------------------------------------------------- |
| Source     | `ai_agents/agents/website_clone.py`                         |
| Uses       | ScreenshotAgent, AnalyzerAgent, GeneratorAgent, DetectorAgent |
| Returns    | `CloneResult` (Pydantic model)                              |

### Output

[`CloneResult`](../config/system_config.py) – Pydantic model with fields:
* `status: str`
* `similarity_score: float`
* `generation_time: float`
* `deployed_url: Optional[str]`
* `lighthouse_score: Optional[Dict]`

## `async clone_website(url, framework="react", options={})`

| Stage | Details |
| ----- | ------- |
| Screenshot | `original_<ts>.png` via ScreenshotAgent |
| Analysis   | HTML/screenshot → analysis JSON |
| Code-gen   | GeneratorAgent writes `project_<ts>/…` |
| Validation | Checks essential files |
| Similarity | Compares `original_*.png` vs generated site (tunnel URL recommended) |
| Lighthouse | TODO stub |

### Options

| Key in `options` | Meaning |
| ---------------- | ------- |
| `generated_url`  | Where the generated site is served (defaults `http://localhost:3000`) |
| `run_lighthouse` | `True/False` |
| `analysis_depth` | How deep the Analyzer should crawl (default 2) |
| etc.             | see source |

### Quick start

```python
from ai_agents.main import run  # or call manually

config = SystemConfig()
orch   = WebsiteCloneOrchestrator(config)
result = await orch.clone_website(
    "https://netflix.com",
    framework="react",
    options={"generated_url": "https://abcd.ngrok-free.app"}
)
print(result.similarity_score)
```
```
---

### Putting the docs into the repo

Create the directory and add an `mkdocs.yml` / Docusaurus sidebar, or just link
these files from your main `README.md`, e.g.

```md
## Agent Docs
- [AnalyzerAgent](docs/agents/analyzer_agent.md)
- [ScreenshotAgent](docs/agents/screenshot_agent.md)
- ...
```

That's it—each agent now has a concise, self-contained reference page.
