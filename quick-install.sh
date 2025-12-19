#!/bin/bash

# Warhammer Veteran - Quick Install Script
# Copies module files to an existing BMAD project

set -e

echo "=========================================="
echo "Warhammer Veteran - Quick Install"
echo "=========================================="
echo ""

# Configuration
MODULE_ROOT="/workspaces/warhammer-veteran"
BMAD_PROJECT="${1}"

# Check if BMAD project path provided
if [ -z "$BMAD_PROJECT" ]; then
    echo "Usage: ./quick-install.sh <path-to-bmad-project>"
    echo ""
    echo "Example:"
    echo "  ./quick-install.sh /home/node/my-project"
    echo ""
    echo "This script copies the Warhammer Veteran module files to an"
    echo "existing BMAD project. Make sure you've already run:"
    echo "  npx bmad-method@alpha install"
    echo "in your target project directory."
    exit 1
fi

# Check if target exists and has BMAD
if [ ! -d "$BMAD_PROJECT/.bmad" ]; then
    echo "❌ Error: $BMAD_PROJECT doesn't appear to be a BMAD project"
    echo ""
    echo "Please run 'npx bmad-method@alpha install' in that directory first."
    exit 1
fi

echo "Module Source: $MODULE_ROOT"
echo "Target Project: $BMAD_PROJECT"
echo ""

# Install module files
echo "Installing Warhammer Veteran module..."
echo ""

cd "$BMAD_PROJECT"

# Copy agents
echo "📝 Copying agents..."
cp -f "$MODULE_ROOT"/agents/*.yaml .bmad/agents/
agent_count=$(ls -1 "$MODULE_ROOT"/agents/*.yaml | wc -l)
echo "   ✅ $agent_count agents copied"

# Copy agent sidecar folders
echo "📁 Copying sidecar folders..."
for sidecar in "$MODULE_ROOT"/agents/*-sidecar; do
    if [ -d "$sidecar" ]; then
        sidecar_name=$(basename "$sidecar")
        cp -rf "$sidecar" .bmad/agents/
        echo "      - $sidecar_name"
    fi
done
echo "   ✅ Sidecar folders copied"

# Copy tasks
echo "⚙️  Copying tasks..."
mkdir -p .bmad/tasks
cp -f "$MODULE_ROOT"/tasks/*.md .bmad/tasks/
task_count=$(ls -1 "$MODULE_ROOT"/tasks/*.md | wc -l)
echo "   ✅ $task_count tasks copied"

# Copy workflows
echo "🔄 Copying workflows..."
mkdir -p .bmad/workflows
for workflow_dir in "$MODULE_ROOT"/workflows/*; do
    if [ -d "$workflow_dir" ]; then
        workflow_name=$(basename "$workflow_dir")
        mkdir -p ".bmad/workflows/$workflow_name"
        cp -rf "$workflow_dir"/* ".bmad/workflows/$workflow_name/"
        echo "      - $workflow_name"
    fi
done
workflow_count=$(ls -1d "$MODULE_ROOT"/workflows/*/ | wc -l)
echo "   ✅ $workflow_count workflows copied"

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Warhammer Veteran module installed to:"
echo "  $BMAD_PROJECT"
echo ""
echo "Available Agents:"
echo "  ⚔️  Tacticus     - Army List Builder"
echo "  ⚖️  Arbitrator   - Rules Judge"
echo "  📜 Lorekeeper   - Lore Master"
echo "  🎨 Brushmaster  - Painting Guide"
echo "  📖 Chronicler   - Campaign Manager"
echo "  🔨 Artisan      - Hobby Advisor"
echo ""
echo "Try it out:"
echo "  cd $BMAD_PROJECT"
echo "  # Load Tacticus and use [BL] to build an army list"
echo "  # Load Brushmaster and use [DPS] to design a paint scheme"
echo "  # Use Party Mode to chat with all agents at once"
echo ""
echo "For the Emperor! 🎮"
echo ""
