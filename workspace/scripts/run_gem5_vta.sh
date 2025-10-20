#!/usr/bin/env bash
set -e
MODEL_SO=${1:-/root/workspace/tvm_build/mnist.so}
GEM5_DIR=${GEM5_DIR:-/root/gem5}
OUTROOT=${OUTROOT:-/root/workspace/results}
TS=$(date +%Y%m%d-%H%M%S)
OUTDIR="$OUTROOT/$(basename ${MODEL_SO%.*})-$TS"
mkdir -p "$OUTDIR"

# 자동으로 적절한 config 찾기 (우선 example/se/basic.py)
if [ -f "$GEM5_DIR/configs/vta/vta_example.py" ]; then
  CONFIG="$GEM5_DIR/configs/vta/vta_example.py"
elif [ -f "$GEM5_DIR/configs/example/se/basic.py" ]; then
  CONFIG="$GEM5_DIR/configs/example/se/basic.py"
else
  echo "No suitable gem5 config found under $GEM5_DIR/configs"
  exit 1
fi

echo "[+] Using config: $CONFIG"
pushd "$GEM5_DIR" >/dev/null
# 실행: gem5에서 python 인터프리터로 run_inference.py 호출
./build/ARM/gem5.opt "$CONFIG" --cmd=/usr/bin/python3 --options="/root/workspace/run_inference.py ${MODEL_SO}" 2>&1 | tee "$OUTDIR/gem5.log"
RET=${PIPESTATUS[0]}
popd

# 복사 m5out -> OUTDIR
if [ -d "$GEM5_DIR/m5out" ]; then
  cp -r "$GEM5_DIR/m5out" "$OUTDIR/"
fi

echo "[+] Results saved in $OUTDIR (exit code $RET)"
exit $RET

