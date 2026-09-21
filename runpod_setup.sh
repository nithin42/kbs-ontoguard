#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "  Setting up RunPod Environment for KBS Research Benchmark"
echo "=========================================================="

# Ensure GPU is visible
nvidia-smi

# Update pip
python3 -m pip install --upgrade pip

# Install PyTorch dependencies and project requirements
echo "[1/3] Installing Python dependencies..."
pip install -r requirements.txt

# Create results and cache directories
echo "[2/3] Creating directory structure..."
mkdir -p results/plots
mkdir -p data/cache

# Verify installation
echo "[3/3] Verifying environment..."
python3 -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()} | Devices: {torch.cuda.device_count()}')"
python3 -c "import outlines; print('Outlines successfully imported')"
python3 -c "import datasets; print('Datasets library ready')"

echo "=========================================================="
echo "  Setup Complete! Ready to execute experiments:"
echo "  python3 scripts/run_experiments.py --model meta-llama/Meta-Llama-3-8B-Instruct --samples 300"
echo "=========================================================="
