#!/bin/bash

echo "Verde" > color

mkdir -p colors

mv color colors/

echo "Azul" >> colors/color

cat colors/color