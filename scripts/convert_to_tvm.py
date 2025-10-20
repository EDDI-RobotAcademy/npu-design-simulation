#!/usr/bin/env python3
# scripts/convert_to_tvm.py
# Usage:
#  python3 convert_to_tvm.py --input model.onnx --name resnet50 --shape "input:1,3,224,224" --target llvm
#  python3 convert_to_tvm.py --input model.pt --name mlp --shape "input0:1,784" --target llvm

import os
import argparse
import sys
import numpy as np

def parse_shape(s):
    # "input:1,3,224,224" -> ("input", (1,3,224,224))
    name, dims = s.split(":")
    shape = tuple(int(x) for x in dims.split(","))
    return name, shape

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help=".onnx or PyTorch .pt/.pth")
    parser.add_argument("--name", required=True, help="output name prefix")
    parser.add_argument("--shape", required=True,
                        help='input shape string like "input:1,3,224,224" or "input0:1,784"')
    parser.add_argument("--target", default="llvm", help="tvm target (llvm or vta)")
    parser.add_argument("--outdir", default="/root/tvm_build", help="output dir inside container")
    args = parser.parse_args()

    try:
        import tvm
        from tvm import relay
        from tvm.contrib import utils
    except Exception as e:
        print("ERROR: TVM not found in Python environment. Ensure TVM is installed in /root/tvm and PYTHONPATH set.")
        print(e)
        sys.exit(1)

    input_name, shape = parse_shape(args.shape)
    shape_dict = {input_name: shape}

    mod = None
    params = None

    if args.input.endswith(".onnx"):
        try:
            import onnx
            onnx_model = onnx.load(args.input)
            mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)
        except Exception as e:
            print("ONNX load failed:", e)
            sys.exit(1)
    elif args.input.endswith(".pt") or args.input.endswith(".pth"):
        # PyTorch trace path
        try:
            import torch
            scripted = torch.jit.load(args.input).eval()
            mod, params = relay.frontend.from_pytorch(scripted, [(input_name, shape)])
        except Exception as e:
            print("PyTorch -> Relay conversion failed:", e)
            sys.exit(1)
    else:
        print("Unsupported input format. Provide .onnx or .pt/.pth")
        sys.exit(1)

    target = args.target
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    # Choose build target
    if target == "vta":
        tvm_target = "vta"  # requires TVM built with VTA and vta runtime available
    else:
        tvm_target = "llvm"

    print(f"[+] Building Relay for target={tvm_target} ...")
    with tvm.transform.PassContext(opt_level=3):
        lib = relay.build(mod, target=tvm_target, params=params)

    out_lib = os.path.join(outdir, f"{args.name}.so")
    print(f"[+] Exporting library to {out_lib}")
    lib.export_library(out_lib)

    # save graph & params (optional)
    graph_json = os.path.join(outdir, f"{args.name}_graph.json")
    params_bin = os.path.join(outdir, f"{args.name}_params.params")
    with open(graph_json, "w") as f:
        f.write(lib.get_graph_json())
    lib.get_params().save(params_bin)

    print("[+] Done.")
    print("Saved files:", out_lib, graph_json, params_bin)

if __name__ == "__main__":
    main()

