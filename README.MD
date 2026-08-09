# Project Newz

**Project Newz** is an AI-powered news generation platform built with **Flask**.

It automatically collects news, generates summaries and classifications using LLMs, creates AI-generated images, and stores the resulting articles in Supabase.

## Features

* 📰 Automated news scraping
* 🤖 AI-generated article summaries
* 🏷️ Article classification
* 🖼️ AI-generated article images
* 📄 Individual article pages
* 🗄️ Supabase database and storage
* 🔐 Password-protected pipeline
* 🌐 Flask web application

## Tech Stack

* **Backend:** Python, Flask
* **Database & Storage:** Supabase
* **Text AI:** OpenRouter — Llama 3.1 8B
* **Image AI:** Cloudflare AI — `@cf/lykon/dreamshaper-8-lcm`
* **Frontend:** HTML, CSS, JavaScript

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

## Pipeline

```text
News
 ↓
Scraper Agent
 ↓
Summarizer Agent
 ↓
Classifier Agent
 ↓
Supabase
 ↓
Image Generation
 ↓
Supabase Storage
 ↓
Website
```

The pipeline currently generates **3 articles at a time**.

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

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

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

## Pipeline

Running the pipeline requires the configured pipeline password.

The pipeline:

1. Scrapes news articles.
2. Generates summaries using OpenRouter and Llama 3.1 8B.
3. Classifies the articles.
4. Stores article data in Supabase.
5. Generates article images using Cloudflare AI.
6. Uploads images to Supabase Storage.

## Current Limitation

Tag-based filtering was available in **v1**, but the tag schema was lost and has not yet been recreated. Therefore, tag filtering is currently unavailable.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for project changes.

## License

Project Newz is licensed under the [MIT License](LICENSE).
