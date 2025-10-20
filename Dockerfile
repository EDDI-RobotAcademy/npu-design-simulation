FROM ubuntu:22.04

ARG LLVM_VERSION=14
ARG PYTHON_VERSION=3.10

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

# Timezone & 필수 패키지 설치 (캐시 최적화)
RUN apt-get update && apt-get install -y tzdata \
    && ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && apt-get install -y \
        build-essential git cmake ninja-build wget curl unzip pkg-config \
        python${PYTHON_VERSION} python3-pip python3-dev python3-setuptools \
        llvm-${LLVM_VERSION} llvm-${LLVM_VERSION}-dev llvm-${LLVM_VERSION}-tools \
        clang-${LLVM_VERSION} libclang-${LLVM_VERSION}-dev \
        libedit-dev libxml2-dev zlib1g-dev libtinfo-dev scons m4 \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치 (캐시 최적화)
RUN python3 -m pip install --upgrade pip wheel setuptools \
    && python3 -m pip install \
        numpy scipy decorator tornado onnx attrs pytest pytest-xdist synr mypy pylint autopep8

# 환경 변수 설정 파일 생성
RUN echo "export TVM_HOME=/root/tvm" > /etc/profile.d/tvm_env.sh \
    && echo "export GEM5_HOME=/root/gem5" >> /etc/profile.d/tvm_env.sh \
    && echo "export PYTHONPATH=\$TVM_HOME/python:\$TVM_HOME/vta/python:\$PYTHONPATH" >> /etc/profile.d/tvm_env.sh \
    && echo "export LD_LIBRARY_PATH=\$TVM_HOME/build:\$LD_LIBRARY_PATH" >> /etc/profile.d/tvm_env.sh

# TVM 복사 및 빌드
COPY tvm /root/tvm
WORKDIR /root/tvm
RUN mkdir -p build && cp cmake/config.cmake build/ \
    && sed -i "s|USE_LLVM OFF|USE_LLVM ON|" build/config.cmake \
    && sed -i "s|USE_VTA OFF|USE_VTA ON|" build/config.cmake \
    && echo "set(USE_LLVM /usr/bin/llvm-config-${LLVM_VERSION})" >> build/config.cmake \
    && cd build && cmake .. && make -j$(nproc)

# TVM Python 바인딩 설치
WORKDIR /root/tvm/python
RUN python3 -m pip install -e .

# gem5 복사 및 빌드
COPY gem5 /root/gem5
WORKDIR /root/gem5
RUN scons build/ARM/gem5.opt -j$(nproc)

# TVM + Relay + VTA Import 테스트
WORKDIR /root/tvm/python
RUN /bin/bash -c "source /etc/profile.d/tvm_env.sh && \
    python3 -c 'import tvm; print(\"TVM version:\", tvm.__version__)' && \
    python3 -c 'from tvm import relay; print(\"Relay OK\")' && \
    python3 -c 'import vta; print(\"VTA OK\")'"

# Gem5 실행 준비
WORKDIR /root/gem5
CMD ["/bin/bash"]

