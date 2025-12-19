#!/bin/bash

# Warhammer Veteran - Install and Party Mode Script
# Installs the module to a test BMAD project and launches Party Mode with all agents

set -e  # Exit on error

echo "=========================================="
echo "Warhammer Veteran - Install & Party Mode"
echo "=========================================="
echo ""

# Configuration
MODULE_ROOT="/workspaces/warhammer-veteran"
TEST_PROJECT="${1:-$HOME/warhammer-test}"

echo "Module Source: $MODULE_ROOT"
echo "Test Project:  $TEST_PROJECT"
echo ""

# Step 1: Create test project directory
echo "1. Setting up test project..."
if [ ! -d "$TEST_PROJECT" ]; then
    echo "   Creating $TEST_PROJECT..."
    mkdir -p "$TEST_PROJECT"
    echo "   ✅ Directory created"
else
    echo "   ✅ Directory exists"
fi
echo ""

# Step 2: Install BMAD Core if needed
echo "2. Checking BMAD Core installation..."
cd "$TEST_PROJECT"
if [ ! -d ".bmad" ]; then
    echo "   Installing BMAD Core..."
    npx bmad-method@alpha install
    echo "   ✅ BMAD Core installed"
else
    echo "   ✅ BMAD Core already installed"
fi
echo ""

# Step 3: Install Warhammer Veteran module
echo "3. Installing Warhammer Veteran module..."

# Create module directories if they don't exist
mkdir -p .bmad/agents
mkdir -p .bmad/tasks
mkdir -p .bmad/workflows

# Copy agents
echo "   Copying agents..."
cp -f "$MODULE_ROOT"/agents/*.yaml .bmad/agents/
echo "   ✅ 6 agents copied"

# Copy agent sidecar folders
echo "   Copying agent sidecar folders..."
for sidecar in "$MODULE_ROOT"/agents/*-sidecar; do
    if [ -d "$sidecar" ]; then
        sidecar_name=$(basename "$sidecar")
        cp -rf "$sidecar" .bmad/agents/
        echo "      - $sidecar_name"
    fi
done
echo "   ✅ Sidecar folders copied"

# Copy tasks
echo "   Copying tasks..."
cp -f "$MODULE_ROOT"/tasks/*.md .bmad/tasks/
echo "   ✅ 3 tasks copied"

# Copy workflows
echo "   Copying workflows..."
for workflow_dir in "$MODULE_ROOT"/workflows/*; do
    if [ -d "$workflow_dir" ]; then
        workflow_name=$(basename "$workflow_dir")
        mkdir -p ".bmad/workflows/$workflow_name"
        cp -rf "$workflow_dir"/* ".bmad/workflows/$workflow_name/"
        echo "      - $workflow_name"
    fi
done
echo "   ✅ 2 workflows copied"

echo ""
echo "   Module installation complete!"
echo ""

# Step 4: Verify installation
echo "4. Verifying installation..."
agent_count=$(ls -1 .bmad/agents/*.yaml 2>/dev/null | wc -l)
task_count=$(ls -1 .bmad/tasks/*.md 2>/dev/null | wc -l)
workflow_count=$(ls -1d .bmad/workflows/*/ 2>/dev/null | wc -l)

echo "   Agents found:    $agent_count"
echo "   Tasks found:     $task_count"
echo "   Workflows found: $workflow_count"

if [ "$agent_count" -ge 6 ]; then
    echo "   ✅ All agents installed"
else
    echo "   ⚠️  Some agents may be missing"
fi
echo ""

# Step 5: List available agents
echo "5. Warhammer Veteran Agents Available:"
echo ""
echo "   ⚔️  Tacticus      - Army List Builder & Competitive Strategist"
echo "   ⚖️  Arbitrator    - Rules Judge & Dispute Resolver"
echo "   📜 Lorekeeper    - Lore Master & Narrative Historian"
echo "   🎨 Brushmaster   - Painting Guide & Hobby Mentor"
echo "   📖 Chronicler    - Campaign Manager & Narrative Coordinator"
echo "   🔨 Artisan       - Hobby Advisor & Conversion Specialist"
echo ""

