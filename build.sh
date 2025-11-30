#!/bin/bash
# Build script for distribution

echo "🏗️  Building ats-resume-builder distribution..."

# Clean previous builds
make clean

# Install build tools
pip install --upgrade build twine

# Build distributions
python -m build

echo "✅ Build complete!"
echo ""
echo "Distribution files created:"
ls -lh dist/
echo ""
echo "Next steps:"
echo "  - Test: pip install dist/*.whl"
echo "  - Upload to PyPI: twine upload dist/*"
echo "  - Create GitHub release: git tag v0.2.0 && git push origin v0.2.0"