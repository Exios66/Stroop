# Stroop Task V3

This is an enhanced version of the Stroop Task, incorporating personality traits, emotion recognition, and adaptive responses.

## Setup Instructions

1. Ensure you have Python 3.7 or later installed on your system.

2. Clone this repository or download the files to your local machine.

3. Open a terminal/command prompt and navigate to the project directory.

4. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

5. Activate the virtual environment:
   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

6. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

7. Download the spaCy English language model:

   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Stroop Task

To run the Stroop Task, execute the following command in your terminal:

```bash
python StroopV3.py
```

Follow the on-screen instructions to complete the task.

## Features

- Classic Stroop Task implementation
- Personality traits that influence the task's behavior
- Emotion recognition based on user input
- Adaptive responses generated based on personality and emotions
- Dynamic personality adjustment based on performance

## File Descriptions

- `StroopV3.py`: The main Python script containing the Stroop Task implementation.
- `requirements.txt`: List of Python packages required for this project.
- `README.md`: This file, containing setup instructions and project information.

## Troubleshooting

### Missing Dependencies or Import Errors

If you encounter issues with missing dependencies or import errors, especially with the `transformers` library, follow these steps:

1. Ensure you're in the project's virtual environment (if you created one).

2. Update pip to the latest version:

   ```bash
   pip install --upgrade pip
   ```

3. Reinstall the requirements:

   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

4. If you're still experiencing issues, try installing the transformers library separately:

   ```bash
   pip install transformers torch
   ```

5. If the problem persists, please check your Python version and ensure it's compatible with the latest version of the transformers library.

For any other problems or questions, please open an issue in this repository.

Enjoy the enhanced Stroop Task experience!