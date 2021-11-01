#!/bin/bash
cd load
docker build --network=host -t alu0101040882/load .

cd ../preprocessing
docker build --network=host -t alu0101040882/preprocessing .

cd ../training
docker build --network=host -t alu0101040882/training .

cd ../validation
docker build --network=host -t alu0101040882/validation .