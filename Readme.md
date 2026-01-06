# 🎬 AI-Movie Recommending System

A visually stunning **IMDB-style movie recommendation dashboard** built with Streamlit.  
Features **neon night mode, posters, ratings, genre badges, YouTube trailer embeds**, and responsive layout.

## Features
- Content-based movie recommendations
- IMDB-style cards with posters, ratings, and similarity scores
- Neon-themed night/day mode toggle
- Embedded YouTube trailers
- Genre filters
- Responsive and mobile-friendly layout

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Movie Recommending System.git
cd AI-Movie Recommending System
Create a virtual environment:

bash
Copy code
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Add your TMDB API key:

bash
Copy code
echo "TMDB_API_KEY=your_api_key_here" > .env
Run the app:

bash
Copy code
streamlit run app.py