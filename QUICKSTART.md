# 🚀 Quick Start Guide

Get the AI-IDE Observatory running in 5 minutes!

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git
- (Optional) Anthropic API key for LLM insights

## Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install web dependencies
cd web && npm install && cd ..
```

## Step 2: Set API Key (Optional but Recommended)

```bash
# Linux/Mac
export ANTHROPIC_API_KEY="your-key-here"

# Windows
set ANTHROPIC_API_KEY=your-key-here
```

**Without API key**: The system will run in fallback mode with basic insights.

## Step 3: Run Analysis

```bash
# Option A: Using Python CLI
python run.py analyze

# Option B: Using steering commands
source steering/commands.sh
steer_analyze
```

This will:
- Clone 3 AI-IDE repositories (Cline, Continue, GPT Engineer)
- Analyze their architecture
- Generate insights (with LLM if API key is set)
- Create web-ready data files

**Estimated time**: 5-15 minutes depending on your connection and API key availability.

## Step 4: View Results

```bash
# Start the web UI
python run.py serve

# Or manually
cd web && npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser!

## Next Steps

### Analyze a Specific Repository

```bash
python run.py analyze --repo cline
```

### Check Status

```bash
source steering/commands.sh
steer_status
```

### Explore the Code

- `registry/repos.yaml` - Repository definitions
- `steering/config.yaml` - System configuration
- `storage/insights/v1/` - Generated insights
- `docs/` - Comprehensive documentation

### Add More Repositories

Edit `registry/repos.yaml`:

```yaml
repositories:
  - id: my-repo
    name: "My AI-IDE"
    url: "https://github.com/user/repo"
    type: "vscode-extension"
    language: "typescript"
    focus_areas:
      - llm_integration
    analysis_priority: high
    tags: ["ai", "ide"]
```

Then run `steer_analyze` again!

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
- This is a warning, not an error
- System will run in fallback mode with basic insights
- Set the key for better AI-powered analysis

### "Repository clone failed"
- Check internet connection
- Verify GitHub is accessible
- Repository URL might be incorrect

### "Module not found"
- Run `pip install -r requirements.txt` again
- Make sure you're in the project root directory

### Web UI won't start
- Run `cd web && npm install`
- Check if port 3000 is available
- Try `npm run build` then `npm start`

## Getting Help

- Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- Read [GROWTH_PATH.md](docs/GROWTH_PATH.md) for extending features
- Check steering commands: `source steering/commands.sh && steer_help`

## What's Next?

Once you have the basic system running, explore:

1. **Patterns** - View cross-repository patterns at `/patterns`
2. **Repository Details** - Click any repo card for deep dive
3. **Growth Features** - Enable monitoring, auto-discovery in `steering/config.yaml`

Happy analyzing! 🔬
