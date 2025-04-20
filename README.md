```markdown
# Roo Code × Perplexity AI Browser Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## 1. Overview

This project provides a robust system for integrating Perplexity AI's browser version with Roo Code. It utilizes Selenium for browser automation, allowing users to send prompts to Perplexity and receive formatted answers directly within their Roo Code environment.

The core philosophy emphasizes reliability and maintainability through a state machine-driven architecture, detailed error handling, and a test-driven development approach. This system aims to streamline research and information gathering workflows by automating interactions with Perplexity AI.

**Key Features:**

*   **Direct Prompting:** Send questions or instructions to Perplexity AI from Roo Code.
*   **Structured Output:** Receive formatted answers including citations and related questions in JSON format.
*   **Focus Mode & Options:** Specify Perplexity's search focus (Web, Academic, Writing, etc.) and other options like response length.
*   **Automated Browser Interaction:** Uses Selenium and Firefox to interact with `perplexity.ai` in the background (headless mode supported and recommended).
*   **Session Persistence:** Maintains browser sessions using Redis for faster consecutive queries.
*   **State Machine Control:** Manages the entire process flow reliably using a finite state machine.
*   **Robust Error Handling:** Implements multi-layered error detection and automated recovery strategies.
*   **Configuration Driven:** Browser behavior and element selectors are managed via external configuration files.

## 2. Technical Stack

| Component           | Technology            | Version | Notes                               |
| :------------------ | :-------------------- | :------ | :---------------------------------- |
|---------------------|-----------------------|---------|---------------------------------------|
| Language            | Python                | 3.11.2+ |                                     |
| Browser Automation  | Selenium              | 4.15.2  | For controlling the browser         |
| Browser             | Firefox               | 128.0+  | Target browser for automation       |
| Session Management  | Redis                 | 7.2.3+  | For persisting browser sessions     |
| Configuration       | Pydantic              | 2.6.1   | For settings validation             |
|                       | TOML                  |         | For `settings.toml`               |
| HTML Parsing        | BeautifulSoup4        | Latest  | For extracting data from responses  |
| Markdown Conversion | Markdownify           | Latest  | For converting HTML response parts  |
| Logging             | structlog             | 23.1.0  | For structured logging              |
| Testing Framework   | pytest                | 8.0.2   | For unit, integration, E2E tests    |
| Code Formatting     | black, isort          | Latest  |                                     |
| Linting             | flake8                | Latest  |                                     |
| Type Checking       | mypy                  | Latest  |                                     |

## 3. Prerequisites

*   **Python:** Version 3.11.2 or higher.
*   **Firefox:** Version 128.0 or higher installed.
*   **Redis:** A running Redis server (defaults to `localhost:6379`).
*   **Git:** For cloning the repository.
*   **pip & venv:** For package management and virtual environments.

## 4. Installation

1.  **Clone the Repository:**
    ```
    git clone  # Replace  with the actual URL
    cd roo-perplexity
    ```

2.  **Create and Activate Virtual Environment:**
    ```
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```
    *(Note: Ensure `requirements.txt` includes all packages listed in the Technical Stack)*

4.  **Configure Settings:**
    *   Copy the example configuration files:
        ```
        cp config/settings.toml.example config/settings.toml
        cp config/selectors.json.example config/selectors.json
        ```
    *   Edit `config/settings.toml` to match your environment (especially Redis host/port if not default, and potentially Firefox path if needed).
    *   Review `config/selectors.json`. These are CSS selectors used to find elements on `perplexity.ai`. Update them *only* if Perplexity changes its website structure significantly.

## 5. Configuration
### 5.1 `config/settings.toml`

This file controls the core behavior of the browser automation and session management.


[selenium]
# Browser type (currently only "firefox" is fully supported)
browser = "firefox"
# Run browser without UI (true recommended for production/normal use)
headless = true
# Default timeout in seconds for waiting for elements
timeout = 30
# User agent string to mimic a real browser
user_agent = "Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0"
# Optional: Specify Firefox binary path if not in default location
# firefox_binary_path = "/path/to/firefox"

[redis]
# Redis server hostname or IP address
host = "localhost"
# Redis server port
port = 6379
# Session Time-To-Live in seconds (e.g., 28800 = 8 hours)
session_ttl = 28800
```

### 5.2 `config/selectors.json`

This file contains CSS selectors to locate key elements on the Perplexity AI website. **Modify with caution**, as incorrect selectors will break the automation.

```
{
  "input_field": "textarea[data-testid='perplexity-input']", // Input area for the prompt
  "submit_button": "button[aria-label='Ask']",             // Button to submit the prompt
  "answer_container": "div.answer-content",              // Main container holding the answer
  "citation_links": "a.citation-link",                  // Links for citations within the answer
  // Add other selectors as needed, e.g., for focus mode buttons
}
```

