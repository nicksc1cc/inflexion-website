#!/bin/bash
# Run the full Inflexion Site Intelligence pipeline
# Then serve the dashboard

echo "============================================"
echo "  INFLEXION SITE INTELLIGENCE"
echo "  Manual run pipeline"
echo "============================================"
echo ""

cd "$(dirname "$0")"
INTELLIGENCE_DIR=$(pwd)
export PYTHONPATH="$INTELLIGENCE_DIR:$PYTHONPATH"

# Check for TypeSafe API key
if [ -z "$TYPESAFE_API_KEY" ]; then
    if [ -f ".env" ]; then
        source .env
    fi
fi

if [ -n "$TYPESAFE_API_KEY" ]; then
    echo "[✓] TypeSafe API key configured"
else
    echo "[!] TypeSafe API key not set — using fallback analysis"
    echo "    Set TYPESAFE_API_KEY in .env for Jev atomic evaluations"
fi

echo ""

# Run the pipeline
python3 pipelines/full_run.py "$@"

echo ""
echo "Dashboard: file://$INTELLIGENCE_DIR/ui/dashboard.html"
echo ""
echo "To serve via HTTP:"
echo "  python3 -m http.server 8080 --directory $INTELLIGENCE_DIR/ui"
echo ""