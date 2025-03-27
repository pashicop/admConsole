#!/usr/bin/env bash
mkdir dispatcher
mv dispatcher-compose_1.0.0-1_amd64\ \(7\).deb dispatcher
cd dispatcher/
ar x dispatcher-compose_1.0.0-1_amd64\ \(7\).deb
zstd -d data.tar.zst
tar -xf data.tar
