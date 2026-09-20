"""
capture_screenshots.py
======================
Automated Playwright screenshot script for the behavioural course study
(oTree app ``design_exp``).

Adapted from capture_cs1_screenshots.py of the CS1/Anti-Inher project.

HOW TO USE
----------
1. pip install playwright && playwright install chromium
2. Start oTree:  otree devserver
3. Run:          python capture_screenshots.py
4. Screenshots land in ./screenshots/A/ and ./screenshots/B/

WHAT IT DOES
------------
Creates one session with 2 participants and walks both of them through the
whole study, screenshotting every page from start to finish.

* Every screenshot is a FULL-PAGE shot (top to bottom of the oTree page, not
  just the part that fits in the viewport).
* Output is split by experiment group:

      screenshots/A/   the complete path, group A version of every experiment
      screenshots/B/   the complete path, group B version of every experiment

  Group A/B is balanced across participants for every question, so the two
  participants together fill both folders. Pages with no A/B version (welcome,
  survey, thanks) are written into both folders, so each one is a complete
  start-to-finish walkthrough on its own, and the two folders line up
  file-for-file for side-by-side comparison.
* File names are <step>_<experiment>.png, e.g. ``02_E1_Conjunction_fallacy.png``
  - the step keeps the folder in the order the pages were walked, the group is
  in the folder name. Set NUMBER_FILES = False to drop the step prefix.
* The experiment is recognised from the form field names on the page (see
  FIELD_PREFIX_TO_EXPERIMENT), because every experiment is served by the same
  ``QuestionPage`` class.
* The session is created with ``randomize_experiment_order = False`` so the
  experiments appear in the fixed C.PAGES_TO_QUESTIONS order (see settings.py)
  and both folders are numbered the same. Pass --randomize to keep the
  per-participant shuffle instead.

POP-UPS / IN-PAGE STEPS (all captured)
--------------------------------------
E26 Wisdom of crowd, group B : the dialectical-bootstrapping overlay
      (#secondGuessOverlay) opened by #secondGuessContinue.
      -> B/<n>_E26_Wisdom_of_crowd.png + B/<n>_E26_Wisdom_of_crowd_popup.png
E32 Insurance plan, group B  : the 4 in-page steps (.step / nextStep()).
      -> B/<n>_E32_Insurance_plan_step1..step4.png
      (group A shows everything on one page -> A/<n>_E32_Insurance_plan.png)
E27-30 Counting heuristic    : the chart is revealed year by year by
      #updateChartButton; the form only appears at the end.
      -> <n>_E27_30_Counting_heuristic_round<r>_chart.png      (first year)
         <n>_E27_30_Counting_heuristic_round<r>_chart_end.png  (last year)
         <n>_E27_30_Counting_heuristic_round<r>_question.png
Native JS alert()s (e.g. the wisdom-of-crowd validation) are auto-dismissed.

The session is created with ``testing = False`` so the "Skip for testing"
button stays out of the shots, and the devserver's debug panel is hidden
before each screenshot.
"""

import argparse
import json as _json
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


# ---------------------------------------------------------------------------
# Config (edit here or pass as CLI args)
# ---------------------------------------------------------------------------
BASE_URL            = "http://127.0.0.1:8000/"
SESSION_CONFIG_NAME = "design_exp"      # name in settings.py SESSION_CONFIGS
NUM_PARTICIPANTS    = 2                 # 2 = one A and one B for every question
MAX_STEPS           = 200
OUT_DIR             = "screenshots"      # A/ and B/ are created inside it
HEADED              = True              # False = headless
RANDOMIZE_ORDER     = False             # False = fixed experiment order
NUMBER_FILES        = True              # prefix files with their step in the path

# One folder per experiment group; each one gets the whole path.
GROUP_FOLDERS = ("A", "B")


