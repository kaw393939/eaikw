#!/bin/bash
# Build and Deploy Script for EAIKW

echo "🏗️  Building EAIKW Site..."
echo "=" * 50

# Clean old build
echo "🧹 Cleaning old build..."
rm -rf docs/*

# Run Python build
echo "🔨 Building site..."
python build.py

# Check if build succeeded
if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

# Run validation (optional)
echo "🔍 Running validation..."
python build.py --validate

# Copy CNAME for GitHub Pages
echo "📝 Setting up domain..."
echo "eaikw.com" > docs/CNAME

# Create .nojekyll to prevent Jekyll processing
touch docs/.nojekyll

echo ""
echo "=" * 50
echo "✅ Build complete!"
echo "📂 Output: docs/"
echo ""
echo "To deploy:"
echo "  git add docs/"
echo "  git commit -m 'Build site'"
echo "  git push origin main"
echo "=" * 50
