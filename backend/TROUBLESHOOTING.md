# Troubleshooting - ZNPHI Backend Installation

## Common Installation Errors

### Error: "E: Package 'python' has no installation candidate"

**Problem:** Trying to install `python` package, but it doesn't exist in Ubuntu repos.

**Solution:** Use `python3` instead. Python 2 is deprecated.
```bash
# Don't do this:
sudo apt install python

# Do this instead:
sudo apt install python3-pip python3-venv
```

---

### Error: "E: Unable to locate package"

**Problem:** Package repositories are out of date.

**Solution:** Update package list first:
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

---

### Error: "Permission denied" or "Are you root?"

**Problem:** Missing sudo privileges.

**Solution:** Make sure to use `sudo`:
```bash
sudo apt install python3-pip python3-venv
```

Enter your password when prompted.

---

### Error: "Could not get lock /var/lib/dpkg/lock"

**Problem:** Another package manager is running.

**Solution:** 
1. Close Software Updater or Ubuntu Software
2. Wait for any background updates to finish
3. Try again:
```bash
sudo apt install python3-pip python3-venv
```

Or force it (use carefully):
```bash
sudo killall apt apt-get
sudo rm /var/lib/apt/lists/lock
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/lock*
sudo dpkg --configure -a
sudo apt update
sudo apt install python3-pip python3-venv
```

---

### Error: "pip3: command not found" (after installation)

**Problem:** pip wasn't installed or shell needs refresh.

**Solution:**
```bash
# Try closing and reopening terminal, then:
pip3 --version

# Or use Python module directly:
python3 -m pip --version

# If still not found, reinstall:
sudo apt install --reinstall python3-pip
```

---

### Error: Network/Download Issues

**Problem:** Slow or failed downloads.

**Solution:**
```bash
# Try different mirror
sudo apt update
sudo apt install python3-pip python3-venv

# Or install from get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
```

---

### Error: "No module named 'pip'"

**Problem:** pip module is corrupted or missing.

**Solution:**
```bash
# Reinstall pip
sudo apt remove python3-pip
sudo apt install python3-pip

# Or use ensurepip
python3 -m ensurepip --upgrade
```

---

### Error: Disk Space Issues

**Problem:** Not enough space for packages.

**Solution:**
```bash
# Check available space
df -h

# Clean up
sudo apt clean
sudo apt autoremove

# Need at least 20GB free for full installation
```

---

## Alternative Installation Methods

### Method 1: Using get-pip.py (No sudo needed)
```bash
cd ~
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Method 2: Using snap (if available)
```bash
sudo snap install python3-pip
```

### Method 3: Manual pip + venv
```bash
# Install only venv first
sudo apt install python3-venv

# Create virtual environment
cd ~/Desktop/my-chatbot/backend
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install pip inside venv
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

---

## Still Having Issues?

### Share the Error Message

Please copy and paste:
1. The exact command you ran
2. The complete error message
3. Your Ubuntu version: `lsb_release -a`

### Quick Diagnostic

Run this to gather info:
```bash
echo "=== System Info ==="
lsb_release -a
echo ""
echo "=== Python Version ==="
python3 --version
echo ""
echo "=== Python Location ==="
which python3
echo ""
echo "=== Pip Status ==="
pip3 --version 2>&1 || echo "pip3 not found"
python3 -m pip --version 2>&1 || echo "pip module not found"
echo ""
echo "=== Disk Space ==="
df -h | grep -E "Filesystem|/$"
echo ""
echo "=== Package Manager Lock ==="
ls -la /var/lib/dpkg/lock* 2>&1 || echo "No locks"
```

Copy the output and we can diagnose the specific issue!

---

## Contact & Resources

- **Ubuntu Packages:** https://packages.ubuntu.com/
- **pip Documentation:** https://pip.pypa.io/
- **Python venv:** https://docs.python.org/3/library/venv.html

---

Last Updated: 2024-12-10
