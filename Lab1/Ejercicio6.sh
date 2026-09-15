#!/bin/bash

# Crear usuario supervisor
sudo adduser supervisor

# Agregar supervisor al grupo distribution
sudo usermod -aG distribution supervisor

# Cambiar propietario de Designed tasks
sudo chown -R supervisor:distribution "Designed tasks"

# Dar permisos completos al propietario y al grupo
sudo chmod -R 770 "Designed tasks"

# Mostrar propietario y permisos
ls -ld "Designed tasks"

# Mostrar grupos de supervisor
groups supervisor