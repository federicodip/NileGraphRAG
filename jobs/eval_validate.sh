#!/usr/bin/bash -l
#SBATCH --job-name=eval-cot-500
#SBATCH --time=01:00:00
#SBATCH --mem=48G
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --constraint="GPUMEM80GB|GPUMEM96GB|GPUMEM140GB"
#SBATCH --partition=lowprio
#SBATCH --chdir=/home/fdipas/nilegraphrag
#SBATCH --output=logs/eval-cot-%j.out
#SBATCH --error=logs/eval-cot-%j.err
set -e

module load apptainer

CTR_APP=/scratch/fdipas/tellusgraph/tellusgraph.sif

echo "=== Running retrieval comparison: raw vs COT ==="
HF_HOME=/scratch/fdipas/cache/huggingface \
    apptainer exec --nv \
    $CTR_APP python validate_cot.py \
        --cot-chunks data/validation_cot_500.jsonl \
        --questions data/eval_questions.jsonl \
        --embedding-model BAAI/bge-m3 \
        --k 20 \
        --output data/validation_results.json

echo "=== Done ==="
