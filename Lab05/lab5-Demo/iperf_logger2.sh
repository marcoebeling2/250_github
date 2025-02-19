#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./iperf_logger.sh <distance_in_meters>"
    exit 1
fi

DISTANCE=$1
LAPTOP_IP="192.168.1.225"

TCP_LOGFILE="iperf_tcp_${DISTANCE}m.csv"
UDP_LOGFILE="iperf_udp_${DISTANCE}m.csv"

# Write CSV headers (if files don't exist)
if [ ! -f "$TCP_LOGFILE" ]; then
    echo "Distance, Run1, Run2, Run3, Run4, Run5, Avg" > $TCP_LOGFILE
fi

if [ ! -f "$UDP_LOGFILE" ]; then
    echo "Distance, Run1, Run2, Run3, Run4, Run5, Avg, PacketLoss1, PacketLoss2, PacketLoss3, PacketLoss4, PacketLoss5, Avg_PacketLoss" > $UDP_LOGFILE
fi

echo "============================================="
echo " Running iPerf tests at $DISTANCE meters..."
echo "============================================="

echo "---------------------------------------------"
echo "Starting TCP Tests..."
echo "---------------------------------------------"

TCP_RESULTS=()

# Run 5 TCP Tests First
for i in {1..5}; do
    echo "🚀 TCP Run $i..."
    
    # Run TCP and extract sender's throughput
    tcp_result=$(iperf3 -c $LAPTOP_IP -t 10 | grep "sender" | awk '{print $7}')
    
    # Error handling if iPerf fails
    if [[ -z "$tcp_result" ]]; then
        echo "⚠️  Error: iPerf3 failed. Skipping this run."
        tcp_result="0"
    fi

    # Print to terminal for students
    echo "📊 TCP Sender Throughput (Run $i): $tcp_result Mbps"

    TCP_RESULTS+=("$tcp_result")
    sleep 1
done

# Compute TCP Average
TCP_AVG=$(echo "${TCP_RESULTS[@]}" | awk '{sum=0; for (i=1; i<=NF; i++) sum+=$i; print sum/NF}')

# Save TCP results in one row
echo "$DISTANCE, ${TCP_RESULTS[@]}, $TCP_AVG" >> $TCP_LOGFILE

echo "---------------------------------------------"
echo "✅ TCP Tests Completed!"
echo "TCP Results (Mbps): ${TCP_RESULTS[@]}"
echo "TCP Average: $TCP_AVG Mbps"
echo "✅ Results logged in $TCP_LOGFILE"
echo "---------------------------------------------"

sleep 2  # Small pause before UDP

echo "Starting UDP Tests..."
echo "---------------------------------------------"

UDP_RESULTS=()
PACKET_LOSS=()

# Run 5 UDP Tests Next
for i in {1..5}; do
    echo "🚀 UDP Run $i..."
    
    # Run UDP and extract sender's throughput & packet loss
    udp_output=$(iperf3 -c $LAPTOP_IP -u -b 10M -t 10)
    udp_result=$(echo "$udp_output" | grep "sender" | awk '{print $7}')
    packet_loss=$(echo "$udp_output" | grep "loss" | awk '{print $12}')
    
    # Error handling if iPerf fails
    if [[ -z "$udp_result" ]]; then
        echo "⚠️  Error: iPerf3 failed. Skipping this run."
        udp_result="0"
        packet_loss="100"
    fi

    # Print to terminal for students
    echo "📊 UDP Sender Throughput (Run $i): $udp_result Mbps"
    echo "📊 UDP Packet Loss (Run $i): $packet_loss %"

    UDP_RESULTS+=("$udp_result")
    PACKET_LOSS+=("$packet_loss")
    sleep 1
done

# Compute UDP & Packet Loss Averages
UDP_AVG=$(echo "${UDP_RESULTS[@]}" | awk '{sum=0; for (i=1; i<=NF; i++) sum+=$i; print sum/NF}')
PKT_LOSS_AVG=$(echo "${PACKET_LOSS[@]}" | awk '{sum=0; for (i=1; i<=NF; i++) sum+=$i; print sum/NF}')

# Save UDP results in one row
echo "$DISTANCE, ${UDP_RESULTS[@]}, $UDP_AVG, ${PACKET_LOSS[@]}, $PKT_LOSS_AVG" >> $UDP_LOGFILE

echo "---------------------------------------------"
echo "✅ UDP Tests Completed!"
echo "UDP Results (Mbps): ${UDP_RESULTS[@]}"
echo "UDP Average: $UDP_AVG Mbps"
echo "Packet Loss (%): ${PACKET_LOSS[@]}"
echo "Packet Loss Average: $PKT_LOSS_AVG %"
echo "✅ Results logged in $UDP_LOGFILE"
echo "---------------------------------------------"

echo "✅ Logging completed. Data saved in $TCP_LOGFILE and $UDP_LOGFILE."
