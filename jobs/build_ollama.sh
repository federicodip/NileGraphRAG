#!/usr/bin/bash -l
#SBATCH --job-name=build-ollama
#SBATCH --time=01:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4
#SBATCH --partition=lowprio
#SBATCH --chdir=/home/fdipas/nilegraphrag
#SBATCH --output=logs/build-ollama-%j.out
#SBATCH --error=logs/build-ollama-%j.err
set -e

module load apptainer

echo "=== Building updated Ollama container ==="
HTTPS_PROXY=http://10.129.62.115:3128 HTTP_PROXY=http://10.129.62.115:3128 \
    APPTAINER_BINDPATH="" \
    apptainer build --ignore-fakeroot-command \
    /scratch/fdipas/graphRAG/containers/ollama_new.sif \
    docker://ollama/ollama:latest

echo "=== Swapping containers ==="
mv /scratch/fdipas/graphRAG/containers/ollama.sif /scratch/fdipas/graphRAG/containers/ollama_old.sif
mv /scratch/fdipas/graphRAG/containers/ollama_new.sif /scratch/fdipas/graphRAG/containers/ollama.sif

echo "=== Done ==="
echo "Old container backed up as ollama_old.sif"
