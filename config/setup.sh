#!/bin/bash

# Check if ENV is set and not empty
if [ -z "$BUILD_ENV" ]; then
  echo "Error: ENV variable is not set. Please set it before running the script."
  exit 1
fi

# If ENV is set, continue with the rest of the script
if [ "$BUILD_ENV" == "dev" ]; then
  echo '{"environment": "dev", "api_endpoint": "instance-12.subnet06021123.vcn06021123.oraclevcn.com:3000"}' > build-config.json
elif [ "$BUILD_ENV" == "prod" ]; then
  echo '{"environment": "prod", "api_endpoint": "instance-12.subnet06021123.vcn06021123.oraclevcn.com:80"}' > build-config.json
else
  echo "Error: Invalid ENV value. Expected 'dev' or 'prod'."
  exit 1
fi