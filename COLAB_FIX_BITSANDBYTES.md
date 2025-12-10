# Fix bitsandbytes Error in Colab

## 🔧 Solution: Add This to the TOP of Your Notebook

### Step 1: Create a NEW CELL at the very beginning

Click **"+ Code"** at the top of your notebook to add a cell BEFORE all other code.

### Step 2: Copy and paste this code:

```python
# ============================================================
# INSTALL ALL REQUIRED PACKAGES
# Run this cell FIRST before anything else
# ============================================================

print("📦 Installing required packages...")

# Install bitsandbytes with specific version for Colab compatibility
!pip install -q bitsandbytes==0.41.0

# Install other required packages
!pip install -q -U \
    transformers==4.36.0 \
    accelerate==0.25.0 \
    peft==0.7.0 \
    datasets==2.15.0 \
    trl==0.7.4

print("✅ All packages installed!")

# Verify bitsandbytes is installed
try:
    import bitsandbytes as bnb
    print(f"✅ bitsandbytes version: {bnb.__version__}")
except ImportError as e:
    print(f"❌ Error: {e}")
    print("Trying alternative installation...")
    !pip install -q bitsandbytes --no-cache-dir
    import bitsandbytes as bnb
    print(f"✅ bitsandbytes version: {bnb.__version__}")
```

### Step 3: Run this cell FIRST

Click the play button ▶️ on this new cell and wait for it to complete.

### Step 4: Then run the rest of your notebook

After this completes successfully, run your other cells as normal.

---

## 🔄 Alternative Fix: Restart Runtime

If the above doesn't work, try this:

```python
# Install packages
!pip install -q bitsandbytes==0.41.0 transformers accelerate peft datasets trl

# IMPORTANT: Restart runtime after installation
import os
os.kill(os.getpid(), 9)
```

After running this:
1. You'll see "Your session crashed"
2. Click **"Reconnect"**
3. Run ALL cells again from the beginning

---

## 🐛 Common Issues and Fixes

### Issue 1: "CUDA not available"
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
```

If CUDA is not available:
- Go to **Runtime** → **Change runtime type**
- Set **Hardware accelerator** to **GPU** (T4 or better)
- Click **Save**

### Issue 2: "Module 'bitsandbytes' has no attribute 'XXX'"
This usually means version mismatch. Use specific versions:

```python
!pip uninstall -y bitsandbytes
!pip install -q bitsandbytes==0.41.0
```

### Issue 3: Environment was reset
Colab resets after 12 hours of inactivity. You need to:
1. Reinstall all packages (run the first cell again)
2. Re-run all cells

---

## ✅ Complete Setup Cell (Copy This)

Put this at the VERY TOP of your notebook:

```python
# ============================================================
# COMPLETE SETUP - RUN THIS FIRST
# ============================================================

import os
import sys

print("="*70)
print("ZNPHI Measles Chatbot - Environment Setup")
print("="*70)

# Check GPU
import torch
print(f"\n✓ PyTorch version: {torch.__version__}")
print(f"✓ CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"✓ CUDA version: {torch.version.cuda}")
    print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
else:
    print("❌ WARNING: No GPU detected!")
    print("   Go to Runtime → Change runtime type → Set to GPU")

# Install packages
print("\n📦 Installing packages...")
!pip install -q bitsandbytes==0.41.0
!pip install -q transformers==4.36.0
!pip install -q accelerate==0.25.0
!pip install -q peft==0.7.0
!pip install -q datasets==2.15.0
!pip install -q trl==0.7.4

# Verify installations
print("\n✅ Verifying installations...")
try:
    import bitsandbytes as bnb
    print(f"✓ bitsandbytes: {bnb.__version__}")
except Exception as e:
    print(f"❌ bitsandbytes: {e}")

try:
    import transformers
    print(f"✓ transformers: {transformers.__version__}")
except Exception as e:
    print(f"❌ transformers: {e}")

try:
    import peft
    print(f"✓ peft: {peft.__version__}")
except Exception as e:
    print(f"❌ peft: {e}")

try:
    import accelerate
    print(f"✓ accelerate: {accelerate.__version__}")
except Exception as e:
    print(f"❌ accelerate: {e}")

print("\n" + "="*70)
print("✅ Setup complete! You can now run the rest of the notebook.")
print("="*70)
```

---

## 🎯 Quick Checklist

Before training:
- ✅ GPU is enabled (Runtime → Change runtime type → GPU)
- ✅ All packages installed (run setup cell)
- ✅ No errors in setup cell output
- ✅ bitsandbytes version shows correctly

---

## 📝 Notes

1. **Always run setup cell first** after starting/restarting Colab
2. **GPU must be enabled** for bitsandbytes to work
3. **Don't skip package installation** - even if you installed before
4. **Colab resets** after 12 hours - you'll need to reinstall

---

## 🆘 Still Having Issues?

If bitsandbytes still won't install:

**Option 1: Use older compatible version**
```python
!pip install bitsandbytes==0.37.0
```

**Option 2: Train without 4-bit quantization**
Remove or comment out the quantization config in your training code:
```python
# Comment out or remove:
# bnb_config = BitsAndBytesConfig(...)
# load_in_4bit=True,
```

**Option 3: Use different Colab GPU**
- Try switching to a different GPU type
- Runtime → Change runtime type → Try T4, A100, or V100

---

Copy the "Complete Setup Cell" above and put it at the very top of your Colab notebook!
