#!/opt/homebrew/bin/bash

source ./simulator_udids.conf

for UDID in "${SIMULATOR_UDIDS[@]}"; do
  echo "Shutting down simulator with UDID: $UDID..."
  xcrun simctl shutdown "$UDID"  # Shutdown the simulator
done

echo "All simulators have been shut down safely."
