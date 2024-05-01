#!/bin/bash

version=$1

if [ -z "$version" ]; then
  echo "Usage: release.sh <version>"
  exit 1
fi

mv "HumanEvalPlus-Mini-${version}.jsonl" HumanEvalPlus-Mini.jsonl
mv "HumanEvalPlus-${version}.jsonl" HumanEvalPlus.jsonl
mv "HumanEvalPlus-NoExtreme-${version}.jsonl" HumanEvalPlus-NoExtreme.jsonl
mv "HumanEvalPlus-OriginFmt-${version}.jsonl" HumanEvalPlus-OriginFmt.jsonl

gzip HumanEvalPlus.jsonl
gzip HumanEvalPlus-Mini.jsonl
gzip HumanEvalPlus-NoExtreme.jsonl
gzip HumanEvalPlus-OriginFmt.jsonl

git tag -a $version -m "HumanEval+ $version"
git push --tags
gh release create $version $(dirname $0)/*.jsonl.gz --title "HumanEval+ $version" --notes "HumanEval+ $version"
python hf_upload.py --version "$version" --overwrite
