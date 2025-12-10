#!/bin/bash

echo "🔧 Fixing Package Manager Locks..."
echo ""

# Check if any apt processes are running
echo "📋 Checking for running package managers..."
ps aux | grep -i apt | grep -v grep

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Choose an option:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Wait for other updates to finish (SAFE - Recommended)"
echo "   - Close any Software Updater windows"
echo "   - Wait 5 minutes"
echo "   - Try again"
echo ""
echo "2. Force remove locks (USE WITH CAUTION)"
echo "   - Run these commands:"
echo ""
echo "   sudo killall apt apt-get"
echo "   sudo rm /var/lib/dpkg/lock*"
echo "   sudo rm /var/lib/apt/lists/lock"
echo "   sudo rm /var/cache/apt/archives/lock"
echo "   sudo dpkg --configure -a"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "After locks are cleared, run:"
echo "   sudo apt update && sudo apt install -y python3-pip python3-venv"
echo ""
