# Project Newz | SLOTH NEWS

**Project Newz** is an AI-powered news generation and aggregation platform built with **Python and Flask**.

It automatically collects news, generates AI-powered summaries and classifications, creates AI-generated article images, and stores the resulting articles in Supabase.

The platform features a newsroom-style interface under the **SLOTH NEWS** identity, providing news discovery, topic-based sections, market information, weather updates, and individual article pages.

## Features

### News Automation & AI
- 📰 Automated news scraping and aggregation.
- 🤖 AI-generated article summaries.
- 🏷️ Automated article classification.
- 🖼️ AI-generated article images.
- 🔄 Daily automated news generation.
- 📄 Individual article pages.

### News Discovery
- 🔎 Article search functionality.
- 🏷️ Tag-based filtering.
- 🌍 Dedicated news sections and topic-based discovery.
- 📈 Financial Intelligence Desk.
- 🔥 Trending Topic Desks.

### Newsroom Interface
- 📰 Redesigned SLOTH NEWS newsroom interface.
- 🚨 Breaking news ticker.
- 📊 Market index displays.
- 🌤️ Weather information.
- 🏢 Dedicated Bureau (About Us) section.
- 📖 Newsroom Charter and Mission.
- 🏛️ Institutional Governance information.

### Backend & Infrastructure
- 🗄️ Supabase database and storage.
- 🔐 Password-protected pipeline.
- 🌐 Flask web application.
- ⚙️ Automated news pipeline.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database & Storage | Supabase |
| Text AI | OpenRouter, Llama 3.1 8B |
| Image AI | Cloudflare AI, `@cf/lykon/dreamshaper-8-lcm` |
| Frontend | HTML, CSS, JavaScript |
| Automation | GitHub Actions |

## Project Structure

```text
Project-Newz/
│
├── app.py
├── requirements.txt
├── .env
│
├── services/
│   ├── supabase_client.py
│   ├── llm_utils.py
│   └── finance_llm.py
│
├── agent/
│   ├── scraper_agent.py
│   ├── summarizer_agent.py
│   └── classifier_agent.py
│
├── image_generation/
│   ├── upload_image_to_supabase.py
│   ├── image_generate.py
│   └── lib.py
│
├── route/
│   └── route.py
│
├── templates/
└── static/
```

## News Pipeline

```text
News Sources
     ↓
Scraper Agent
     ↓
Summarizer Agent
     ↓
Classifier Agent
     ↓
Supabase Database
     ↓
AI Image Generation
     ↓
Supabase Storage
     ↓
SLOTH NEWS Website
```

The news pipeline automatically runs daily and generates **4 articles per run**.

## Bureau & Mission

SLOTH NEWS operates under the institutional identity of **Sloth News Network (SNN)**.

Its newsroom charter is built around three journalistic pillars:

1. **Accuracy First:** Cross-verification of information.
2. **Signal Over Noise:** Concise executive briefs.
3. **Zero Conflicts:** Editorial independence.

Sloth News operates as the public media and intelligence division of **Triarc and Thinker**.

The Bureau section provides further information about the platform's mission, journalistic principles, technology and institutional governance.

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Project-Newz
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token

OPENROUTER_API_KEY=your_openrouter_api_key

PIPELINE_PASSWORD=your_pipeline_password
```

**Never commit your `.env` file.**

### 5. Run the application

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

## Running the Pipeline

Running the pipeline manually requires the configured pipeline password.

The pipeline:

1. Scrapes news articles.
2. Generates summaries using OpenRouter and Llama 3.1 8B.
3. Classifies the articles.
4. Stores article data in Supabase.
5. Generates article images using Cloudflare AI.
6. Uploads images to Supabase Storage.

The automated pipeline runs daily and generates four articles per run.

## Changelog

The project has evolved through multiple versions, introducing AI image generation, automated news processing, search and filtering functionality, and a redesigned newsroom interface.

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## License

Project Newz is licensed under the [MIT License](LICENSE).