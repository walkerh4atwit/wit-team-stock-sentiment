#!/bin/bash

# Check if BUILD_ENV is set and not empty
if [ -z "$BUILD_ENV" ]; then
  echo "Error: BUILD_ENV variable is not set. Please set it before running the script."
  exit 1
fi

# If BUILD_ENV is set, continue with the rest of the script
if [ "$BUILD_ENV" == "dev" ]; then
  echo '{"environment": "dev", "api_endpoint": "instance-12.subnet06021123.vcn06021123.oraclevcn.com:3000"}' > ./front-end/src/resources/build-config.json
elif [ "$BUILD_ENV" == "prod" ]; then
  echo '{"environment": "prod", "api_endpoint": "instance-12.subnet06021123.vcn06021123.oraclevcn.com:80"}' > ./front-end/src/resources/build-config.json
else
  echo "Error: Invalid BUILD_ENV value. Expected 'dev' or 'prod'."
  exit 1
fi