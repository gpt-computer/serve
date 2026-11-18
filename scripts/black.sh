#!/bin/bash
set -euo pipefail

if command -v uvx >/dev/null 2>&1; then
  BLACK=(uvx black==24.3.0)
else
  python -m pip install --quiet black==24.3.0
  BLACK=(black)
fi
arrVar=()
echo we ignore non-*.py files and files generated from protobuf
excluded_files=(
   gptc/proto/docarray_v1/pb/gptc_pb2.py
   gptc/proto/docarray_v1/pb/gptc_pb2_grpc.py
   gptc/proto/docarray_v1/pb2/gptc_pb2.py
   gptc/proto/docarray_v1/pb2/gptc_pb2_grpc.py
   gptc/proto/docarray_v2/pb/gptc_pb2.py
   gptc/proto/docarray_v2/pb/gptc_pb2_grpc.py
   gptc/proto/docarray_v2/pb2/gptc_pb2.py
   gptc/proto/docarray_v2/pb2/gptc_pb2_grpc.py
   gptc/serve/consensus/add_voter/pb/add_voter_pb2.py
   gptc/serve/consensus/add_voter/pb/add_voter_pb2_grpc.py
   gptc/serve/consensus/add_voter/pb2/add_voter_pb2.py
   gptc/serve/consensus/add_voter/pb2/add_voter_pb2_grpc.py
   docs/conf.py
)
for changed_file in ${CHANGED_FILES:-}; do
  if [[ ${changed_file} == *.py ]] && ! [[ " ${excluded_files[@]} " =~ " ${changed_file} " ]]; then
    echo checking ${changed_file}
    arrVar+=(${changed_file})
  fi
done
if (( ${#arrVar[@]} )); then
  "${BLACK[@]}" -S --check "${arrVar[@]}"
else
  echo "no files left to check"
fi
