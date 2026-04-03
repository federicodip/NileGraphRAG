#!/usr/bin/bash -l
#SBATCH --job-name=cot-full
#SBATCH --time=08:00:00
#SBATCH --mem=48G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --constraint="GPUMEM80GB|GPUMEM96GB|GPUMEM140GB"
#SBATCH --partition=lowprio
#SBATCH --chdir=/home/fdipas/nilegraphrag
#SBATCH --output=logs/cot-full-%j.out
#SBATCH --error=logs/cot-full-%j.err
set -e

unset HTTP_PROXY
unset http_proxy
export NO_PROXY=localhost,127.0.0.1
export no_proxy=localhost,127.0.0.1

module load apptainer

CTR_OLLAMA=~/scratch/graphRAG/containers/ollama.sif
CTR_APP=/scratch/fdipas/tellusgraph/tellusgraph.sif
MODELS_DIR=/scratch/fdipas/graphRAG/ollama

# --- Choose model ---
# gemma3:12b  = ~3s/chunk → ~9600 chunks per 8h job → ~19 jobs total
# gemma3:27b  = ~7s/chunk → ~4100 chunks per 8h job → ~44 jobs total
COT_MODEL="${COT_MODEL:-gemma3:12b}"

echo "=== Starting Ollama server ==="
HTTPS_PROXY=http://10.129.62.115:3128 \
    OLLAMA_MAX_LOADED_MODELS=1 \
    apptainer exec --nv \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env HTTPS_PROXY=http://10.129.62.115:3128 \
    --env NO_PROXY=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama serve &
sleep 20

echo "=== Model: $COT_MODEL ==="
echo "=== Running COT (with resume) ==="
apptainer exec \
    --env NO_PROXY=localhost,127.0.0.1 \
    --env no_proxy=localhost,127.0.0.1 \
    --env COT_MODEL=$COT_MODEL \
    $CTR_APP python translate/cot.py \
        --input /scratch/fdipas/tellusgraph/data/processed/rag/chunks.jsonl \
        --output data/cot_full.jsonl \
        --vocab vocab/ecology_v01.yaml \
        --batch-size 50

DONE=$(wc -l < data/cot_full.jsonl 2>/dev/null || echo 0)
echo "=== Done this run: $DONE total chunks translated ==="
echo "=== Resubmit this job to continue (resume is automatic) ==="