# ---------------------------------------------------------------------------
# Experiment naming
# Keys mirror C.PAGES_TO_QUESTIONS / C.EXPERIMENT_TOGGLES in design_exp/__init__.py
# ---------------------------------------------------------------------------
EXPERIMENT_LABELS = {
    "ConjunctionFallacy":        "E1_Conjunction_fallacy",
    "GamblersFallacy":           "E2_Gamblers_fallacy",
    "HotHandFallacy":            "E3_Hot_hand_fallacy",
    "BaseRateFallacy":           "E5_Base_rate_fallacy",
    "IllusionofControl":         "E6_Illusion_of_control",
    "AnchoringEffect":           "E7_Anchoring",
    "HindsightBias":             "E8_Hindsight_bias",
    "PresentBias":               "E9_Present_bias",
    "LossAversion":              "E10_Loss_aversion",
    "EndowmentEffect":           "E11_Endowment_effect",
    "DecoyEffect":               "E12_Decoy_effect",
    "FramingEffect":             "E13_Framing_effect",
    "StatusQuoBias":             "E14_Status_quo_bias",
    "SunkCostFallacy":           "E15_Sunk_cost_fallacy",
    "MentalAccounting":          "E16_Mental_accounting",
    "UltimatumGame":             "E17_Ultimatum_game",
    "DictatorGame":              "E18_Dictator_game",
    "TrustInvestmentGame":       "E19_Trust_game",
    "PublicGoodsGame":           "E20_Public_goods_game",
    "PrisonersDilemma":          "E21_Prisoners_dilemma",
    "CoordinationGame":          "E22_Coordination_game",
    "BertrandCompetition":       "E23_Bertrand_price",
    "CournotCompetition":        "E24_Cournot_quantity",
    "SSWMarket":                 "E25_SSW_market",
    "WisdomofCrowd":             "E26_Wisdom_of_crowd",
    "CognitiveLimitInvestment":  "E27_30_Counting_heuristic",
    "CognitiveLimitBox":         "E31_Deterministic_mirror",
    "CognitiveLimitInsurance":   "E32_Insurance_plan",
}

# Form-field prefix -> experiment key. Longest prefix wins, so order is
# irrelevant. Field names on the page carry a "_A"/"_B" group suffix.
FIELD_PREFIX_TO_EXPERIMENT = {
    "conjunction_":                 "ConjunctionFallacy",
    "gambler_":                     "GamblersFallacy",
    "hotHand":                      "HotHandFallacy",
    "baseRate":                     "BaseRateFallacy",
    "illusionControl":              "IllusionofControl",
    "anchoring":                    "AnchoringEffect",
    "hindsight":                    "HindsightBias",
    "presentBias":                  "PresentBias",
    "lossAversion":                 "LossAversion",
    "endowment":                    "EndowmentEffect",
    "decoy":                        "DecoyEffect",
    "framing":                      "FramingEffect",
    "statusQuo":                    "StatusQuoBias",
    "sunkCost":                     "SunkCostFallacy",
    "mentalAccounting":             "MentalAccounting",
    "ultimatum_":                   "UltimatumGame",
    "dictator_":                    "DictatorGame",
    "trust_":                       "TrustInvestmentGame",
    "public_goods_":                "PublicGoodsGame",
    "prisoner_":                    "PrisonersDilemma",
    "coord_":                       "CoordinationGame",
    "bertrand_":                    "BertrandCompetition",
    "cournot_":                     "CournotCompetition",
    "ssw_":                         "SSWMarket",
    "wisdom_":                      "WisdomofCrowd",
    "CognitiveLimitInvestment":     "CognitiveLimitInvestment",
    "cognitiveLimitBox_switch":     "CognitiveLimitBox",
    "cognitiveLimitInsurance":      "CognitiveLimitInsurance",
}

# ---------------------------------------------------------------------------
# Values used to fill the forms (only needed to get past validation)
# ---------------------------------------------------------------------------
TEXT_VALUES = {
    "first_name":     "Test",
    "last_name":      "Participant",
    "student_number": "00000000",
    "Demographics_InvestorExperience": "No prior investment experience.",
}

