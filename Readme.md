# 🎬 AI-Based Movie Recommendation System

An interactive **content-based movie recommendation system** built with Python. The application recommends movies similar to a selected movie and provides additional information such as posters, ratings, genres, release year, and trailers.

## ✨ Features

* 🎯 Content-based movie recommendations
* 🔍 Movie search and selection
* 🎭 Genre-based filtering
* 📊 Similarity scores
* 🖼️ Movie posters and ratings
* 🎥 YouTube trailer integration
* 🔗 TMDB movie details
* 🌗 Day Mode & Neon Night Mode
* ⚡ Cached and concurrent API requests
* 📱 Responsive Streamlit interface

## 🧠 How It Works

```text
Select Movie
     ↓
Find Similar Movies
     ↓
Apply Genre Filter
     ↓
Rank by Similarity
     ↓
Fetch TMDB Details
     ↓
Display Recommendations
```

The system uses a precomputed movie similarity matrix to identify and rank movies similar to the selected movie. The application then retrieves additional movie information through the TMDB API.

## 🛠️ Tech Stack

* **Python**
* **Requests**
* **Pillow**
* **FPDF2**
* **python-dotenv**
* **TMDB API**
* **YouTube**

The project's dependencies are listed in `requirements.txt`.

## 📂 Project Structure

```text
AI-Movie-Recommendation-System/
│
├── app.py
├── movie_recom_sys.ipynb
├── movie_list.pkl
├── similarity.pkl
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Movie-Recommendation-System.git
cd AI-Movie-Recommendation-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure TMDB API

Create a `.env` file:

```env
TMDB_API_KEY=your_api_key_here
```

**Do not upload `.env` or expose your API key on GitHub.** The project already excludes `.env` through `.gitignore`.

### 5. Run the application

```bash
streamlit run app.py
```

## 🔮 Future Improvements

* 🤖 Hybrid recommendation system
* 👤 Personalized user profiles
* ❤️ Favorites and watchlists
* ⭐ User ratings
* 🔐 Authentication
* 📊 Recommendation evaluation metrics
* 🌐 Online deployment
* 🗄️ Database integration

## 🎓 Skills Demonstrated

**Recommendation Systems • Content-Based Filtering • Python • Streamlit • REST APIs • Data Processing • API Integration • UI Development • Concurrent Programming**

## 👩‍💻 Author

**Avani Mahendrakar**

Third-Year Artificial Intelligence & Machine Learning Student

---

⭐ If you find this project useful, consider giving it a star!
