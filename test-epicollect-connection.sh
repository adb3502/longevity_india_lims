#!/bin/bash

# Test Epicollect5 API connection
echo "Testing Epicollect5 API connection..."

# Load configuration
if [ -f "epicollect-config.properties" ]; then
    CLIENT_ID=$(grep "epicollect.client.id" epicollect-config.properties | cut -d'=' -f2)
    CLIENT_SECRET=$(grep "epicollect.client.secret" epicollect-config.properties | cut -d'=' -f2)
    PROJECT_SLUG=$(grep "epicollect.project.slug" epicollect-config.properties | cut -d'=' -f2)
else
    echo "Error: epicollect-config.properties not found!"
    exit 1
fi

# Get access token
echo "Getting access token..."
TOKEN_RESPONSE=$(curl -s -X POST https://five.epicollect.net/api/oauth/token \
    -H "Content-Type: application/vnd.api+json" \
    -d "{\"grant_type\":\"client_credentials\",\"client_id\":\"$CLIENT_ID\",\"client_secret\":\"$CLIENT_SECRET\"}")

ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "Error: Failed to get access token"
    echo "Response: $TOKEN_RESPONSE"
    exit 1
fi

echo "Successfully obtained access token!"

# Test fetching project data
echo "Fetching project information..."
PROJECT_RESPONSE=$(curl -s -X GET "https://five.epicollect.net/api/export/project/$PROJECT_SLUG" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$PROJECT_RESPONSE" | grep -q "longevity"; then
    echo "Successfully connected to Longevity project!"
    
    # Try to fetch entries
    echo "Fetching entries..."
    ENTRIES_RESPONSE=$(curl -s -X GET "https://five.epicollect.net/api/export/entries/$PROJECT_SLUG?per_page=1" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    TOTAL_ENTRIES=$(echo $ENTRIES_RESPONSE | grep -o '"total":[0-9]*' | cut -d':' -f2)
    echo "Total entries in project: $TOTAL_ENTRIES"
else
    echo "Error: Could not fetch project data"
    echo "Response: $PROJECT_RESPONSE"
fi