# Explicit numeric answers; anything else falls back to the input's own
# min attribute, then DEFAULT_NUMBER (clamped to min/max).
NUMBER_VALUES = {
    "Demographics_Age": "25",
}
DEFAULT_NUMBER = "5"

# Explicit radio/select answers by field name (base name without _A/_B).
# Empty by default: the first option is picked.
RADIO_VALUES = {}


# ---------------------------------------------------------------------------
# URL helpers
# ---------------------------------------------------------------------------

def normalize_url(base_url, maybe_relative):
    return urljoin(base_url.rstrip("/") + "/", maybe_relative)


def unique_participant_links(page, base_url):
    links = page.eval_on_selector_all(
        "a[href]", "els => els.map(e => e.getAttribute('href'))"
    )
    results, seen = [], set()
    for href in links:
        if not href or "/InitializeParticipant/" not in href:
            continue
        full = normalize_url(base_url, href)
        if full not in seen:
            seen.add(full)
            results.append(full)
    return results


# ---------------------------------------------------------------------------
# Session creation
# ---------------------------------------------------------------------------

def create_session_and_get_links(page, base_url, config_name, expected_links,
                                 config_overrides):
    """Try REST API -> admin page -> demo page to create a session and get links."""

    # Strategy 1: oTree 5 REST API
    api_url = normalize_url(base_url, "api/sessions")
    try:
        page.goto(base_url, wait_until="domcontentloaded")
        response = page.request.post(
            api_url,
            data=_json.dumps({
                "session_config_name": config_name,
                "num_participants": expected_links,
                "modified_session_config_fields": config_overrides,
            }),
            headers={"Content-Type": "application/json"},
        )
        if response.ok:
            body = response.json()
            session_code = body.get("code") or body.get("session_code")
            if session_code:
                lresp = page.request.get(
                    normalize_url(base_url, f"api/sessions/{session_code}")
                )
                if lresp.ok:
                    urls = []
                    for participant in lresp.json().get("participants", []):
                        token = participant.get("_url_param") or participant.get("code")
                        if token:
                            urls.append(normalize_url(base_url, f"InitializeParticipant/{token}"))
                    if len(urls) >= expected_links:
                        print(f"  [session] REST API -> {session_code}")
                        return urls[:expected_links]
                # Fallback: scrape the start-links page
                page.goto(normalize_url(base_url, f"SessionStartLinks/{session_code}"),
                          wait_until="domcontentloaded")
                page.wait_for_timeout(1500)
                links = unique_participant_links(page, base_url)
                if len(links) >= expected_links:
                    print(f"  [session] REST API + start-links scrape -> {session_code}")
                    return links[:expected_links]
        else:
            print(f"  [session] REST API returned {response.status}, trying admin page...")
    except Exception as e:
        print(f"  [session] REST API failed ({e}), trying admin page...")

    # Strategy 2: Admin sessions page
    for admin_path in ["sessions", "create_session"]:
        try:
            page.goto(normalize_url(base_url, admin_path), wait_until="domcontentloaded")
            page.wait_for_timeout(1000)
            for btn_text in ["Create new session", "Create session", "New session"]:
                btn = page.locator(f"text={btn_text}").first
                if btn.count() > 0:
                    btn.click()
                    page.wait_for_load_state("domcontentloaded")
                    break
            if page.locator("select[name='session_config']").count() > 0:
                page.select_option("select[name='session_config']", config_name)
                page.wait_for_timeout(500)
            filled = False
            for sel in ["input[name='num_participants']", "input[name='num-demo-participants']",
                        "input[name='num_demo_participants']", "input[type='number']"]:
                if page.locator(sel).count() > 0:
                    page.fill(sel, str(expected_links))
                    filled = True
                    break
            if not filled:
                continue
            for sel in ["button[type='submit']", "input[type='submit']",
                        "button:has-text('Create')", "button:has-text('Start')"]:
                if page.locator(sel).count() > 0:
                    page.locator(sel).first.click()
                    break
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2000)
            links = unique_participant_links(page, base_url)
            if links:
                print(f"  [session] Admin page /{admin_path}")
                return links[:expected_links]
            matches = re.findall(r"/InitializeParticipant/[A-Za-z0-9_-]+", page.content())
            urls, seen = [], set()
            for m in matches:
                full = normalize_url(base_url, m)
                if full not in seen:
                    seen.add(full)
                    urls.append(full)
            if urls:
                print(f"  [session] Admin page /{admin_path} (regex scrape)")
                return urls[:expected_links]
        except Exception as e:
            print(f"  [session] Admin page /{admin_path} failed ({e})")

    # Strategy 3: Demo page (gives only 1 link - warns but continues)
    try:
        page.goto(normalize_url(base_url, f"demo/{config_name}"), wait_until="domcontentloaded")
        page.wait_for_timeout(1000)
        for btn_text in ["Play", "Start", "Demo"]:
            btn = page.locator(f"button:has-text('{btn_text}'), a:has-text('{btn_text}')").first
            if btn.count() > 0:
                btn.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(2000)
                break
        try:
            page.wait_for_url(lambda u: f"/demo/{config_name}" not in u, timeout=15000)
        except PlaywrightTimeoutError:
            pass
        links = unique_participant_links(page, base_url)
        if not links and "/InitializeParticipant/" in page.url:
            links = [page.url]
        if links:
            print(f"  [session] WARNING: demo page returned {len(links)}/{expected_links} links.")
            print( "            The demo page ignores the session config overrides, so the")
            print( "            experiment order may be randomized.")
            return links
    except Exception as e:
        print(f"  [session] Demo page failed ({e})")

    raise RuntimeError(
        f"Could not create a session with {expected_links} participants.\n"
        f"Open {normalize_url(base_url, 'sessions')} manually, create a "
        f"'{config_name}' session with {expected_links} participants, then rerun."
    )


