#!/usr/bin/bash -l
#SBATCH --job-name=cot-ab-test
#SBATCH --time=02:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --constraint="GPUMEM80GB|GPUMEM96GB|GPUMEM140GB"
#SBATCH --partition=lowprio
#SBATCH --chdir=/home/fdipas/nilegraphrag
#SBATCH --output=logs/cot-ab-%j.out
#SBATCH --error=logs/cot-ab-%j.err
set -e

module load apptainer

echo "=== Starting Ollama server ==="
HTTPS_PROXY=http://10.129.62.115:3128 HTTP_PROXY=http://10.129.62.115:3128 \
    OLLAMA_MAX_LOADED_MODELS=1 \
    apptainer exec --nv --env OLLAMA_MODELS=/scratch/fdipas/graphRAG/ollama \
    ~/scratch/graphRAG/containers/ollama.sif ollama serve &
sleep 15

echo "=== Pulling models (if not cached) ==="
HTTPS_PROXY=http://10.129.62.115:3128 HTTP_PROXY=http://10.129.62.115:3128 \
    apptainer exec --env OLLAMA_MODELS=/scratch/fdipas/graphRAG/ollama \
    ~/scratch/graphRAG/containers/ollama.sif ollama pull gemma3:27b

HTTPS_PROXY=http://10.129.62.115:3128 HTTP_PROXY=http://10.129.62.115:3128 \
    apptainer exec --env OLLAMA_MODELS=/scratch/fdipas/graphRAG/ollama \
    ~/scratch/graphRAG/containers/ollama.sif ollama pull qwen3:32b

echo "=== Running A/B test ==="
apptainer exec \
    --env NO_PROXY=localhost,127.0.0.1 \
    --env no_proxy=localhost,127.0.0.1 \
    /scratch/fdipas/tellusgraph/tellusgraph.sif \
    python test_cot_ab.py \
        --input data/test_sample_10.jsonl \
        --vocab vocab/ecology_v01.yaml \
        --output data/cot_ab_results.json

echo "=== Done ==="
