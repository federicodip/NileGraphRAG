#!/usr/bin/bash -l
#SBATCH --job-name=smoke-test
#SBATCH --time=00:30:00
#SBATCH --mem=48G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --constraint="GPUMEM80GB|GPUMEM96GB|GPUMEM140GB"
#SBATCH --partition=lowprio
#SBATCH --chdir=/home/fdipas/nilegraphrag
#SBATCH --output=logs/smoke-%j.out
#SBATCH --error=logs/smoke-%j.err
set -e

COT_MODEL="${COT_MODEL:-gemma4:31b}"

unset HTTP_PROXY
unset http_proxy
export NO_PROXY=localhost,127.0.0.1
export no_proxy=localhost,127.0.0.1

module load apptainer

CTR_OLLAMA=~/scratch/graphRAG/containers/ollama.sif
CTR_APP=/scratch/fdipas/tellusgraph/tellusgraph.sif
MODELS_DIR=/scratch/fdipas/graphRAG/ollama

echo "=== Smoke test: ${COT_MODEL} ==="

HTTPS_PROXY=http://10.129.62.115:3128 \
    OLLAMA_MAX_LOADED_MODELS=1 \
    apptainer exec --nv \
    --env OLLAMA_MODELS=$MODELS_DIR \
    --env HTTPS_PROXY=http://10.129.62.115:3128 \
    --env NO_PROXY=localhost,127.0.0.1 \
    $CTR_OLLAMA ollama serve &
sleep 20

apptainer exec \
    --env NO_PROXY=localhost,127.0.0.1 \
    --env no_proxy=localhost,127.0.0.1 \
    --env COT_MODEL=$COT_MODEL \
    $CTR_APP python translate/cot.py \
        --input data/test_sample_10.jsonl \
        --output data/smoke_test_output.jsonl \
        --vocab vocab/ecology_v01.yaml \
        --no-resume

echo "=== Results ==="
wc -l data/smoke_test_output.jsonl
head -1 data/smoke_test_output.jsonl | python -c "import sys,json; r=json.loads(sys.stdin.read()); print(f'Model: {r.get(\"cot_model\",\"?\")}, COT length: {len(r.get(\"cot_english\",\"\"))}, JSON valid: True')"
echo "=== Done ==="
