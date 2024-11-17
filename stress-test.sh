#!/bin/bash

# Configuración
SERVICE_URL="http://127.0.0.1:8000/ecocycle/api/sorteo"  # URL del servicio a probar
TOTAL_REQUESTS=1000             # Número total de solicitudes
SLEEP_INTERVAL=5               # Intervalo entre pruebas (en segundos)
TEST_ROUNDS=5                   # Número de rondas de prueba

echo "Iniciando prueba de estrés en $SERVICE_URL"
echo "Solicitudes totales: $TOTAL_REQUESTS, Solicitudes concurrentes: $CONCURRENT_REQUESTS"
echo "Número de rondas: $TEST_ROUNDS, Intervalo entre rondas: $SLEEP_INTERVAL segundos"
echo ""

# Función para monitorear el clúster durante la prueba
monitor_cluster() {
  echo "Estado del clúster:"
  echo "-------------------"
  sudo microk8s kubectl get pods -o wide
  sudo microk8s kubectl top pods
  echo ""
}

# Prueba de estrés
for round in $(seq 1 $TEST_ROUNDS); do
  echo "--------------------------------------"
  echo "Iniciando prueba de estrés: Ronda $round"
  echo "--------------------------------------"

  deposito_id=1
  for request in $(seq 1 $TOTAL_REQUESTS); do
    curl -s -X POST -H "Content-Type: application/json" -d "{\"deposito_id\": $deposito_id}" $SERVICE_URL > /dev/null
    # echo "\n"
  done

  # Monitorear el clúster después de cada ronda
  echo ""
  echo "Monitoreo después de la prueba: Ronda $round"
  monitor_cluster

  # Pausa antes de la siguiente ronda
  if [ $round -lt $TEST_ROUNDS ]; then
    echo "Esperando $SLEEP_INTERVAL segundos antes de la siguiente ronda..."
    sleep $SLEEP_INTERVAL
  fi
done

echo "Prueba de estrés completada."
