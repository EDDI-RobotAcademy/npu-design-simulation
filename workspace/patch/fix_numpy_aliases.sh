#!/bin/bash
echo "[INFO] Restoring deprecated numpy aliases via sitecustomize.py ..."

SITE_DIR=$(python3 -c "import site; print(site.getsitepackages()[0])")
TARGET=$SITE_DIR/sitecustomize.py

cat << 'EOF' > $TARGET
import numpy as np

# Restore deprecated numpy aliases for legacy code
if not hasattr(np, "int"):
    np.int = int
if not hasattr(np, "float"):
    np.float = float
if not hasattr(np, "bool"):
    np.bool = bool
if not hasattr(np, "complex"):
    np.complex = complex
EOF

echo "[INFO] Patched $TARGET"
echo "[INFO] Now np.int, np.float, np.bool, np.complex are available again."

