# AI Resume Matcher

A Streamlit app that uses OpenAI's GPT-3.5-turbo to analyze and match resumes against job descriptions, then generates a PDF report.

## Features

- Upload `.docx` resumes
- Paste job descriptions
- Anonymizes personal data
- Provides match score, strengths, skill gaps, and suggestions
- Downloadable PDF report

## How to Run

1. **Clone the repository**

    ```bash
    git clone https://github.com/your-username/resume-matcher.git
    cd resume-matcher
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set your OpenAI API key**

    - For **macOS/Linux**:

        ```bash
        export OPENAI_API_KEY="your_api_key_here"
        ```

    - For **Windows PowerShell**:

        ```powershell
        $env:OPENAI_API_KEY="your_api_key_here"
        ```

4. **Run the app**

    ```bash
    streamlit run app.py
    ```



## Requirements
   See `requirements.txt` for dependencies.

   If you have a virtual environment, you can generate this automatically by running:
   ```bash
   pip freeze > requirements.txt
   ```

## License
   MIT License

## Author
   Ambika Narayanan
   Feel free to connect or contribute!

