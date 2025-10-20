FROM ubuntu:22.04

# 1. 기본 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. 사용자 계정 생성 및 sudo 권한 부여
RUN useradd -m -s /bin/bash eddi \
    && echo "eddi:eddi@123" | chpasswd \
    && usermod -aG sudo eddi \
    && echo "eddi ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER eddi
WORKDIR /home/eddi

# 3. 필수 개발 패키지 설치 (eddi 계정으로도 sudo 가능)
RUN sudo apt-get update && sudo apt-get install -y \
    autoconf \
    automake \
    libtool \
    pkg-config \
    python3 \
    python3-pip \
    python3-dev \
    zlib1g-dev \
    libssl-dev \
    universal-ctags \
    kmod \
    && sudo rm -rf /var/lib/apt/lists/*

# 4. 파이썬 패키지 업그레이드
RUN python3 -m pip install --upgrade pip setuptools wheel

# 5. Miniforge 설치 (Conda)
RUN wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O /tmp/miniforge.sh && \
    bash /tmp/miniforge.sh -b -p /home/eddi/miniforge && \
    rm /tmp/miniforge.sh

# 6. Conda 경로 설정
ENV PATH=/home/eddi/miniforge/bin:$PATH

# 7. Conda base 환경 활성화
RUN /home/eddi/miniforge/bin/conda init bash
SHELL ["/bin/bash", "-c"]

# 8. 작업 디렉토리
WORKDIR /workspace

# 기본 셸
CMD ["/bin/bash"]

