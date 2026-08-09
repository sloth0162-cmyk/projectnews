# Project Newz

Project Newz is an **AI-powered news generation platform** built with Flask.

The platform collects news articles, processes them through AI agents, generates summaries and classifications, creates AI-generated images, and stores the resulting content in Supabase. Users can then browse the generated news through the website.

## Features

* 📰 Automated news scraping
* 🤖 AI-powered article summarization
* 🏷️ AI-powered article classification
* 🖼️ AI-generated article images
* 📄 Individual article pages
* 🗄️ Supabase database integration
* ☁️ Supabase Storage for generated images
* 🔐 Password-protected pipeline execution
* 🌐 Flask web application
* 🔌 Backend API routes

## Tech Stack

* **Python**
* **Flask**
* **Supabase**
* **Cloudflare AI**
* **HTML / CSS / JavaScript**

### AI Image Generation

Project Newz currently uses Cloudflare AI for image generation.

Model:

```text
@cf/lykon/dreamshaper-8-lcm
```

## Project Structure

```text
Project-Newz/
│
├── app.py
├── requirements.txt
├── .env
├── README.md
├── CHANGELOG.md
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
│   └── ...
│
└── static/
    ├── css/
    └── js/
```

> The structure may change as Project Newz continues to develop.

## Architecture

Project Newz separates the main responsibilities of the application into different modules.

### `services/`

Contains shared services and integrations used throughout the application.

#### `supabase_client.py`

Handles the Supabase client and database/storage communication.

#### `llm_utils.py`

Contains utilities used for working with language models.

#### `finance_llm.py`

Contains finance-specific LLM functionality for processing financial/news-related information.

---

### `agent/`

Contains the AI/data-processing agents used by the news pipeline.

#### `scraper_agent.py`

Responsible for collecting news articles from configured sources.

#### `summarizer_agent.py`

Processes scraped articles and generates summaries.

#### `classifier_agent.py`

Classifies articles and processes their relevant categories or metadata.

---

### `image_generation/`

Contains the article image-generation pipeline.

#### `lib.py`

Contains the core image-generation functionality and communication with the image-generation API.

#### `image_generate.py`

Builds prompts from article information and generates images for news articles.

#### `upload_image_to_supabase.py`

Handles uploading generated images to Supabase Storage.

---

### `route/`

Contains Flask application routes.

#### `route.py`

Defines the application's HTTP routes and connects the web interface/API endpoints to the underlying services.

## Pipeline

The main Project Newz pipeline follows this flow:

```text
                News Sources
                     │
                     ▼
              Scraper Agent
                     │
                     ▼
             Article Processing
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   Summarizer Agent      Classifier Agent
          │                     │
          └──────────┬──────────┘
                     ▼
              Supabase Database
                     │
                     ▼
             Image Generation
                     │
                     ▼
             Supabase Storage
                     │
                     ▼
                Flask App
                     │
                     ▼
                Website
```

## How It Works

When the pipeline is executed:

1. The scraper agent collects news articles.
2. The articles are processed by the summarizer agent.
3. The classifier agent processes article classification and metadata.
4. The resulting article information is stored in Supabase.
5. Article titles and summaries are used to generate AI images.
6. Generated images are uploaded to Supabase Storage.
7. The website retrieves the stored articles and displays them.
8. Users can open individual article pages.

The pipeline currently generates **3 articles at a time**.

## Image Generation

Project Newz generates an image for each processed news article using Cloudflare AI.

The article's title and summary are used to create the image-generation prompt.

The resulting image is then uploaded to Supabase Storage.

```text
Article Title
      +
Article Summary
      ↓
Prompt Generation
      ↓
Cloudflare AI
      ↓
Generated Image
      ↓
Supabase Storage
      ↓
Article Page
```

## Supabase

Supabase is used for both database storage and image storage.

### Database

The database stores the generated article information used by the website.

### Storage

Generated article images are stored in Supabase Storage and served to the website through their stored URLs.

## Requirements

Before running Project Newz, install:

* Python 3.x
* pip
* Supabase project
* Cloudflare account with AI API access

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Project-Newz
```

Create a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token

PIPELINE_PASSWORD=your_pipeline_password
```

Replace the placeholder values with your actual credentials.

**Never commit your `.env` file to Git.**

Add it to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

## Running the Pipeline

The news-generation pipeline is password protected.

A valid pipeline password is required before the pipeline can be executed.

The pipeline performs the following operations:

```text
Scrape
  ↓
Summarize
  ↓
Classify
  ↓
Store in Supabase
  ↓
Generate Images
  ↓
Upload Images
```

The current pipeline processes **3 articles at a time**.

## Current Limitations

### Tag Filtering

Tag-based filtering was available in **v1**, but the tag schema was subsequently lost and has not yet been recreated.

Therefore, tag-based filtering is currently unavailable.

## Development

Project Newz is an actively developed project. The architecture, agents, database schema, and pipeline may change as development continues.

For a record of changes between versions, see:

[`CHANGELOG.md`](CHANGELOG.md)

## Security

Keep credentials and secrets in environment variables.

Do not commit:

```text
.env
```

or files containing:

* Supabase credentials
* Cloudflare API tokens
* Pipeline passwords
* Other private API keys

## Project Status

Current functionality includes:

* News scraping
* AI article summarization
* AI article classification
* AI image generation
* Supabase database integration
* Supabase image storage
* Individual article pages
* Password-protected pipeline execution
* Flask API/routes

Project Newz is currently under active development.

## License
MIT License

Copyright (c) 2026 ProjectNewzz