## 6. Usage

This library is intended to be used programmatically, typically integrated into the Roo Code extension. The primary entry point is likely the `main.py` script or specific functions/classes imported from the `core` modules.

### 6.1 Sending a Prompt

Prompts are sent as JSON objects adhering to the defined schema.

1.  **Prepare the Input JSON:**
    ```
    {
      "prompt": "Explain the theory of relativity in simple terms.",
      "focusMode": "Academic", // Optional: Web, Academic, Writing, Math, Video, Social
      "options": {            // Optional
        "maxLength": 500     // Optional: Desired max length (informational, Perplexity might not strictly adhere)
      }
    }
    ```

2.  **Invoke the Processing Function/Script:**
    (This depends on the final implementation of `main.py` or the exposed API)
    ```
    # Example using a potential command-line interface via main.py
    python main.py --input '{"prompt": "...", "focusMode": "Web"}'
    ```
    Or programmatically:
    ```
    # Assuming an entry point function `process_perplexity_query` exists
    from main import process_perplexity_query # Fictional entry point

    input_data = {
      "prompt": "Explain the theory of relativity in simple terms.",
      "focusMode": "Academic"
    }
    result_json = process_perplexity_query(input_data)
    print(result_json)
    ```

### 6.2 Receiving the Output

The system returns a JSON object containing the processed response.

*   **Output Format (JSON Schema):**
    ```
    {
      "type": "object",
      "properties": {
        "answer": { "type": "string", "description": "AI's generated answer text" },
        "citations": {
          "type": "array",
          "items": { "type": "string", "format": "uri", "description": "Source URLs" }
        },
        "relatedQuestions": {
          "type": "array",
          "items": { "type": "string", "description": "Suggested follow-up questions" }
        }
      },
      "required": ["answer"]
    }
    ```
*   **Example Output:**
    ```
    {
      "answer": "The theory of relativity, developed by Albert Einstein, fundamentally changed our understanding of space, time, gravity...",
      "citations": [
        "https://example.com/einstein-bio",
        "https://physics.org/relativity-explained"
      ],
      "relatedQuestions": [
        "What is the difference between special and general relativity?"
      ]
    }
    ```

## 7. Project Structure

```
roo-perplexity/
├── config/                 # Configuration files
│   ├── settings.toml       # Main application settings (Selenium, Redis)
│   └── selectors.json      # CSS selectors for Perplexity website elements
├── core/                   # Core application logic
│   ├── browser_control/    # Selenium WebDriver management and browser actions
│   │   ├── driver_manager.py # Initializes and manages the WebDriver instance
│   │   └── element_locators.py # Logic for finding elements based on selectors.json
│   ├── session_handling/   # Browser session persistence
│   │   ├── redis_client.py   # Redis connection and operations
│   │   └── cookie_handler.py # Saving/loading session cookies via Redis
│   ├── processing/         # Handling prompts and parsing responses
│   │   ├── prompt_processor.py # Validates and prepares prompts
│   │   └── response_parser.py  # Extracts information from Perplexity's HTML response
│   └── state_machine/      # Finite State Machine for controlling workflow
│       ├── states.py         # Defines possible system states (Enum)
│       └── transitions.py    # Defines rules for state transitions
├── tests/                  # Automated tests
│   ├── unit/               # Unit tests for individual components (mocked dependencies)
│   ├── integration/        # Tests for component interactions (e.g., Redis connection)
│   └── e2e/                # End-to-end tests simulating full user workflow
├── utils/                  # Utility functions and classes
│   ├── logger.py           # Structured logging setup (structlog)
│   └── error_handler.py    # Defines custom exceptions and error handling logic
├── main.py                 # Main entry point for the application/script
├── requirements.txt        # Python package dependencies
└── README.md               # This file
```

## 8. Error Handling

The system includes mechanisms to handle common errors:

*   **Element Not Found:** Often caused by changes in Perplexity's website structure. The system attempts retries with potentially updated selectors (if implemented) or notifies the user. Check `config/selectors.json` if this persists.
*   **Timeout:** Perplexity taking too long to respond, or slow network. Check network connection or increase `selenium.timeout` in `config/settings.toml`.
*   **Network Error:** Issues connecting to Perplexity or Redis. Verify network connectivity and Redis server status.
*   **Rate Limit:** Accessing Perplexity too frequently. The system has internal limits (e.g., 3 queries/min), but excessive use might still trigger blocks. Wait before retrying.
*   **Initialization Error:** Problems starting the browser or navigating to Perplexity. Ensure Firefox is installed correctly and WebDriver setup is functional.

