#!/bin/bash
# Build script for standalone release
# Copies plugin contents from source locations

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

echo "Building standalone release..."
echo "Source: $SOURCE_ROOT"
echo "Target: $SCRIPT_DIR"

# Clean existing
rm -rf "$SCRIPT_DIR/research-toolkit"
rm -rf "$SCRIPT_DIR/financial-data-mcp"

# Copy research-toolkit
echo "Copying research-toolkit..."
cp -r "$SOURCE_ROOT/projects/plugins/research-toolkit" "$SCRIPT_DIR/research-toolkit"

# Copy financial-data-mcp
echo "Copying financial-data-mcp..."
mkdir -p "$SCRIPT_DIR/financial-data-mcp"
rsync -av --exclude='.mcp.json' --exclude='__pycache__' --exclude='.claude' \
    "$SOURCE_ROOT/projects/mcp-servers/financial-mcp-server/" "$SCRIPT_DIR/financial-data-mcp/"

# Create a sample .mcp.json for reference
cat > "$SCRIPT_DIR/financial-data-mcp/.mcp.json.example" << 'EOF'
{
  "mcpServers": {
    "financial-server": {
      "type": "stdio",
      "command": "./server.py",
      "args": [],
      "env": {}
    }
  }
}
EOF

echo "Build complete!"
echo ""
echo "Contents:"
find "$SCRIPT_DIR" -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) | head -20
echo "..."
