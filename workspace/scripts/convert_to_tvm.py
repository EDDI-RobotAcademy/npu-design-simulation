import tvm
from tvm import relay
from tvm.relay import testing
import numpy as np

def main():
    print("shape: (1, 3, 224, 224)")

    # ResNet workload 생성 (TVM v0.7 방식)
    mod, params = testing.resnet.get_workload(num_classes=1000, batch_size=1)

    print("Relay module:", mod)
    print("Params keys:", list(params.keys()))

if __name__ == "__main__":
    main()

