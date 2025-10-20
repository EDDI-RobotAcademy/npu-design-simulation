#!/bin/bash
TVM_DIR=/root/tvm/python/tvm

echo "[INFO] Patching TVM numpy compatibility..."

grep -rl "np.int" $TVM_DIR | while read file; do
  echo "Fixing int types in $file ..."
  sed -i -E 's/\bnp\.int(32|64)?\b/int/g' "$file"
done

grep -rl "np.float" $TVM_DIR | while read file; do
  echo "Fixing float types in $file ..."
  sed -i -E 's/\bnp\.float(32|64)?\b/float/g' "$file"
done

grep -rl "\bint(32|64)\b" $TVM_DIR | while read file; do
  echo "Fixing stray int32/int64 in $file ..."
  sed -i -E 's/\bint(32|64)\b/int/g' "$file"
done

grep -rl "\bfloat(32|64)\b" $TVM_DIR | while read file; do
  echo "Fixing stray float32/float64 in $file ..."
  sed -i -E 's/\bfloat(32|64)\b/float/g' "$file"
done

grep -rl "isinstance" $TVM_DIR | while read file; do
  sed -i 's/(str, int, float/(str, int, float, np.integer, np.floating/g' "$file"
done

echo "[INFO] Patch complete. Please retry your TVM conversion."

