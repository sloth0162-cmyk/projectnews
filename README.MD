# Project Newz | SLOTH NEWS

**Project Newz** is an AI-powered news generation and aggregation platform built with Python and Flask.

It automatically collects news, generates AI-powered summaries and classifications, creates AI-generated article images, and stores the resulting articles in Supabase.

The platform features a newsroom-style interface under the **SLOTH NEWS** identity, providing news discovery, topic-based sections, market information, weather updates, individual article pages, and authenticated reader accounts.

## Features

### News Automation & AI

- 📰 Automated news scraping and aggregation.
- 🤖 AI-generated article summaries.
- 🏷️ Automated article classification and tagging.
- 🖼️ AI-generated article images using Cloudflare Workers AI.
- 🔄 Automated daily news generation through GitHub Actions.
- 📄 Individual article pages.
- 📈 Dedicated finance news generation pipeline.
- 🗄️ Supabase database and image storage integration.

### News Discovery

- 🔎 Article search functionality.
- 🏷️ Tag-based filtering.
- 🌍 Dedicated news sections and topic-based discovery.
- 📈 Financial Intelligence Desk.
- 🔥 Trending Topic Desks.
- 📰 Individual article pages.

### Reader Accounts & Authentication

- 🔐 Google sign-in through Supabase Auth.
- 👤 Reader Profile page with account information and profile management.
- ✏️ Persistent profile name updates through Supabase Auth.
- 🚪 Account logout and session management.
- 🔑 Flask session integration with the navigation system.
- 📱 Authentication compatibility across desktop and Android.
- 📖 Subscriber Center page for signed-out readers.
- 🧭 Account-aware navigation with separate signed-in and signed-out states.

### Newsletter Subscriptions

- 📧 Newsletter subscription form integrated into the website footer.
- 🗄️ Email subscription storage through Supabase.
- 🔄 Duplicate subscription detection and subscriber reactivation.
- 🔔 Subscription success and error notifications.

The current newsletter system handles subscription management and email storage. Automated newsletter email delivery is not yet implemented.

### Newsroom Interface

- 📰 SLOTH NEWS newsroom-style interface.
- 🚨 Breaking news ticker.
- 📊 Live market information, including Reliance stock data.
- 🌤️ Dynamic, city-based weather information.
- 🏢 Dedicated Bureau (About Us) section.
- 📖 Newsroom Charter and Mission.
- 🏛️ Institutional Governance information.
- ⏳ Global loading animation.
- 📱 Responsive layouts across desktop and mobile devices.

### Backend & Infrastructure

- 🗄️ Supabase database, authentication, and storage.
- 🔐 Password-protected pipeline execution.
- 🌐 Flask web application with modular authentication routes.
- ⚙️ Automated news and finance pipelines.
- 🔄 GitHub Actions automation.
- 🔒 Flask session-based reader authentication.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database & Storage | Supabase |
| Authentication | Supabase Auth, Google OAuth, Flask sessions |
| Text AI | OpenRouter, Llama 3.1 8B |
| Image AI | Cloudflare Workers AI, `@cf/black-forest-labs/flux-1-schnell` |
| Frontend | HTML, CSS, JavaScript, Tailwind CSS |
| Market Data | Indian stock market API |
| Automation | GitHub Actions |
| Deployment | Vercel |

## Project Structure

```text
Project-Newz/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── auth/
│   ├── __init__.py
│   └── auth.py
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
├── market/
│   └── livestockapi.py
│
├── route/
│   └── route.py
│
├── templates/
│   ├── profile.html
│   ├── subscriber.html
│   └── ...
│
├── static/
└── .github/
    └── workflows/
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

The automated news pipeline runs daily through GitHub Actions and generates 4 articles per run.

The finance pipeline generates 6 articles per run and uses the shared OpenRouter configuration.

## Authentication & Reader Profiles

The authentication system uses Supabase Auth with Google sign-in and Flask sessions.

Authentication and profile routes are organized inside the `auth` module, keeping the main `app.py` focused on the rest of the application.

The system supports:

- Google sign-in and authenticated sessions.
- Reader profile access and persistent name updates.
- Account logout.
- A Subscriber Center for signed-out users.
- Dynamic navigation based on authentication status.

The Reader Profile includes a Saved Articles area, which is intended for future saved-article functionality.

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

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token

OPENROUTER_API_KEY=your_openrouter_api_key
PIPELINE_PASSWORD=your_pipeline_password
```

Configure the additional settings required for Supabase Auth, Flask sessions and the market data API according to `config.py`.

**Never commit your `.env` file or private API credentials to version control.**

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
3. Classifies and tags the articles.
4. Stores article data in Supabase.
5. Generates article images using Cloudflare Workers AI and FLUX.1 Schnell.
6. Uploads images to Supabase Storage.

The automated pipeline runs daily and generates four news articles per run.

## Changelog

The project has evolved through multiple versions, introducing AI image generation, automated news processing, search and filtering functionality, a redesigned newsroom interface, authenticated reader profiles, and newsletter subscription management.

The current version is **3.2**.

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## License

Project Newz is licensed under the [MIT License](LICENSE).