# ---------------------------------------------------------------------------
# Page identification
# ---------------------------------------------------------------------------

def otree_page_class(url):
    """/p/<code>/design_exp/QuestionPage/<round>/ -> 'QuestionPage'"""
    parts = [p for p in urlparse(url).path.split("/") if p]
    return parts[-2] if len(parts) >= 2 else "page"


def form_field_names(page):
    return page.eval_on_selector_all(
        "input[name], select[name], textarea[name]",
        "els => [...new Set(els.map(e => e.name))]",
    )


def experiment_from_fields(names):
    """Return (experiment_key, group) from the form field names, or (None, None)."""
    best_key, best_len, best_group = None, -1, None
    for name in names:
        group = None
        base = name
        if name.endswith("_A") or name.endswith("_B"):
            group, base = name[-1], name[:-2]
        for prefix, key in FIELD_PREFIX_TO_EXPERIMENT.items():
            if base.startswith(prefix) and len(prefix) > best_len:
                best_key, best_len, best_group = key, len(prefix), group
    return best_key, best_group


def resolve_page(page, survey_seen):
    """Return (kind, label, group).

    kind: 'welcome' | 'question' | 'investment' | 'insurance' | 'survey'
          | 'thanks' | 'other'
    """
    page_class = otree_page_class(page.url)
    names = form_field_names(page)

    if page_class == "Instructions_WelcomeScreen":
        return "welcome", "Welcome", None
    if page_class == "ThanksPage":
        return "thanks", "Thanks", None
    if page_class == "SurveyPage":
        return "survey", f"Survey_{survey_seen + 1}", None
    if page_class == "LeavePage":
        return "other", "LeavePage", None

    key, group = experiment_from_fields(names)

    if page_class == "CognitiveLimitInvestmentPage" or page.locator("#updateChartButton").count() > 0:
        key = "CognitiveLimitInvestment"
        # No _A/_B suffix on these fields: tell the groups apart by the wording.
        body = page.inner_text("body").lower()
        group = "B" if "cumulative returns below" in body else "A"
        return "investment", EXPERIMENT_LABELS[key], group

    if page_class == "CognitiveLimitInsurancePage" or "cognitiveLimitInsurance" in names:
        key = "CognitiveLimitInsurance"
        # No _A/_B suffix either: group B is the stepwise version.
        group = "B" if page.locator("#step-1").count() > 0 else "A"
        return "insurance", EXPERIMENT_LABELS[key], group

    if key:
        return "question", EXPERIMENT_LABELS[key], group

    return "other", page_class, None


