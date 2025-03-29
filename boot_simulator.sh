#!/opt/homebrew/bin/bash

APP_PATH="~/Library/Developer/Xcode/DerivedData/Vitals-dhiyjmeqieicgzdptyqdjdjidjlc/Build/Products/Debug-watchsimulator/Vitals Watch App.app"
BUNDLE_ID="com.lekhnathkhanal.thesis.Vitals.watchkitapp"

declare -A SIMULATORS=(
  ["simulator1"]="C6E90AF9-B1DF-4EBF-ACF4-AF70739F93F8"
  ["simulator2"]="F1F977AA-5DA3-47B5-97BD-384804E80B60"
  ["simulator3"]="6A1C99D2-FF95-4028-BBBD-02E3BDA025A4"
  ["simulator4"]="D358A5B1-E816-4C07-BC99-FBB3A7C2BD30"
  ["simulator5"]="5DDD5A43-3C79-40BD-83B0-AC892F6D45F0"
)

# Loop through the array and install the app on each simulator
for NAME in "${!SIMULATORS[@]}"; do
    UDID="${SIMULATORS[$NAME]}"

    echo "Booting $NAME ($UDID)..."
    xcrun simctl boot "$UDID"
  

    echo "Installing on $NAME ($UDID)..."

    xcrun simctl install "$UDID" "$APP_PATH"
    echo "Launching on $NAME ($UDID)..."
xcrun simctl launch "$UDID" "$BUNDLE_ID"
done

echo "App installed and running on all simulators!"
