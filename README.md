# Clinical Scenario Simulator

Standalone interactive simulator for clinical scenarios. Reviewers can walk through generated scenarios step-by-step, make clinical decisions, and receive performance feedback.

## Quick Start

# Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

# Install dependencies
```bash
pip install -r requirements.txt
```

# Run the app
```bash
streamlit run app.py
```

## Adding Scenarios

**Bundled scenarios:** Drop `.json` scenario files into the `scenarios/` folder. They will appear automatically in the scenario selector.

**Upload:** Use the file uploader in the app to load scenario JSON files on the fly.

No API keys or cloud services needed — everything runs client-side.

## Project Structure

```
app.py                  # Main application
scenario_viewer.py      # Simulation UI components
theme.py                # Visual styling
scenarios/              # Bundled scenario JSON files
requirements.txt        # Python dependencies
```
