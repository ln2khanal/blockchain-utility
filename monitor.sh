#!/bin/bash

PID=$1
LOG_FILE="system_monitor.jsontxt"

if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi


log_stats() {
    read CPU_USAGE MEM_USAGE RSS VSZ <<< $(ps -p $PID -o %cpu,%mem,rss,vsz | tail -n 1)

    RSS_MB=$((RSS / 1024))
    VSZ_MB=$((VSZ / 1024))

    THREADS=$(ps -M -p $PID | wc -l)
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    
    echo "{\"timestamp\": \"$TIMESTAMP\",\"pid\":$PID, \"cpu_percent\":$CPU_USAGE, \"memory_percent\":$MEM_USAGE, \"rss_memory_mb\":$RSS_MB,\"virtual_memory_mb\":$VSZ_MB,\"threads\":$THREADS}" >> "$LOG_FILE"
}

echo "Monitoring PID: $PID..."
echo "Logging system usage to: $LOG_FILE"
echo "" > $LOG_FILE
while true; do
    log_stats
    sleep 1
done
