#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "  Setting up RunPod Environment for KBS Research Benchmark"
echo "=========================================================="

# Check NVIDIA GPU presence and memory
echo "[0/3] Checking GPU hardware..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
else
    echo "[Warning] nvidia-smi not found. Ensure you are on a GPU instance."
fi

# Upgrade pip and wheel
echo "[1/3] Updating pip and installing core scientific dependencies..."
python3 -m pip install --upgrade pip setuptools wheel

# Install PyTorch dependencies and project requirements
pip install -r requirements.txt

# Create results and cache directories
echo "[2/3] Preparing output directories..."
mkdir -p results/plots
mkdir -p data/cache

# Verify core research dependencies
echo "[3/3] Verifying environment & compilation capabilities..."
python3 -c "import torch; print(f'PyTorch: {torch.__version__} | CUDA Available: {torch.cuda.is_available()}')"
python3 -c "import transformers; print(f'Transformers: {transformers.__version__}')"
python3 -c "import outlines; print('Outlines neuro-symbolic grammar compiler: READY')"
python3 -c "import matplotlib; print('Matplotlib publication plotting engine: READY')"

echo "=========================================================="
echo "  Setup Complete! Ready to execute experiments."
echo "  Fast verification run:"
echo "    python3 scripts/run_experiments.py --samples 50"
echo "  Full Q1 publication benchmark:"
echo "    python3 scripts/run_experiments.py --samples 300"
echo "=========================================================="
