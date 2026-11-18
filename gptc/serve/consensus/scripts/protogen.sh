#/bin/sh

set -e

# This script is used to generate gRPC client stubs from the proto files.

GO_MODULE="jraft"
DOCARRAY_PROTO="docarray.proto"
DOCARRAY_DIR="../../docarray"
DOCARRAY_PACKAGE="$GO_MODULE/docarray"

GPTC_PROTO="gptc.proto"
GPTC_DIR="../../gptc"
GPTC_PACKAGE="$GO_MODULE/gptc-go-proto"


cd gptc/proto
if ! $(grep -q '^option go_package = ' docarray.proto);then
       awk '/package docarray;/{print; print "option go_package = \"'${DOCARRAY_PACKAGE}'\";";next}1' docarray.proto > temp.proto
       mv temp.proto docarray.proto
fi
protoc --go_out=${DOCARRAY_DIR} \
       --go_opt=paths=source_relative \
       --go_opt=M${DOCARRAY_PROTO}=${DOCARRAY_PACKAGE} \
       --go-grpc_out=${DOCARRAY_DIR} \
       --go-grpc_opt=paths=source_relative \
       --experimental_allow_proto3_optional \
       ${DOCARRAY_PROTO} 

if ! $(grep -q '^option go_package = ' gptc.proto);then
       awk '/package gptc;/{print; print "option go_package = \"'${GPTC_PACKAGE}'\";";next}1' gptc.proto > temp.proto
       mv temp.proto gptc.proto
fi
protoc --go_out=${GPTC_DIR} \
       --go_opt=paths=source_relative \
       --go_opt=M${GPTC_PROTO}=${GPTC_PACKAGE} \
       --go-grpc_out=${GPTC_DIR} \
       --go-grpc_opt=paths=source_relative \
       --experimental_allow_proto3_optional \
       ${GPTC_PROTO} 
cd -