def file_stem(step, label, suffix=""):
    """<step>_<experiment>[_<suffix>], e.g. 08_E7_Anchoring.

    The step prefix keeps the folder in the order the participant walked the
    study; the A/B folder carries the group, so it is not in the name.
    """
    parts = [f"{step:02d}"] if NUMBER_FILES else []
    parts.append(label)
    if suffix:
        parts.append(suffix)
    return "_".join(parts)


def group_dirs(out_root, group):
    """Folders a page belongs in: its own group's, or both when it has none."""
    if group in GROUP_FOLDERS:
        return [out_root / group]
    return [out_root / g for g in GROUP_FOLDERS]


# ---------------------------------------------------------------------------
# Field filling
# ---------------------------------------------------------------------------

def _is_numeric_input(inp):
    """oTree renders Float/Integer fields as <input type="text" inputmode="decimal">,
    so the type attribute alone is not enough."""
    if (inp.get_attribute("type") or "text").lower() in {"number", "range"}:
        return True
    return (inp.get_attribute("inputmode") or "").lower() in {"decimal", "numeric"}


def _number_for(inp, name):
    """Pick a value a numeric input will accept (respects min/max)."""
    value = NUMBER_VALUES.get(name)
    lo = inp.get_attribute("min")
    hi = inp.get_attribute("max")
    if value is None:
        value = lo if lo not in (None, "") else DEFAULT_NUMBER
    try:
        v = float(value)
        if lo not in (None, ""):
            v = max(v, float(lo))
        if hi not in (None, ""):
            v = min(v, float(hi))
        return str(int(v)) if v == int(v) else str(v)
    except (TypeError, ValueError):
        return str(value)


def fill_fields(page, root=None):
    """Fill every visible form field under `root` (default: the whole page)."""
    scope = root if root is not None else page

    # Textareas
    for ta in scope.locator("textarea[name]").all():
        name = ta.get_attribute("name")
        if not name:
            continue
        try:
            if not ta.is_visible():
                continue
            ta.fill(TEXT_VALUES.get(name, "Test response for the automated screenshot run."))
        except Exception:
            pass

    # Selects
    for sel_el in scope.locator("select[name]").all():
        name = sel_el.get_attribute("name")
        if not name:
            continue
        base = name[:-2] if name.endswith(("_A", "_B")) else name
        preferred = RADIO_VALUES.get(base, RADIO_VALUES.get(name))
        try:
            if preferred is not None:
                sel_el.select_option(value=str(preferred))
                continue
        except Exception:
            pass
        for opt in sel_el.locator("option").all():
            v = opt.get_attribute("value")
            if v:
                try:
                    sel_el.select_option(value=v)
                except Exception:
                    pass
                break

    # Text / number inputs (hidden inputs such as isLeaving are left alone)
    for inp in scope.locator(
        "input[name]:not([type='radio']):not([type='checkbox'])"
        ":not([type='hidden']):not([type='submit'])"
    ).all():
        name = inp.get_attribute("name")
        if not name:
            continue
        try:
            if not inp.is_visible():
                continue
        except Exception:
            continue
        if _is_numeric_input(inp):
            value = _number_for(inp, name)
        else:
            value = TEXT_VALUES.get(name, NUMBER_VALUES.get(name, "test"))
        try:
            inp.fill(str(value))
        except Exception:
            pass

    # Radios
    radio_names = scope.locator("input[type='radio'][name]").evaluate_all(
        "els => [...new Set(els.map(e => e.name))]"
    )
    for name in radio_names:
        base = name[:-2] if name.endswith(("_A", "_B")) else name
        preferred = RADIO_VALUES.get(base, RADIO_VALUES.get(name))
        if preferred is not None:
            selector = f"input[type='radio'][name='{name}'][value='{preferred}']"
            if page.locator(selector).count() > 0:
                try:
                    page.check(selector, force=True)
                    continue
                except Exception:
                    pass
        first = page.locator(f"input[type='radio'][name='{name}']").first
        if first.count() > 0:
            try:
                first.check(force=True)
            except Exception:
                try:
                    first.evaluate(
                        "el => { el.checked = true;"
                        " el.dispatchEvent(new Event('change', {bubbles:true})); }"
                    )
                except Exception:
                    pass


# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------

def next_button_locator(page):
    for selector in [
        "button.otree-btn-next",
        "button[type='submit']",
        "input[type='submit']",
        "button:has-text('Next')",
        "button:has-text('Continue')",
    ]:
        loc = page.locator(selector)
        if loc.count() > 0:
            return loc.first
    return None


def force_advance_form(page):
    try:
        page.evaluate("""
            () => {
                const form = document.querySelector('form');
                if (form) { form.submit(); return true; }
                const btn = document.querySelector(
                    'button.otree-btn-next, button[type="submit"], input[type="submit"]');
                if (btn) { btn.click(); return true; }
                return false;
            }
        """)
        return True
    except Exception:
        return False


def page_errors(page):
    """Validation messages oTree re-renders the page with."""
    try:
        texts = page.locator(".otree-form-errors, .form-control-errors").all_inner_texts()
    except Exception:
        return []
    return [t.strip().replace("\n", " ") for t in texts if t.strip()]


def click_next_and_wait(page, locator=None, timeout=10000):
    """Click the (oTree) next button. True only if we really left the page.

    A failed validation re-renders the same URL, which also fires a navigation
    event, so the URL - not the navigation - is what decides.
    """
    btn = locator if locator is not None else next_button_locator(page)
    if btn is None:
        return False
    url_before = page.url
    try:
        with page.expect_navigation(wait_until="domcontentloaded", timeout=timeout):
            btn.click()
    except PlaywrightTimeoutError:
        pass
    try:
        page.wait_for_load_state("domcontentloaded")
    except Exception:
        pass
    if page.url != url_before:
        return True
    # One retry through the form itself (custom in-page buttons, JS guards).
    force_advance_form(page)
    try:
        page.wait_for_url(lambda u: u != url_before, timeout=5000)
    except Exception:
        pass
    return page.url != url_before


# ---------------------------------------------------------------------------
# Screenshot capture
# ---------------------------------------------------------------------------

DEV_CHROME_SELECTORS = ".debug-info, #skipTestingBtn"


def hide_dev_chrome(page):
    """The devserver renders a debug panel under every page; keep it out of shot."""
    try:
        page.evaluate(
            "sel => document.querySelectorAll(sel)"
            ".forEach(el => { el.style.display = 'none'; })",
            DEV_CHROME_SELECTORS,
        )
    except Exception:
        pass


def capture(page, out_dirs, stem, taken):
    """Full-page screenshot (top to bottom) into every folder in out_dirs.

    full_page=True is what makes each file the whole oTree page from start to
    finish instead of just the part that happens to fit in the viewport.
    Already-written files are skipped, so the second participant does not
    redo the pages that have no A/B version.
    """
    hide_dev_chrome(page)
    source = None
    for out_dir in out_dirs:
        key = (out_dir.name, stem)
        if key in taken:
            continue
        target = out_dir / f"{stem}.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        if source is None:
            page.screenshot(path=str(target), full_page=True)
            source = target
        else:
            # Same page in both folders (welcome, survey, thanks): copy it.
            shutil.copyfile(source, target)
        taken.add(key)
        print(f"      + {out_dir.name}/{target.name}")


# ---------------------------------------------------------------------------
# Page handlers for the pages with pop-ups / in-page steps
# ---------------------------------------------------------------------------

