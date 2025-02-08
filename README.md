# AI Travel Agent

This project is an AI Travel Agent that allows users to upload their yearly calendar files (PDF, ICS, or CSV), automatically parses the events, flags weekends as holidays, and provides vacation recommendations using the OpenAI API.

## Project Structure
ai_travel_agent/ ├── app.py # Main Streamlit application ├── database.py # Database models and initialization (SQLite with SQLAlchemy) ├── file_parser.py # Functions to parse calendar files (PDF, ICS, CSV) ├── llm_agent.py # OpenAI API integration with .env support ├── requirements.txt # Python dependencies ├── .env # Environment variables (contains OPENAI_API_KEY) └── README.md # Project documentation and instructions
