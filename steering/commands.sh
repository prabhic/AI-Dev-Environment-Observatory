#!/bin/bash
# =======================================================
# AI-IDE OBSERVATORY - STEERING COMMANDS
# =======================================================
# Your command center for controlling the observatory.

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- MVP COMMANDS (Work Today) ---

steer_analyze() {
    echo -e "${CYAN}🔬 Running full analysis...${NC}"
    python run.py analyze
}

steer_analyze_one() {
    if [ -z "$1" ]; then
        echo -e "${YELLOW}Usage: steer_analyze_one <repo_id>${NC}"
        echo "Available: cline, continue, gpt-engineer"
        exit 1
    fi
    echo -e "${CYAN}🔬 Analyzing $1...${NC}"
    python run.py analyze --repo "$1"
}

steer_serve() {
    echo -e "${CYAN}🌐 Starting web UI...${NC}"
    python run.py serve
}

steer_export() {
    echo -e "${CYAN}📦 Exporting data for web...${NC}"
    python run.py export
}

steer_install() {
    echo -e "${CYAN}📦 Installing Python dependencies...${NC}"
    pip install -r requirements.txt

    echo -e "${CYAN}📦 Installing web dependencies...${NC}"
    cd web && npm install && cd ..

    echo -e "${GREEN}✓ Installation complete${NC}"
}

steer_status() {
    echo -e "${CYAN}📊 Observatory Status${NC}"
    echo ""

    if [ -f "storage/insights/v1/metadata.json" ]; then
        echo -e "${GREEN}✓ Analysis data exists${NC}"
        python -c "
import json
with open('storage/insights/v1/metadata.json') as f:
    data = json.load(f)
    print(f\"  Last run: {data.get('run_id', 'N/A')}\")
    print(f\"  Repos analyzed: {data.get('successful', 0)}\")
"
    else
        echo -e "${YELLOW}⚠ No analysis data yet. Run 'steer_analyze' first.${NC}"
    fi

    echo ""
    echo "Growth features status:"
    echo "  Auto-discovery: Disabled (MVP)"
    echo "  Monitoring: Disabled (MVP)"
    echo "  Evolution tracking: Disabled (MVP)"
}

# --- FUTURE COMMANDS (Stubbed) ---

steer_monitor() {
    echo -e "${YELLOW}[Future] Starting 24/7 monitoring...${NC}"
    echo "Not yet enabled. Edit steering/config.yaml:"
    echo "  monitoring.enabled = true"
    # python run.py monitor --daemon
}

steer_discover() {
    echo -e "${YELLOW}[Future] Scanning for new repos...${NC}"
    echo "Not yet enabled. Edit steering/config.yaml:"
    echo "  experimental.auto_discovery = true"
    # python run.py discover --auto-add
}

steer_research() {
    echo -e "${YELLOW}[Future] Generating research insights...${NC}"
    echo "Feature not yet implemented"
    # python run.py research --output=paper.md
}

steer_enable() {
    if [ -z "$1" ]; then
        echo -e "${YELLOW}Usage: steer_enable <feature>${NC}"
        echo "Features: monitoring, discovery, evolution"
        exit 1
    fi

    echo -e "${YELLOW}[Future] Enabling: $1${NC}"
    echo "Manually edit steering/config.yaml for now"
    # Future: Programmatic config updates
}

# --- HELP ---

steer_help() {
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN} AI-IDE OBSERVATORY - Steering Commands${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo ""
    echo "Working Commands (MVP):"
    echo "  steer_analyze          - Run full analysis of all repos"
    echo "  steer_analyze_one <id> - Analyze specific repo (cline, continue, gpt-engineer)"
    echo "  steer_serve            - Start web UI (localhost:3000)"
    echo "  steer_export           - Export data for web UI"
    echo "  steer_install          - Install all dependencies"
    echo "  steer_status           - Show observatory status"
    echo ""
    echo "Future Commands (Stubbed):"
    echo "  steer_monitor          - Start continuous monitoring"
    echo "  steer_discover         - Auto-discover new AI-IDE repos"
    echo "  steer_research         - Generate research report"
    echo "  steer_enable <feature> - Enable growth feature"
    echo ""
    echo "Documentation:"
    echo "  README.md         - Quick start guide"
    echo "  docs/ARCHITECTURE.md - System architecture"
    echo "  docs/GROWTH_PATH.md  - How to evolve features"
    echo ""
}

# Show help if no command provided
if [ $# -eq 0 ]; then
    steer_help
    exit 0
fi

# Main entry point
case "$1" in
    analyze)
        steer_analyze
        ;;
    analyze-one)
        steer_analyze_one "$2"
        ;;
    serve)
        steer_serve
        ;;
    export)
        steer_export
        ;;
    install)
        steer_install
        ;;
    status)
        steer_status
        ;;
    monitor)
        steer_monitor
        ;;
    discover)
        steer_discover
        ;;
    research)
        steer_research
        ;;
    enable)
        steer_enable "$2"
        ;;
    help|--help|-h)
        steer_help
        ;;
    *)
        echo -e "${YELLOW}Unknown command: $1${NC}"
        steer_help
        exit 1
        ;;
esac
