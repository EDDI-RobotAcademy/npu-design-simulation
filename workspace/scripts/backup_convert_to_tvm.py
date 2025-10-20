#!/usr/bin/env python3

import argparse
import os
import sys
import builtins
import numpy as np

# -------------------------
# numpy compatibility fix
# -------------------------
if not hasattr(np, "int"):
    np.int = int
if not hasattr(np, "float"):
    np.float = float
if not hasattr(np, "bool"):
    np.bool = bool

if "_int32" not in globals():
    _int32 = np.int32

if not hasattr(builtins, "int32"):
    builtins.int32 = np.int32
if not hasattr(builtins, "_int32"):
    builtins._int32 = np.int32
if not hasattr(builtins, "float32"):
    builtins.float32 = np.float32
if not hasattr(builtins, "_float32"):
    builtins._float32 = np.float32
if not hasattr(builtins, "bool_"):
    builtins.bool_ = np.bool_
if not hasattr(builtins, "_bool"):
    builtins._bool = np.bool_

# -------------------------
# argument parsing
# -------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--name", required=True)
parser.add_argument("--shape", required=True)  # e.g. "input:1,1,28,28"
parser.add_argument("--target", default="llvm")
parser.add_argument("--outdir", default="/root/workspace/tvm_build")
args = parser.parse_args()

try:
    import tvm
    from tvm import relay
    import onnx
    import tvm.contrib.graph_executor as runtime
except Exception as e:
    print("TVM import failed:", e)
    sys.exit(1)

iname, dims = args.shape.split(":")
shape = tuple(int(x) for x in dims.split(","))
shape_dict = {iname: shape}

# -------------------------
# Load ONNX model
# -------------------------
onnx_model = onnx.load(args.input)
mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)

os.makedirs(args.outdir, exist_ok=True)

target = args.target
print("Building for target:", target)
if target == "vta":
    tvm_target = "vta"
else:
    tvm_target = "llvm"

# -------------------------
# Build with TVM
# -------------------------
with tvm.transform.PassContext(opt_level=3):
    lib = relay.build(mod, target=tvm_target, params=params)

out_lib = os.path.join(args.outdir, f"{args.name}.so")
lib.export_library(out_lib)

# -------------------------
# Save graph and params
# -------------------------
graph_json_path = os.path.join(args.outdir, f"{args.name}_graph.json")
with open(graph_json_path, "w") as f:
    f.write(lib.get_graph_json())

params_path = os.path.join(args.outdir, f"{args.name}_params.params")
with open(params_path, "wb") as f:
    f.write(tvm.runtime.save_param_dict(lib.get_params()))

print(f"[+] Model compiled and saved to {args.outdir}")
print(f"[+] Graph JSON: {graph_json_path}")
print(f"[+] Params: {params_path}")

