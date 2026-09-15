#!/bin/bash

# Crear carpetas
mkdir -p "Designed tasks/Maintenance"
mkdir -p "Designed tasks/Production Line"
mkdir -p "Designed tasks/Fixes"
mkdir -p "Designed tasks/Costs"

# Crear archivos dates con sus horarios
echo "Maintenance - Friday" > "Designed tasks/Maintenance/dates"

echo "Production line - Monday to Thursday" > "Designed tasks/Production Line/dates"

echo "Fixes - with 2 days of anticipation" > "Designed tasks/Fixes/dates"

echo "Costs - at the end of the month" > "Designed tasks/Costs/dates"

# Crear archivo Products
echo "Tuna" > "Designed tasks/Products"
echo "Peas" >> "Designed tasks/Products"
echo "Corn" >> "Designed tasks/Products"

# Mostrar estructura
tree "Designed tasks"

# Mostrar productos
echo ""
echo "Products:"
cat "Designed tasks/Products"