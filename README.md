# Clinical Scenario Simulator

Standalone interactive simulator for clinical scenarios. Reviewers can walk through generated scenarios step-by-step, make clinical decisions, and receive performance feedback.

## Quick Start

```bash
cd standalone_simulator
pip install -r requirements.txt
streamlit run app.py
```

## Adding Scenarios

**Bundled scenarios:** Drop `.json` scenario files into the `scenarios/` folder. They will appear automatically in the scenario selector.

**Upload:** Use the file uploader in the app to load scenario JSON files on the fly.

## Deploy to Streamlit Cloud

1. Push this `standalone_simulator/` folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Point it to `app.py` in the repository
4. Deploy

No API keys or cloud services needed — everything runs client-side.

## Deploy to Hugging Face Spaces

1. Create a new Space with the Streamlit SDK
2. Upload the contents of this folder
3. Done

## Project Structure

```
app.py                  # Main application
scenario_viewer.py      # Simulation UI components
theme.py                # Visual styling
scenarios/              # Bundled scenario JSON files
requirements.txt        # Python dependencies
```
