#!/bin/bash
# HTML Validation and Analysis Script
# Usage: ./validate.sh [file]

FILE="${1:-index.html}"
echo "🔍 Validating: $FILE"
echo "================================"

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo "❌ Error: File '$FILE' not found"
    exit 1
fi

# Run HTML validator
echo ""
echo "📝 HTML Validation:"
echo "-------------------"
html-validator --file="$FILE" --format=text 2>&1

# Check for common issues
echo ""
echo "⚠️  Common Issues Check:"
echo "------------------------"

# Check for spaces in URLs
echo -n "• Unencoded spaces in URLs: "
if grep -q 'href="[^"]*[[:space:]]' "$FILE"; then
    echo "⚠️  FOUND"
    grep -n 'href="[^"]*[[:space:]]' "$FILE" | head -5
else
    echo "✅ None"
fi

# Check for double hyphens in comments
echo -n "• Double hyphens in comments: "
if grep -q '<!--.*--.*-->' "$FILE"; then
    echo "⚠️  FOUND"
    grep -n '<!--.*--.*-->' "$FILE" | head -5
else
    echo "✅ None"
fi

# Check for unclosed tags
echo -n "• Basic tag balance check: "
OPEN_DIVS=$(grep -o '<div' "$FILE" | wc -l | tr -d ' ')
CLOSE_DIVS=$(grep -o '</div>' "$FILE" | wc -l | tr -d ' ')
if [ "$OPEN_DIVS" -eq "$CLOSE_DIVS" ]; then
    echo "✅ $OPEN_DIVS divs balanced"
else
    echo "⚠️  MISMATCH: $OPEN_DIVS open, $CLOSE_DIVS close"
fi

echo ""
echo "✨ Validation complete!"