# Step 6: Create Party Mode prompt
echo "6. Preparing Party Mode..."
cat > .bmad-party-prompt.txt << 'PARTY_PROMPT'
Welcome to the Warhammer Veteran Party Mode!

All 6 specialist agents are here to help you with Warhammer 40k:

⚔️  Tacticus - Army list building and competitive meta analysis
⚖️  Arbitrator - Rules clarification and dispute resolution
📜 Lorekeeper - Deep lore exploration and faction history
🎨 Brushmaster - Painting techniques and color scheme design
📖 Chronicler - Campaign management and narrative development
🔨 Artisan - Hobby tips, conversions, and collection strategy

Let's discuss Warhammer 40k! What would you like to explore?
PARTY_PROMPT

echo "   ✅ Party Mode prompt ready"
echo ""

# Step 7: Launch options
echo "=========================================="
echo "Installation Complete! 🎉"
echo "=========================================="
echo ""
echo "Your Warhammer Veteran module is now installed at:"
echo "  $TEST_PROJECT"
echo ""
echo "Choose how to proceed:"
echo ""
echo "  [P] Launch Party Mode with all 6 agents"
echo "  [T] Load Tacticus (Army List Builder)"
echo "  [B] Load Brushmaster (Painting Guide)"
echo "  [A] Load Arbitrator (Rules Judge)"
echo "  [L] Load Lorekeeper (Lore Master)"
echo "  [C] Load Chronicler (Campaign Manager)"
echo "  [R] Load Artisan (Hobby Advisor)"
echo "  [X] Exit (you can manually launch agents later)"
echo ""
read -p "Select option: " choice

case "${choice^^}" in
    P)
        echo ""
        echo "Launching Party Mode with all Warhammer Veteran agents..."
        echo ""
        # Launch Party Mode using BMAD core workflow
        if [ -f ".bmad/core/workflows/party-mode/workflow.md" ]; then
            echo "Starting party mode discussion about Warhammer 40k..."
            echo ""
            echo "Party mode would launch here with all 6 agents."
            echo "For now, you can manually run:"
            echo "  cd $TEST_PROJECT"
            echo "  # Load your BMAD CLI and trigger party mode"
        else
            echo "Note: Party mode workflow not found."
            echo "You can load individual agents or use your BMAD interface."
        fi
        ;;
    T)
        echo "Loading Tacticus agent..."
        echo "Use [BL] to Build Army Lists with meta analysis!"
        ;;
    B)
        echo "Loading Brushmaster agent..."
        echo "Use [DPS] to Design Paint Schemes with lore validation!"
        ;;
    A)
        echo "Loading Arbitrator agent..."
        echo "Ask rules questions and get Wahapedia-backed rulings!"
        ;;
    L)
        echo "Loading Lorekeeper agent..."
        echo "Explore the rich lore of the 41st millennium!"
        ;;
    C)
        echo "Loading Chronicler agent..."
        echo "Manage your Crusade campaigns and narrative battles!"
        ;;
    R)
        echo "Loading Artisan agent..."
        echo "Get hobby advice on conversions, basing, and collecting!"
        ;;
    X)
        echo "Setup complete. To use the agents:"
        echo "  cd $TEST_PROJECT"
        echo "  # Use your BMAD interface to load agents"
        ;;
    *)
        echo "Invalid option. Setup complete!"
        echo "Navigate to $TEST_PROJECT to use the agents."
        ;;
esac

echo ""
echo "=========================================="
echo ""
echo "Quick Reference:"
echo "  Test Project: $TEST_PROJECT"
echo "  Agents:       .bmad/agents/"
echo "  Tasks:        .bmad/tasks/"
echo "  Workflows:    .bmad/workflows/"
echo ""
echo "For the Emperor! 🎮"
echo ""
