#!/usr/bin/bash -l
#SBATCH --job-name=pull-models
#SBATCH --time=02:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --constraint="GPUMEM80GB|GPUMEM96GB|GPUMEM140GB"
#SBATCH --partition=lowprio
#SBATCH --chdir=/home/fdipas/nilegraphrag
#SBATCH --output=logs/pull-%j.out
#SBATCH --error=logs/pull-%j.err
set -e

# Unset HTTP_PROXY globally — it breaks ollama pull (client→server is localhost HTTP)
unset HTTP_PROXY
unset http_proxy
export NO_PROXY=localhost,127.0.0.1
export no_proxy=localhost,127.0.0.1

module load apptainer

CTR_OLLAMA=~/scratch/graphRAG/containers/ollama.sif
MODELS_DIR=/scratch/fdipas/graphRAG/ollama

echo "=== Starting Ollama server ==="
HTTPS_PROXY=http://10.129.62.115:3128 \
    apptainer exec --nv \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env HTTPS_PROXY=http://10.129.62.115:3128 \
    --env NO_PROXY=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama serve &
sleep 20

echo "=== Pulling gemma3:27b ==="
apptainer exec \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env NO_PROXY=localhost,127.0.0.1 \
    --env no_proxy=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama pull gemma4:31b

echo "=== Pulling qwen3:32b ==="
apptainer exec \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env NO_PROXY=localhost,127.0.0.1 \
    --env no_proxy=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama pull gemma4:26b

echo "=== Listing available models ==="
apptainer exec \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env NO_PROXY=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama list

echo "=== Done ==="
