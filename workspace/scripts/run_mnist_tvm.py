import tvm
from tvm.contrib import graph_executor
import numpy as np
import torch
import os

MODEL_DIR = "/root/workspace/models"
compiled_model_path = os.path.join(MODEL_DIR, "mnist_model_tvm.so")

print("[4] Load compiled module")
lib = tvm.runtime.load_module(compiled_model_path)
dev = tvm.cpu()
module = graph_executor.GraphModule(lib["default"](dev))

print("[5] Run inference")
dummy_input = torch.randn(1, 1, 28, 28).numpy().astype("float32")
module.set_input("input", dummy_input)
module.run()
output = module.get_output(0).asnumpy()

print("Inference result shape:", output.shape)

print("[6] Benchmark")
ftimer = module.module.time_evaluator("run", dev, number=10)
print("Latency (ms):", ftimer().mean * 1000)