Logs generated by `structlog` (check `utils/logger.py` for configuration) provide detailed information for troubleshooting.

## 9. Testing

Tests are crucial for ensuring reliability, especially given the dependency on an external website.

*   **Run Tests:**
    ```
    pytest tests/
    ```
*   **Run Tests with Coverage:**
    ```
    pytest --cov=core --cov-report=term-missing tests/
    ```
*   **Test Types:**
    *   **Unit Tests (`tests/unit`):** Isolate and test individual functions/classes using mocks.
    *   **Integration Tests (`tests/integration`):** Test interactions between components (e.g., session handler and Redis).
    *   **End-to-End Tests (`tests/e2e`):** Run the full workflow using a real (or mock) browser and potentially a mock Perplexity website or controlled interaction.

## 10. Contributing

Contributions are welcome! Please follow these guidelines:

1.  **Branching:** Use Gitflow ( `develop`, `feature/xxx`, `fix/xxx`). Create feature branches off `develop`.
2.  **TDD:** Write tests *before* writing implementation code (Red-Green-Refactor).
3.  **Code Style:** Adhere to PEP 8. Use `black`, `isort`, and `flake8` (configurations likely provided).
4.  **Type Hinting:** Use Python type hints extensively and check with `mypy`.
5.  **Commits:** Follow Conventional Commits format (e.g., `feat:`, `fix:`, `refactor:`, `test:`).
6.  **Pull Requests:** Submit PRs from your feature branch to `develop`. Ensure all tests pass and include a clear description of changes. Require at least one reviewer approval.

## 11. License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## 12. Important Disclaimers

*   **Unofficial:** This is an unofficial tool and is not affiliated with or endorsed by Perplexity AI.
*   **Website Changes:** This tool relies on the current structure of the `perplexity.ai` website. Changes to their site **will likely break** this tool, requiring updates to the selectors (`config/selectors.json`) and potentially the core logic. Use at your own risk.
*   **Terms of Service:** You are responsible for complying with Perplexity AI's Terms of Service, including any restrictions on automated access. Excessive use may lead to your IP being blocked.

## 13. Running Tests

To run the tests, use the following command:

```
pytest tests/
```

## 14. Contributing

Contributions are welcome! Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Write tests for your changes.
4.  Make sure all tests pass.
5.  Submit a pull request.
```

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/7a04f025-5e90-4e97-91a8-65d9eeccdacc/ref1.md
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/0438d1f4-0a20-492c-ae44-231851b45610/ref2.md
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/4e72129b-ec12-4a84-a17e-7e7333e34635/ref3.md
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/c7658b29-9f0a-4ef7-bc8f-cae9718cb6a0/Quan-Ti-She-Ji.md
[5] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/74cb3edf-94a1-4918-9745-6350563c4d00/She-Ji-Yao-Jian.md
[6] https://github.com/HTTPS-Miner/perplexity-ai
[7] https://mikelev.in/futureproof/agentic-frameworks-vs-browser-automation/
[8] https://news.ycombinator.com/item?id=42388783
[9] https://github.com/Arbaaz-Mahmood/Perplexity-API
[10] https://github.com/letsbuildagent/perplexity-tool/blob/main/README.md
[11] https://github.com/taishi-i/awesome-ChatGPT-repositories/blob/main/docs/README.en.md
[12] https://www.reddit.com/r/ChatGPT/comments/12580m9/create_your_own_custom_plugins_for_chatgpt_browse/
[13] https://aclanthology.org/2025.chipsal-1.pdf
[14] https://yanggggjie.github.io/rising-repo/
[15] https://github.com/allotmentandy/Awesome-perplexity.ai
[16] https://marketplace.visualstudio.com/sitemap.xml
[17] https://ai-rockstars.com/claude-ai-api-tutorial/
[18] https://techpoint.africa/2025/01/30/my-perplexity-ai-review/
[19] https://journal.esrgroups.org/jes/article/download/7091/4888/13029
[20] https://mcp.so/en/server/mcp-server/Yangbin-v
[21] https://www.linkedin.com/posts/mrtayyabmughal_github-tayyabmughal676f1gptbackend-formula-activity-7260713812071235585-ib61
[22] https://mcp.so/en/server/test-mcp-servers-in-vs-code/F88
[23] https://github.com/jasonkneen/Roo-Code
[24] https://huggingface.co/datasets/togethercomputer/llama-instruct/viewer/default/train
[25] https://www.youtube.com/watch?v=OT7XvazhHgE

---
Perplexity の Eliot より: pplx.ai/share# RooBrawser
