#!/usr/bin/bash -l
#SBATCH --job-name=cot-500
#SBATCH --time=03:00:00
#SBATCH --mem=48G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --constraint="GPUMEM80GB|GPUMEM96GB|GPUMEM140GB"
#SBATCH --partition=lowprio
#SBATCH --chdir=/home/fdipas/nilegraphrag
#SBATCH --output=logs/cot-500-%j.out
#SBATCH --error=logs/cot-500-%j.err
set -e

unset HTTP_PROXY
unset http_proxy
export NO_PROXY=localhost,127.0.0.1
export no_proxy=localhost,127.0.0.1

module load apptainer

CTR_OLLAMA=~/scratch/graphRAG/containers/ollama.sif
CTR_APP=/scratch/fdipas/tellusgraph/tellusgraph.sif
MODELS_DIR=/scratch/fdipas/graphRAG/ollama

echo "=== Starting Ollama server ==="
HTTPS_PROXY=http://10.129.62.115:3128 \
    OLLAMA_MAX_LOADED_MODELS=1 \
    apptainer exec --nv \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env HTTPS_PROXY=http://10.129.62.115:3128 \
    --env NO_PROXY=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama serve &
sleep 20

echo "=== Running COT on 500 validation chunks ==="
apptainer exec \
    --env NO_PROXY=localhost,127.0.0.1 \
    --env no_proxy=localhost,127.0.0.1 \
    $CTR_APP python translate/cot.py \
        --input data/validation_sample_500.jsonl \
        --output data/validation_cot_500.jsonl \
        --vocab vocab/ecology_v01.yaml \
        --batch-size 25

echo "=== Done: $(wc -l < data/validation_cot_500.jsonl) chunks translated ==="
