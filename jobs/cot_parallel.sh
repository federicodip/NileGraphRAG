#!/usr/bin/bash -l
#SBATCH --job-name=cot-shard
#SBATCH --time=08:00:00
#SBATCH --mem=48G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --constraint="GPUMEM80GB|GPUMEM96GB|GPUMEM140GB"
#SBATCH --partition=lowprio
#SBATCH --chdir=/home/fdipas/nilegraphrag
#SBATCH --output=logs/cot-shard%a-%j.out
#SBATCH --error=logs/cot-shard%a-%j.err
#SBATCH --array=0-7
#SBATCH --exclusive
set -e

# ---------------------------------------------------------------
# Parallel COT using Slurm job arrays.
# Submit with:  sbatch jobs/cot_parallel.sh
#
# This launches 8 GPU jobs (shards 0-7). Each processes 1/8 of
# the chunks and writes to its own output file. Resume-safe.
#
# To change number of shards: edit --array above AND NUM_SHARDS.
# To use gemma3:12b (faster): change COT_MODEL below.
# ---------------------------------------------------------------

NUM_SHARDS=8
COT_MODEL="gemma4:31b"
LIMIT_FLAG="${COT_LIMIT:+--limit $COT_LIMIT}"

unset HTTP_PROXY
unset http_proxy
export NO_PROXY=localhost,127.0.0.1
export no_proxy=localhost,127.0.0.1

module load apptainer

CTR_OLLAMA=~/scratch/graphRAG/containers/ollama.sif
CTR_APP=/scratch/fdipas/tellusgraph/tellusgraph.sif
MODELS_DIR=/scratch/fdipas/graphRAG/ollama

# Each shard gets its own Ollama port to avoid collisions on shared nodes
OLLAMA_PORT=$((11434 + SLURM_ARRAY_TASK_ID))

echo "=== Shard ${SLURM_ARRAY_TASK_ID}/${NUM_SHARDS} | Model: ${COT_MODEL} | Port: ${OLLAMA_PORT} ==="

echo "=== Starting Ollama server on port ${OLLAMA_PORT} ==="
HTTPS_PROXY=http://10.129.62.115:3128 \
    OLLAMA_MAX_LOADED_MODELS=1 \
    OLLAMA_HOST=0.0.0.0:${OLLAMA_PORT} \
    apptainer exec --nv \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env OLLAMA_HOST=0.0.0.0:${OLLAMA_PORT} \
    --env HTTPS_PROXY=http://10.129.62.115:3128 \
    --env NO_PROXY=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama serve &
sleep 20

echo "=== Running COT shard ${SLURM_ARRAY_TASK_ID} ==="
apptainer exec \
    --env NO_PROXY=localhost,127.0.0.1 \
    --env no_proxy=localhost,127.0.0.1 \
    --env COT_MODEL=$COT_MODEL \
    --env OLLAMA_BASE_URL=http://localhost:${OLLAMA_PORT} \
    $CTR_APP python translate/cot.py \
        --input /scratch/fdipas/tellusgraph/data/processed/rag/chunks.jsonl \
        --output data/cot_full.jsonl \
        --vocab vocab/ecology_v01.yaml \
        --batch-size 50 \
        --shard ${SLURM_ARRAY_TASK_ID} \
        --num-shards ${NUM_SHARDS} \
        ${LIMIT_FLAG}

echo "=== Shard ${SLURM_ARRAY_TASK_ID} done ==="
