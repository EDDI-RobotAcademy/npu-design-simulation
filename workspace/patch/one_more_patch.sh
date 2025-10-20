#!/bin/bash
TVM_DIR=/root/tvm/python/tvm

echo "[INFO] Fixing wrong int32/float32 identifiers (not strings)..."

grep -rl "int32" $TVM_DIR | while read file; do
  echo "Checking $file ..."
  sed -i 's/\bint32\b/int/g' "$file"
done

grep -rl "int64" $TVM_DIR | while read file; do
  echo "Checking $file ..."
  sed -i 's/\bint64\b/int/g' "$file"
done

grep -rl "float32" $TVM_DIR | while read file; do
  echo "Checking $file ..."
  sed -i 's/\bfloat32\b/float/g' "$file"
done

grep -rl "float64" $TVM_DIR | while read file; do
  echo "Checking $file ..."
  sed -i 's/\bfloat64\b/float/g' "$file"
done

echo "[INFO] Identifier patch complete."

