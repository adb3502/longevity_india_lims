#!/bin/bash
#
# Redeploy Clean OpenSpecimen
#

echo "🔄 REDEPLOYING CLEAN OPENSPECIMEN"
echo "================================="

# 1. Stop Tomcat (but we can't use sudo, so we'll just remove the webapp)
echo "🛑 Removing corrupted deployment..."
rm -rf /opt/tomcat9/webapps/openspecimen/

# 2. Wait a moment for cleanup
sleep 2

# 3. Copy fresh WAR file
echo "📦 Deploying fresh WAR file..."
if [ -f "/opt/tomcat9/webapps/openspecimen.war" ]; then
    echo "✅ WAR file exists, Tomcat should auto-deploy it"
else
    echo "❌ WAR file not found"
    exit 1
fi

# 4. Touch the WAR file to trigger redeployment
touch /opt/tomcat9/webapps/openspecimen.war

echo ""
echo "================================="
echo "🎉 CLEAN REDEPLOYMENT INITIATED"
echo "================================="
echo ""
echo "⏳ Wait 30-60 seconds for Tomcat to auto-deploy"
echo "🔄 Then try: http://localhost:8082/openspecimen"
echo ""
echo "💡 If still not working:"
echo "   1. Restart Tomcat: sudo systemctl restart tomcat9"
echo "   2. Check logs: sudo tail -f /opt/tomcat9/logs/catalina.out"
echo "================================="