def handle_wisdom_popup(page, out_dirs, step, label, taken):
    """E26 group B: fill the first estimates, open the overlay, shoot it, submit."""
    fill_fields(page)
    capture(page, out_dirs, file_stem(step, label), taken)

    page.locator("#secondGuessContinue").click()
    page.wait_for_timeout(400)

    overlay = page.locator("#secondGuessOverlay")
    if overlay.is_visible():
        capture(page, out_dirs, file_stem(step, label, "popup"), taken)
        # The second estimates live inside the overlay now.
        fill_fields(page, root=overlay)
        page.wait_for_timeout(150)
        url_before = page.url
        try:
            with page.expect_navigation(wait_until="domcontentloaded", timeout=15000):
                page.locator("#secondGuessDone").click()
        except PlaywrightTimeoutError:
            if page.url == url_before:
                force_advance_form(page)
        return page.url != url_before

    # Overlay did not open (e.g. validation): fall back to the normal next button.
    return click_next_and_wait(page)


def handle_insurance_steps(page, out_dirs, step, label, group, taken):
    """E32: group B walks through 4 in-page steps; group A is one page."""
    if group == "A":
        fill_fields(page)
        capture(page, out_dirs, file_stem(step, label), taken)
        return click_next_and_wait(page)

    for sub in range(1, 5):
        active = page.locator(f"#step-{sub}")
        if active.count() == 0:
            break
        if sub == 4:
            fill_fields(page)
        capture(page, out_dirs, file_stem(step, label, f"step{sub}"), taken)
        if sub < 4:
            nxt = active.locator("button:has-text('Next')").first
            if nxt.count() == 0:
                break
            nxt.click()
            page.wait_for_timeout(250)
    return click_next_and_wait(page)


def handle_investment(page, out_dirs, step, label, round_idx, taken, max_clicks=20):
    """E27-30: click through the chart years, then answer the revealed form.

    The chart is Highcharts loaded from a CDN, so the machine running this
    needs internet access or the chart area comes out blank.
    """
    try:
        page.wait_for_selector("#contr2 svg", timeout=8000)
        page.wait_for_timeout(400)
    except PlaywrightTimeoutError:
        print("      ! chart did not render (Highcharts CDN unreachable?)")
    capture(page, out_dirs, file_stem(step, label, f"round{round_idx}_chart"), taken)

    form_area = page.locator("#form-area")
    btn = page.locator("#updateChartButton")
    clicks = 0
    while clicks < max_clicks:
        try:
            if form_area.is_visible():
                break
            if btn.count() == 0 or not btn.is_visible():
                break
        except Exception:
            break
        btn.click()
        page.wait_for_timeout(250)
        clicks += 1

    if clicks:
        # Last chart state before the form takes over is worth keeping.
        capture(page, out_dirs, file_stem(step, label, f"round{round_idx}_chart_end"), taken)

    fill_fields(page)
    capture(page, out_dirs, file_stem(step, label, f"round{round_idx}_question"), taken)
    return click_next_and_wait(page)


# ---------------------------------------------------------------------------
# Per-participant runner
# ---------------------------------------------------------------------------

def report_stuck(page, label):
    print(f"      ! stuck on {label} ({page.url})")
    for err in page_errors(page)[:8]:
        print(f"        error: {err}")


