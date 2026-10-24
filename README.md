# DataLab Academy — Prototype v0.1

A combined educational web app for KS3/KS4 learners and teachers:
- DataLab Classroom: upload CSV files, calculate summary statistics, explore charts and answer a basic question.
- Data Detective Academy: solve a fictional school sports mystery with evidence, a verdict and prototype scoring.
- Teacher Guide: suggested objectives and lesson sequence.

## Requirements
- Python 3.10 or newer recommended
- Internet connection for first-time package installation

## Run locally

1. Unzip the project.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment (recommended):

   Windows:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:
   ```bash
   streamlit run app.py
   ```

6. Open the local address Streamlit prints in the terminal (usually http://localhost:8501).

## Current limitations
- This is an MVP prototype, not a production school platform.
- No student accounts, teacher/class administration, cloud storage or payment processing.
- Case scoring is rule-based and does not assess the quality of written reasoning.
- CSV uploads are processed for the current session; avoid uploading personal or identifiable pupil data.
- Validate all outputs before using the app for formal assessment.
