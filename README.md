# Akamai Security Configuration Analyzer

A powerful tool built with Streamlit and Agno that analyzes Akamai security configurations against predefined and custom security rules using AI models (GPT-4 and Gemini Pro).

## Features

- 🔒 Automated security analysis of Akamai configurations
- 🤖 Support for multiple AI models (GPT-4 and Gemini Pro)
- ✨ Built-in security rules for common configurations
- ➕ Custom rule addition capability
- 📊 Detailed security analysis reports
- 🎯 Rule-by-rule assessment
- 💡 Actionable recommendations

## Default Security Rules

- WAF configuration validation
- Rate limiting verification
- Geo-blocking configuration check
- TLS version validation
- Bot management review
- DDoS protection confirmation

## Prerequisites

- Python 3.8+
- OpenAI API key (for GPT-4) or Google API key (for Gemini Pro)
- Akamai configuration in JSON format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shadsidd/akamai-config-validator.git
cd akamai-config-validator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run akamai-config.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. In the sidebar:
   - Select your preferred AI model (GPT-4 or Gemini Pro)
   - Enter your API key

4. Upload your Akamai configuration JSON file

5. (Optional) Add custom security rules for evaluation

6. Click "Analyze Configuration" to generate a detailed security report

## Output

The analysis provides:
- Overall security score
- Detailed assessment of each security rule
- Critical security findings
- Specific recommendations for improvements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created by Shadab

## Support

For support, please open an issue in the GitHub repository.