def run_participant(page, participant_url, out_root, max_steps, taken):
    """Walk one participant from the welcome screen to the thanks page.

    Every page goes into the folder of the group this participant was given
    for that experiment; pages without an A/B version go into both, so each
    folder ends up holding the complete start-to-finish path.
    """
    page.on("dialog", lambda dialog: dialog.accept())
    page.goto(participant_url, wait_until="domcontentloaded")

    survey_seen = 0
    investment_round = 0
    step = 0

    for _ in range(max_steps):
        page.wait_for_load_state("domcontentloaded")
        kind, label, group = resolve_page(page, survey_seen)

        if kind == "survey":
            survey_seen += 1

        step += 1
        out_dirs = group_dirs(out_root, group)

        if kind == "thanks":
            capture(page, out_dirs, file_stem(step, label), taken)
            break

        if kind == "investment":
            investment_round += 1
            if not handle_investment(page, out_dirs, step, label,
                                     investment_round, taken):
                report_stuck(page, label)
                break
            continue

        if kind == "insurance":
            if not handle_insurance_steps(page, out_dirs, step, label, group, taken):
                report_stuck(page, label)
                break
            continue

        if label == EXPERIMENT_LABELS["WisdomofCrowd"] and group == "B":
            if not handle_wisdom_popup(page, out_dirs, step, label, taken):
                report_stuck(page, label)
                break
            continue

        # Plain page: fill, shoot, next.
        fill_fields(page)
        capture(page, out_dirs, file_stem(step, label), taken)

        if next_button_locator(page) is None:
            break
        if not click_next_and_wait(page):
            report_stuck(page, label)
            break


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url",     default=BASE_URL)
    parser.add_argument("--config",       default=SESSION_CONFIG_NAME,
                        help="session config name from settings.py")
    parser.add_argument("--participants", type=int, default=NUM_PARTICIPANTS,
                        help="2 is enough to get both the A and the B version")
    parser.add_argument("--max-steps",    type=int, default=MAX_STEPS)
    parser.add_argument("--out",          default=OUT_DIR)
    parser.add_argument("--randomize",    dest="randomize", action="store_true",
                        default=RANDOMIZE_ORDER,
                        help="keep the per-participant experiment shuffle")
    parser.add_argument("--no-randomize", dest="randomize", action="store_false",
                        help="fixed experiment order (default)")
    parser.add_argument("--headed",       action="store_true", default=HEADED)
    parser.add_argument("--no-headed",    dest="headed", action="store_false")
    args = parser.parse_args()

    out_root = Path(args.out)
    for group in GROUP_FOLDERS:
        (out_root / group).mkdir(parents=True, exist_ok=True)

    config_overrides = {
        # off, otherwise the "Skip for testing" button sits in every screenshot
        "testing": False,
        "randomize_experiment_order": args.randomize,
    }

    taken = set()  # (folder, file stem) pairs already written

    print(f"\n{'='*64}")
    print(f"  design_exp screenshot capture")
    print(f"  Output       : {out_root.resolve()}/{{{','.join(GROUP_FOLDERS)}}}")
    print(f"  Participants : {args.participants}   Headed: {args.headed}")
    print(f"  Order        : {'randomized' if args.randomize else 'fixed'}")
    print(f"{'='*64}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        setup_page = browser.new_page(viewport={"width": 1440, "height": 1100})

        print(f"Creating session with {args.participants} participants...")
        participant_links = create_session_and_get_links(
            page=setup_page,
            base_url=args.base_url,
            config_name=args.config,
            expected_links=args.participants,
            config_overrides=config_overrides,
        )
        setup_page.close()

        for idx, url in enumerate(participant_links, start=1):
            print(f"  [{idx}/{len(participant_links)}] participant {idx}")
            run_page = browser.new_page(viewport={"width": 1440, "height": 1100})
            run_participant(
                page=run_page,
                participant_url=url,
                out_root=out_root,
                max_steps=args.max_steps,
                taken=taken,
            )
            run_page.close()

        browser.close()

    print(f"\nDone - {len(taken)} screenshots in {out_root.resolve()}")
    for group in GROUP_FOLDERS:
        count = len([1 for folder, _ in taken if folder == group])
        print(f"  {group}/ : {count} pages")
        missing = [
            label for label in EXPERIMENT_LABELS.values()
            if not any(folder == group and label in stem for folder, stem in taken)
        ]
        if missing:
            print("    not captured (switched off in settings.py, or the run "
                  "stopped early):")
            for label in missing:
                print(f"      - {label}")
    print("\nBefore the next run:  otree resetdb")


if __name__ == "__main__":
    main()
