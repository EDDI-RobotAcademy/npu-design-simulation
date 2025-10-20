#!/usr/bin/env bash
# scripts/run_gem5_vta.sh
set -e

MODEL_SO=$1
if [ -z "$MODEL_SO" ]; then
  echo "Usage: $0 /path/to/model.so [gem5-config-path (optional)]"
  exit 1
fi

GEM5_DIR=${GEM5_DIR:-/root/gem5}
OUTROOT=${OUTROOT:-/root/results}
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTDIR="$OUTROOT/$(basename ${MODEL_SO%.*})-$TIMESTAMP"
mkdir -p "$OUTDIR"

# choose config: try VTA example config if exists, else fallback to example se/basic.py
if [ -f "$GEM5_DIR/configs/vta/vta_example.py" ]; then
  CONFIG="$GEM5_DIR/configs/vta/vta_example.py"
elif [ -f "$GEM5_DIR/configs/example/se/basic.py" ]; then
  CONFIG="$GEM5_DIR/configs/example/se/basic.py"
else
  # fallback: search for se/hello.py
  if [ -f "$GEM5_DIR/configs/example/se/hello.py" ]; then
    CONFIG="$GEM5_DIR/configs/example/se/hello.py"
  else
    echo "Could not find a suitable gem5 config script under $GEM5_DIR/configs."
    echo "Please supply full config path as second argument to this script."
    exit 1
  fi
fi

echo "[+] Using gem5 config: $CONFIG"
echo "[+] Running gem5 (this may take very long)..."
pushd "$GEM5_DIR"
./build/ARM/gem5.opt "$CONFIG" --cmd="$MODEL_SO"
RET=$?
popd

echo "[+] gem5 exit code: $RET"
# copy m5out to OUTDIR (if created)
if [ -d "$GEM5_DIR/m5out" ]; then
  echo "[+] Copying m5out to $OUTDIR"
  cp -r "$GEM5_DIR/m5out" "$OUTDIR/"
  echo "[+] Results copied to $OUTDIR"
else
  echo "No m5out produced. Check gem5 logs above."
fi

exit $RET

