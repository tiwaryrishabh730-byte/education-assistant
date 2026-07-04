**Scribe AI: A Pedagogical Multi-Agent Framework**

A **"Learning by Building"** Project

Hi, my name is Rishabh Tiwary. I am currently a 2nd year B.Tech student studying Artificial Intelligence. I built Scribe AI not as a commercial product, but as an engineering sandbox to deeply understand how Large Language Models (LLMs) and agentic workflows actually operate under the hood.

While using standard AI chatbots to study, I realized they often act as "answer dispensers" rather than actual teachers. You copy the answer, it works, but you don't learn the fundamental concepts. I wanted to build a system that forces the AI to act as a structured, pedagogical tutor—explaining the why using real-world analogies, rather than just the what.

 **The Architecture**
 
To solve the "answer dispenser" problem, I moved away from a single, unpredictable prompt and built a modular multi-agent pipeline. This taught me how to pass structured data between distinct functions:

**The Sanitizer Agent**: Takes raw, often messy user input and normalizes it into a clear, actionable query.

**The Explainer Agent** (The Core): Takes the sanitized prompt and generates an explanation explicitly designed to use real-world analogies (avoiding dry textbook definitions).

**The Evaluator (QA) Agent**: Reviews the explainer's output to ensure it is factually accurate and pedagogically sound before passing it to the user interface.

 **Tech Stack**
**Language**: Python

**Framework**: FastAPI

**Orchestration**: Google Gemini API

**Package Management**: uv

 **Note to Judges: Local Setup Instructions**
 
Thank you for taking the time to review my code. Because this project is focused on foundational engineering and data flow, I have opted for a stable local deployment rather than a fragile cloud host.

To ensure the security of my credentials, the .env file containing the API key has been strictly excluded from this repository via .gitignore. Please follow these instructions to run the framework on your local machine.

**Prerequisites**

Python 3.10 or higher installed.

uv installed on your system.

Your own Google Gemini API Key.

**Step-by-Step Execution**

1. Clone the repository:


git clone https://github.com/tiwaryrishabh730-byte/education-assistant.git
cd scribe-ai

2. Configure the environment variables:

Create a new file named .env in the root directory and add your API key:


GEMINI_API_KEY=your_actual_api_key_here

3. Sync Dependencies:

Install the required packages using uv:

uv sync

4. Start the Server:

Run the FastAPI application:


uv run uvicorn app.fast_api_app:app --host 127.0.0.1 --port 8000 --reload

5. Access the Interface:

Once the terminal displays Application startup complete, open your web browser and navigate to:

http://127.0.0.1:8000

 **How to test the architecture**
 
When you submit a query in the UI, I highly recommend clicking on the "Traces" tab. This will expose the internal logging, allowing you to see exactly how the data moves from the Sanitizer, to the Explainer, and finally to the Evaluator.

 **Final Reflection**
 
Building Scribe AI locally pushed me to learn crucial development practices that aren't always covered in early university courses—from managing secure environment variables to resolving Git merge conflicts and orchestrating async API calls. Thank you for evaluating my journey into AI engineering.
