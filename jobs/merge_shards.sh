#!/usr/bin/bash
# Merge COT shard outputs into a single file.
# Run after all shard jobs complete:
#   bash jobs/merge_shards.sh

set -e
cd /home/fdipas/nilegraphrag

echo "=== Merging COT shards ==="
cat data/cot_full_shard*.jsonl > data/cot_full_merged.jsonl
TOTAL=$(wc -l < data/cot_full_merged.jsonl)
echo "Merged: $TOTAL chunks in data/cot_full_merged.jsonl"

# Check for duplicates
UNIQUE=$(cut -d'"' -f4 data/cot_full_merged.jsonl | sort -u | wc -l)
echo "Unique chunk IDs: $UNIQUE"
if [ "$TOTAL" -ne "$UNIQUE" ]; then
    echo "WARNING: $((TOTAL - UNIQUE)) duplicates found. De-duplicating..."
    python -c "
import json
seen = set()
with open('data/cot_full_merged.jsonl', encoding='utf-8') as f, \
     open('data/cot_full.jsonl', 'w', encoding='utf-8') as out:
    for line in f:
        rec = json.loads(line)
        cid = rec.get('chunk_id', '')
        if cid not in seen:
            seen.add(cid)
            out.write(line)
    print(f'De-duplicated: {len(seen)} unique chunks')
"
else
    mv data/cot_full_merged.jsonl data/cot_full.jsonl
fi

echo "=== Final: $(wc -l < data/cot_full.jsonl) chunks in data/cot_full.jsonl ==="
