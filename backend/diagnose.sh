#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         ZNPHI Backend - System Diagnostic Report              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 System Information:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
lsb_release -d 2>/dev/null || echo "Ubuntu version: Unknown"
echo ""

echo "🐍 Python Status:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v python3 &> /dev/null; then
    echo "✅ Python3: $(python3 --version)"
    echo "   Location: $(which python3)"
else
    echo "❌ Python3: Not found"
fi
echo ""

echo "📦 Pip Status:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v pip3 &> /dev/null; then
    echo "✅ pip3: $(pip3 --version)"
else
    echo "❌ pip3: Not found"
    echo "   Trying python3 -m pip..."
    if python3 -m pip --version &> /dev/null; then
        echo "✅ pip module: $(python3 -m pip --version)"
    else
        echo "❌ pip module: Not found"
    fi
fi
echo ""

echo "💾 Disk Space:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
df -h / | grep -E "Filesystem|/"
echo ""

echo "🔒 Package Manager Locks:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if ls /var/lib/dpkg/lock* &> /dev/null; then
    echo "⚠️  Lock files exist (another package manager may be running)"
    ls -lh /var/lib/dpkg/lock* 2>/dev/null
else
    echo "✅ No lock files found"
fi
echo ""

echo "🔧 Recommended Action:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is not installed"
    echo ""
    echo "Run this command to install:"
    echo "   sudo apt update && sudo apt install -y python3-pip python3-venv"
    echo ""
    echo "If that fails, try:"
    echo "   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
    echo "   python3 get-pip.py --user"
else
    echo "✅ pip is installed! You can proceed with:"
    echo "   ./start-backend.sh"
fi
echo ""
