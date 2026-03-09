#!/bin/bash
# 오프니의 나노 통신 수신용 백그라운드 리스너
LOG_FILE="/tmp/swp_comms/offni_mqtt_receive.log"
echo "[$(date)] 통신선 개통 작업 시작 - 리스너 가동" > $LOG_FILE

mosquitto_sub -h localhost -p 1883 -t "swp/#" -v >> $LOG_FILE 2>&1 &
echo $! > /tmp/swp_comms/offni_listener.pid
