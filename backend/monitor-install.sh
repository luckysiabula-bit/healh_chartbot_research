#!/bin/bash

echo "📦 Monitoring Backend Installation..."
echo ""
echo "This will take 10-20 minutes depending on your internet speed."
echo "Press Ctrl+C to stop monitoring (installation continues in background)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

while true; do
    clear
    echo "📦 Backend Installation Progress"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Check if process is still running
    if ps -p 14998 > /dev/null 2>&1; then
        echo "⏳ Status: INSTALLING..."
        echo ""
        echo "📋 Recent activity:"
        tail -15 ../install.log 2>/dev/null || echo "Waiting for logs..."
    else
        echo "✅ Status: COMPLETED!"
        echo ""
        echo "📋 Final output:"
        tail -30 ../install.log
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "🚀 Installation complete! You can now run:"
        echo "   ./start-backend.sh"
        echo ""
        break
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Last updated: $(date '+%H:%M:%S')"
    echo ""
    
    sleep 10
done
