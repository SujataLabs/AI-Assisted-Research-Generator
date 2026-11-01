
import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Check API key
if not API_KEY or API_KEY == "PASTE_YOUR_COPIED_KEY_HERE":
    print("Error: Please add your actual Gemini API key in the .env file.")
    raise SystemExit

# Connect to Gemini
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-flash-latest"


def get_user_input():
    print("\n======================================")
    print("   AI-ASSISTED RESEARCH GENERATOR")
    print("======================================")

    domain = input("\nEnter Subject Domain: ").strip()
    keywords = input("Enter Research Keywords: ").strip()
    interest = input("Enter Research Interest: ").strip()

    if not domain or not keywords or not interest:
        print("\nError: Please fill in all three fields.")
        return None

    return domain, keywords, interest


def generate_research(domain, keywords, interest):

    prompt = f"""
Act as an academic research assistant.

Analyse the following research information:

Subject Domain: {domain}
Research Keywords: {keywords}
Research Interest: {interest}

Generate the following information:

1. RESEARCH AREAS
Identify five relevant research areas.

2. INTERDISCIPLINARY RESEARCH TOPICS
Suggest four research topics and mention the disciplines
involved in each topic.

3. RESEARCH OBJECTIVES
Develop three clear and meaningful research objectives.

4. PRELIMINARY RESEARCH OUTLINE
Include:
- Research Title
- Background
- Problem Statement
- Research Questions

5. RESEARCH METHODOLOGY
Recommend a suitable methodology including:
- Research Design
- Data Collection Techniques
- Target Population
- Data Analysis Methods

6. EXPECTED OUTCOMES AND CONTRIBUTIONS
Explain the possible expected outcomes and contributions
of the proposed research.

Use simple, formal academic English.
Organize the answer under clear headings.
Keep the suggestions relevant to the user's research interest.
Do not invent research findings or claim that the research
has already been conducted.
"""

    try:
        print("\nConnecting to Google Gemini...")
        print("Generating research suggestions. Please wait...\n")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response.text:
            print("No text was returned. Please try again.")
            return

        result = response.text

        print("\n" + "=" * 65)
        print("           GENERATED RESEARCH SUGGESTIONS")
        print("=" * 65)
        print(result)
        print("\n" + "=" * 65)

        save_output(result, domain, keywords, interest)

    except Exception as error:
        print("\nAn error occurred while connecting to Gemini.")
        print("Error details:", error)


def save_output(result, domain, keywords, interest):

    filename = "research_output.txt"

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("AI-ASSISTED RESEARCH GENERATOR\n")
            file.write("=" * 60 + "\n\n")

            file.write("Subject Domain: " + domain + "\n")
            file.write("Research Keywords: " + keywords + "\n")
            file.write("Research Interest: " + interest + "\n")

            file.write("\nGenerated On: ")
            file.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

            file.write("\n\n" + "=" * 60 + "\n")
            file.write("GENERATED RESEARCH CONTENT\n")
            file.write("=" * 60 + "\n\n")

            file.write(result)

        print("\nResearch suggestions saved successfully!")
        print("File name:", filename)

    except OSError as error:
        print("\nUnable to save output:", error)


def main():

    user_details = get_user_input()

    if user_details is None:
        return

    domain, keywords, interest = user_details

    generate_research(domain, keywords, interest)


if __name__ == "__main__":
    main()
