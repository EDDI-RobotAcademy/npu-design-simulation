#!/usr/bin/env python3
# 인수: 모델 경로
import sys, os
model_so = sys.argv[1] if len(sys.argv)>1 else "/root/workspace/tvm_build/mnist.so"
print("Using model:", model_so)

import tvm
from tvm.contrib import graph_executor
import numpy as np

lib = tvm.runtime.load_module(model_so)
dev = tvm.cpu(0)
module = graph_executor.GraphModule(lib["default"](dev))

# 더미 입력 (MNIST)
data = np.random.rand(1,1,28,28).astype("float32")
module.set_input("input", data)
import time
t0=time.time()
module.run()
t1=time.time()
out = module.get_output(0).asnumpy()
print("Output argmax:", out.argmax(), "elapsed(s):", t1-t0)

