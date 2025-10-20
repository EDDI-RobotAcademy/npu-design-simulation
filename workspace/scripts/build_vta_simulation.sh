#!/usr/bin/env bash
set -e
TVM_DIR=${TVM_DIR:-/root/tvm}

if [ ! -d "$TVM_DIR/vta" ]; then
  echo "No vta directory in $TVM_DIR (VTA not present)"
  exit 1
fi

pushd "$TVM_DIR/vta/sim" >/dev/null 2>&1 || { echo "vta/sim not found"; exit 1; }
if [ -f Makefile ]; then
  make -j8
  echo "VTA sim built"
else
  echo "No Makefile in vta/sim; check TVM/VTA branch"
fi
popd

