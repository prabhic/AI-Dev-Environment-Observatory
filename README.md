# 🔬 AI-IDE Observatory

**Self-Evolving Research Platform for AI-IDE Architecture Analysis**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/ai-ide-observatory)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 Overview

The AI-IDE Observatory is a **living research platform** that analyzes the architecture of AI-powered integrated development environments. By combining static code analysis with LLM-powered insights, it uncovers patterns, best practices, and evolutionary trends across the AI-IDE ecosystem.

**Current State (MVPv1):**
- Analyzes 3 repositories (Cline, Continue, GPT Engineer)
- Extracts architectural components and patterns
- Generates LLM-powered insights
- Beautiful web UI for exploring findings

**Vision:**
- Auto-discovery of new AI-IDEs
- Continuous monitoring and evolution tracking
- Community-driven research platform
- The "arXiv" of AI-IDE architecture

## ✨ Features

### Today (MVPv1)
- ✅ **Repository Registry** - Structured tracking of AI-IDE projects
- ✅ **Smart Analysis** - Intelligent file scanning and component extraction
- ✅ **LLM Synthesis** - Claude-powered architectural insights
- ✅ **Pattern Detection** - Cross-repository pattern identification
- ✅ **Web Dashboard** - Interactive exploration of insights
- ✅ **Growth-Ready** - Designed for easy evolution

### Tomorrow (Growth Path)
- 🔮 **Auto-Discovery** - GitHub scanning for new AI-IDEs
- 🔮 **Monitoring** - Continuous 24/7 analysis updates
- 🔮 **Evolution Tracking** - Time-series architecture changes
- 🔮 **Community** - Collaborative research platform
- 🔮 **Research Papers** - Auto-generated insights

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git
- Anthropic API key (for LLM insights)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-ide-observatory.git
cd ai-ide-observatory

# Install dependencies
pip install -r requirements.txt

# Install web dependencies
cd web && npm install && cd ..

# Set up API key (optional, but recommended)
export ANTHROPIC_API_KEY="your-key-here"
```

### Run Analysis

```bash
# Analyze all repositories
python run.py analyze

# Or use steering commands
source steering/commands.sh
steer_analyze
```

This will:
1. Clone the registered repositories
2. Scan and analyze code
3. Generate LLM-powered insights
4. Extract cross-repository patterns
5. Export data for the web UI

### View Results

```bash
# Start web UI
python run.py serve

# Or
cd web && npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to explore insights!

## 📂 Project Structure

```
ai-ide-observatory/
├── registry/           # Repository registry system
├── analyzers/          # Pluggable analysis engines
├── intelligence/       # LLM-powered insights
├── storage/            # Versioned data storage
├── pipeline/           # Orchestration layer
├── web/                # Next.js dashboard
├── steering/           # Your control center
├── docs/               # Documentation
├── run.py              # Main entry point
└── requirements.txt    # Python dependencies
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.

## 🎛️ Steering Commands

The observatory is controlled via simple commands:

```bash
# Source the steering commands
source steering/commands.sh

# Working commands (MVPv1)
steer_analyze              # Run full analysis
steer_analyze_one cline    # Analyze specific repo
steer_serve                # Start web UI
steer_status               # Show status

# Future commands (stubbed)
steer_monitor              # Start continuous monitoring
steer_discover             # Auto-discover new repos
steer_research             # Generate research report
```

## 🔧 Configuration

All behavior is controlled via `steering/config.yaml`:

```yaml
# Analysis configuration
analysis:
  mode: "full"
  llm_provider: "anthropic"
  llm_model: "claude-sonnet-4"
  max_files_per_repo: 100

# Growth switches (easy to enable)
experimental:
  auto_discovery: false      # Enable GitHub scanning
  monitoring: false          # Enable continuous monitoring
```

No code changes needed - just flip switches!

## 📊 Current Insights

The observatory currently analyzes:

1. **Cline** (formerly Claude Dev) - VSCode extension for agentic coding
2. **Continue** - Multi-IDE extension with multi-LLM support
3. **GPT Engineer** - CLI-based autonomous coding agent

### What We Analyze

- 🏗️ **Architecture** - Overall structure and design patterns
- 🤖 **LLM Integration** - How projects integrate with AI models
- 🔧 **Tool Calling** - Tool use and function calling patterns
- 💬 **Context Management** - Conversation and memory handling
- 📝 **Code Patterns** - Reusable architectural patterns
- 🔄 **Streaming** - Real-time response handling

## 🌱 Growth Path

This is a **seed architecture** - designed to grow with minimal effort.

### Adding More Repositories

```yaml
# Edit registry/repos.yaml
repositories:
  - id: new-repo
    name: "New AI-IDE"
    url: "https://github.com/user/repo"
    type: "vscode-extension"
    language: "typescript"
    # ...
```

Then run: `steer_analyze`

### Enabling Auto-Discovery

```yaml
# Edit steering/config.yaml
experimental:
  auto_discovery: true
```

The system will automatically scan GitHub for new AI-IDEs.

### Enabling Monitoring

```yaml
# Edit steering/config.yaml
monitoring:
  enabled: true
  check_interval_hours: 24
```

The system will continuously monitor and update insights.

See [GROWTH_PATH.md](docs/GROWTH_PATH.md) for complete evolution guide.

## 📈 Roadmap

### Phase 1: MVP ✅ (Current)
- [x] Repository registry
- [x] Static analysis
- [x] LLM insights
- [x] Web dashboard
- [x] Pattern detection

### Phase 2: Auto-Growth
- [ ] GitHub auto-discovery
- [ ] Continuous monitoring
- [ ] Incremental updates
- [ ] API endpoints

### Phase 3: Evolution Tracking
- [ ] Time-series database
- [ ] Evolution timeline
- [ ] Pattern emergence detection
- [ ] Trend analysis

### Phase 4: Community Platform
- [ ] User authentication
- [ ] Community contributions
- [ ] Voting on insights
- [ ] Research paper generator

## 🤝 Contributing

This platform is designed for growth! Contributions welcome:

1. **Add Repositories** - Suggest new AI-IDEs to analyze
2. **Improve Analysis** - Enhance pattern detection
3. **Build Features** - Implement growth hooks
4. **Share Insights** - Contribute research findings

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📝 Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture and design
- [GROWTH_PATH.md](docs/GROWTH_PATH.md) - How to evolve each component
- [API.md](docs/API.md) - API documentation (future)

## 🔬 Research Applications

Perfect for:
- **Researchers** - Study AI-IDE evolution and patterns
- **Developers** - Learn architectural best practices
- **Organizations** - Evaluate AI-IDE technologies
- **Educators** - Teaching AI-assisted development

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with:
- [Anthropic Claude](https://anthropic.com) - LLM insights
- [Next.js](https://nextjs.org) - Web framework
- [Python](https://python.org) - Analysis engine

Analyzing:
- [Cline](https://github.com/cline/cline)
- [Continue](https://github.com/continuedev/continue)
- [GPT Engineer](https://github.com/AntonOsika/gpt-engineer)

## 🌟 Star History

If you find this project useful, please ⭐ star it!

---

**Built with Claude Code** | **Self-Evolving Research Platform** | **v1.0.0**
