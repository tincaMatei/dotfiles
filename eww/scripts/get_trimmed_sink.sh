#!/bin/bash

pamixer --get-default-sink | tail -n 1 | cut -d '"' -f4 | xargs | sed 's/\(.\{15\}\).*/\1.../'
