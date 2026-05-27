# Google Flow Prompt Generator

Streamlit app that builds professional cinematographic prompts for [Google Flow](https://labs.google/fx/tools/flow) video generation.

## Prompt formula

`[Shot Type + Camera Move]` → `[Subject]` → `[Environment]` → `[Lighting]` → `[Atmosphere]`

## Run locally

```bash
cd google-flow-helper
pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## Usage

1. Pick options in each of the five sections (or choose **Custom** to type your own).
2. Click **Generate Prompt** to assemble the full sentence.
3. Copy the output into Google Flow, or use **Download .txt**.

Quick presets (Cyberpunk Chase, Samurai Dawn, etc.) load a full example you can tweak.
