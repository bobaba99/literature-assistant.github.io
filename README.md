# Literature Assistant

AI-powered research paper analysis tool that extracts structured information from academic PDFs and generates beautifully formatted reports.

## Features

- **PDF Upload**: Drag-and-drop or click to upload research papers
- **AI Analysis**: Uses OpenAI GPT-4 to extract structured information following academic standards
- **Beautiful Formatting**: Generates clean, readable reports with proper structure and visual hierarchy
- **Multiple Export Formats**:
  - Web display with syntax highlighting
  - Markdown (.md) files for note-taking apps like Obsidian
  - Word documents (.docx) for publication-ready reports
- **Comprehensive Extraction**:
  - APA 7th citation
  - Research questions and hypotheses
  - Theoretical framework
  - Methodology and design details
  - Empirical findings
  - Authors' conclusions and limitations
  - Critical appraisal
  - Metadata and tags (type, year, rating, topics, methods, etc.)

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone <your-repository-url>
cd literature-assistant
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running the Application

#### Option A: Using Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

- Backend API: `http://localhost:5001`
- Frontend: Serve `frontend/` directory separately or deploy to GitHub Pages

#### Option B: Local Python

1. **Start the backend server**
```bash
python main.py server
```

The server will run on `http://localhost:5001` (port 5001 is used because macOS reserves 5000 for AirPlay)

2. **In a new terminal, start the frontend**
```bash
cd frontend
python -m http.server 8000
```

3. **Open in browser**
```
http://localhost:8000
```

## Usage

1. Open the web application in your browser
2. Upload a PDF research paper (drag-and-drop or click to browse)
3. Click "Analyze Paper"
4. Wait for AI processing (usually 30-60 seconds)
5. View the beautifully formatted results
6. Download as Markdown or Word document

## Project Structure

```
literature-assistant/
├── frontend/               # Web interface
│   ├── index.html         # Main page
│   ├── styles.css         # Styling
│   └── app.js             # Frontend logic
├── backend/               # Flask API
│   └── api/
│       └── app.py         # Main backend application
├── uploads/               # Temporary PDF storage (gitignored)
├── outputs/               # Generated outputs (gitignored)
├── prompt.md              # AI analysis prompt template
├── requirements.txt       # Python dependencies
├── main.py                # CLI helper script
├── .env.example           # Environment template
└── README.md              # This file
```

## Output Format

The analysis is structured into the following sections:

1. **Full Citation** (APA 7th format)
2. **Research Question & Hypotheses**
3. **Theoretical Framework**
4. **Methodology & Design**
   - Research design
   - Sample size and population
   - Variables (IV, DV, covariates)
5. **Empirical Findings**
6. **Authors' Conclusions**
7. **Limitations**
8. **Critical Appraisal**
   - Methodological critique
   - Generalizability
   - Construct validity
   - Key contributions
   - Connections to other research
9. **Metadata & Tags**
   - Paper type
   - Year
   - Rating (1-5 stars)
   - Journal
   - Authors (in Obsidian link format)
   - Topics, methods, theory, population tags

## Customization

### Modify the Analysis Prompt

Edit `prompt.md` to customize what information is extracted and how it's structured. The AI will follow the instructions in this file.

### Change Port Numbers

- **Backend**: Edit port in `backend/api/app.py` (line 331) and `main.py` (line 64)
- **Frontend**: Use any port when running the HTTP server

## Deployment

### Quick Deploy to Render (Recommended)

This project is Docker-ready and configured for one-click deployment to Render.

1. **Push to GitHub:**
```bash
git push origin main
```

2. **Deploy to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will detect `render.yaml` and auto-configure
   - Add `OPENAI_API_KEY` environment variable in dashboard

3. **Update Frontend:**
   - Edit `frontend/app.js` with your Render backend URL
   - Example: `https://literature-assistant-backend.onrender.com`

**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.**

### Frontend (GitHub Pages)

The repository includes a GitHub Actions workflow that automatically deploys the frontend to GitHub Pages:

1. Enable GitHub Pages in repository settings
2. Set source to "GitHub Actions"
3. Push to main branch

### Backend Deployment Options

- **Render** (Recommended): Docker-based, free tier available
- **Railway**: Automatic deployments from GitHub
- **Heroku**: Classic PaaS with Docker support
- **DigitalOcean App Platform**: Managed container hosting
- **AWS/GCP**: Full control with Docker containers

**All methods use the included Dockerfile for consistent deployment.**

## Troubleshooting

### "OPENAI_API_KEY not found"
- Ensure `.env` file exists in project root
- Check that the API key is valid
- Restart the backend server after adding the key

### "Cannot connect to backend"
- Verify backend is running on port 5001
- Check that `API_URL` in `frontend/app.js` matches your backend URL
- Ensure no firewall is blocking the connection

### "Failed to extract text from PDF"
- Ensure PDF is not password-protected
- Try a different PDF file
- Check that PyPDF2 is installed correctly

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Marked.js
- **Backend**: Python, Flask, Flask-CORS
- **AI**: OpenAI GPT-4 API
- **PDF Processing**: PyPDF2
- **Document Generation**: python-docx

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please create an issue in the GitHub repository.
