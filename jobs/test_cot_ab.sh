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

# Unset HTTP_PROXY — it breaks ollama client→server communication on localhost
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
    OLLAMA_MAX_LOADED_MODELS=2 \
    apptainer exec --nv \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env HTTPS_PROXY=http://10.129.62.115:3128 \
    --env NO_PROXY=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama serve &
sleep 20

echo "=== Verifying models ==="
apptainer exec \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env NO_PROXY=localhost,127.0.0.1 \
    --env no_proxy=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama list

echo "=== Running A/B test ==="
apptainer exec \
    --env NO_PROXY=localhost,127.0.0.1 \
    --env no_proxy=localhost,127.0.0.1 \
    $CTR_APP python test_cot_ab.py \
        --input data/test_sample_10.jsonl \
        --vocab vocab/ecology_v01.yaml \
        --output data/cot_ab_results.json

echo "=== Done ==="
