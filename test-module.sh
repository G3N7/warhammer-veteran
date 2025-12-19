#!/bin/bash

# Warhammer Veteran Module - Local Testing Script
# This script helps test the module locally without full installation

echo "=========================================="
echo "Warhammer Veteran Module - Local Test"
echo "=========================================="
echo ""

# Set module root
MODULE_ROOT="/workspaces/warhammer-veteran"
cd "$MODULE_ROOT"

echo "Module Location: $MODULE_ROOT"
echo ""

# Test 1: Validate module.yaml
echo "1. Testing module.yaml..."
if [ -f "module.yaml" ]; then
    echo "   ✅ module.yaml exists"
    # Check for required fields
    if grep -q "code:" module.yaml && grep -q "name:" module.yaml; then
        echo "   ✅ module.yaml has required fields"
    else
        echo "   ❌ module.yaml missing required fields"
    fi
else
    echo "   ❌ module.yaml not found"
fi
echo ""

# Test 2: Validate agent files
echo "2. Testing agent YAML files..."
agent_count=0
for agent in agents/*.yaml; do
    if [ -f "$agent" ]; then
        agent_name=$(basename "$agent" .yaml)
        if grep -q "^agent:" "$agent"; then
            echo "   ✅ $agent_name.yaml"
            ((agent_count++))
        else
            echo "   ❌ $agent_name.yaml (invalid structure)"
        fi
    fi
done
echo "   Total: $agent_count/6 agents validated"
echo ""

# Test 3: Validate tasks
echo "3. Testing task files..."
task_count=0
for task in tasks/*.md; do
    if [ -f "$task" ]; then
        task_name=$(basename "$task" .md)
        echo "   ✅ $task_name"
        ((task_count++))
    fi
done
echo "   Total: $task_count/3 tasks found"
echo ""

# Test 4: Validate workflows
echo "4. Testing workflow files..."
workflow_count=0
for workflow in workflows/*/workflow.md; do
    if [ -f "$workflow" ]; then
        workflow_name=$(basename $(dirname "$workflow"))
        echo "   ✅ $workflow_name"
        ((workflow_count++))
    fi
done
echo "   Total: $workflow_count/2 workflows found"
echo ""

# Test 5: Check sidecar folders
echo "5. Testing sidecar folder structure..."
sidecar_count=0
for sidecar in agents/*-sidecar; do
    if [ -d "$sidecar" ]; then
        sidecar_name=$(basename "$sidecar")
        echo "   ✅ $sidecar_name"
        ((sidecar_count++))
    fi
done
echo "   Total: $sidecar_count/6 sidecar folders found"
echo ""

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Agents:    $agent_count/6"
echo "Tasks:     $task_count/3"
echo "Workflows: $workflow_count/2"
echo "Sidecars:  $sidecar_count/6"
echo ""

if [ $agent_count -eq 6 ] && [ $task_count -eq 3 ] && [ $workflow_count -eq 2 ] && [ $sidecar_count -eq 6 ]; then
    echo "✅ All tests passed! Module is ready."
    echo ""
    echo "To use the module locally:"
    echo "1. Copy agent YAML files to your BMAD project's agents/ folder"
    echo "2. Copy task files to your BMAD project's tasks/ folder"
    echo "3. Copy workflow folders to your BMAD project's workflows/ folder"
    echo ""
    echo "Or publish to NPM and install via:"
    echo "  npx bmad-method@alpha install @bmad-modules/warhammer-veteran"
else
    echo "❌ Some tests failed. Check the module structure."
fi

echo ""
echo "=========================================="
