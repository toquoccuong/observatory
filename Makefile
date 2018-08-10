all: protobuf package
.PHONY: all

protobuf:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. observatory/protobuf/observatory.proto

package:
	python setup.py sdist

