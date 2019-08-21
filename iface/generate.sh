#!/bin/sh

mkdir -p gen
protoc --python_out=gen blog.proto
