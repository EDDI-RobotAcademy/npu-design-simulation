#!/usr/bin/env bash
# scripts/build_vta_sim.sh
set -e
TVM_DIR=${TVM_DIR:-/root/tvm}

if [ ! -d "$TVM_DIR" ]; then
  echo "ERROR: TVM directory not found at $TVM_DIR"
  exit 1
fi

echo "[+] Building VTA simulator (if present) in $TVM_DIR/vta ..."
if [ -d "$TVM_DIR/vta/sim" ]; then
  pushd "$TVM_DIR/vta/sim"
  # Many tvm branches use a Makefile in vta/sim
  if [ -f Makefile ]; then
    echo "[+] Running make in $(pwd)"
    make -j$(nproc)
  else
    echo "No Makefile in vta/sim. Check TVM/VTA version and build instructions."
  fi
  popd
else
  echo "No vta/sim directory found. Your TVM might not include VTA or path differs."
  echo "List of top-level dirs in $TVM_DIR:"
  ls -1 "$TVM_DIR"
fi

echo "[+] Build step finished. If vta/sim produced a simulator binary, note its path."

