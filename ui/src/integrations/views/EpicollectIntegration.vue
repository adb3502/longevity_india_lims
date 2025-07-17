<template>
  <div class="epicollect-integration">
    <div class="integration-header">
      <h2>Epicollect5 Integration</h2>
      <Button 
        label="Import Now" 
        icon="pi pi-download" 
        @click="triggerImport"
        :loading="importing"
        class="p-button-primary"
      />
    </div>

    <div class="integration-status">
      <Card>
        <template #title>
          <i class="pi pi-info-circle"></i> Integration Status
        </template>
        <template #content>
          <div class="status-grid">
            <div class="status-item">
              <label>Status:</label>
              <Tag :value="connectionStatus" :severity="getStatusSeverity()" />
            </div>
            <div class="status-item">
              <label>Last Import:</label>
              <span>{{ formatDate(status.lastImportDate) }}</span>
            </div>
            <div class="status-item">
              <label>Total Imported:</label>
              <span>{{ status.totalImported || 0 }}</span>
            </div>
            <div class="status-item">
              <label>Failed Imports:</label>
              <span>{{ status.failedImports || 0 }}</span>
            </div>
          </div>
          <div class="mt-3">
            <a :href="status.epicollectProjectUrl" target="_blank" class="epicollect-link">
              <i class="pi pi-external-link"></i> View on Epicollect5
            </a>
          </div>
        </template>
      </Card>
    </div>

    <div class="field-mappings mt-4">
      <Card>
        <template #title>
          <i class="pi pi-map"></i> Field Mappings
        </template>
        <template #content>
          <DataTable :value="fieldMappings" class="p-datatable-sm">
            <Column field="epicollectField" header="Epicollect Field"></Column>
            <Column field="liimsField" header="LIIMS Field"></Column>
            <Column field="privacyRule" header="Privacy Rule">
              <template #body="slotProps">
                <Tag 
                  :value="slotProps.data.privacyRule" 
                  :severity="getPrivacySeverity(slotProps.data.privacyRule)"
                />
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </div>

    <div class="import-log mt-4">
      <Card>
        <template #title>
          <i class="pi pi-list"></i> Recent Import Activity
        </template>
        <template #content>
          <DataTable :value="importLogs" class="p-datatable-sm" :paginator="true" :rows="10">
            <Column field="timestamp" header="Date/Time">
              <template #body="slotProps">
                {{ formatDate(slotProps.data.timestamp) }}
              </template>
            </Column>
            <Column field="action" header="Action"></Column>
            <Column field="count" header="Records"></Column>
            <Column field="status" header="Status">
              <template #body="slotProps">
                <Tag 
                  :value="slotProps.data.status" 
                  :severity="slotProps.data.status === 'success' ? 'success' : 'danger'"
                />
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </div>

    <Dialog v-model:visible="showConfigDialog" header="Configure Epicollect Integration" :modal="true">
      <div class="p-fluid">
        <div class="field">
          <label for="clientId">Client ID</label>
          <InputText id="clientId" v-model="config.clientId" />
        </div>
        <div class="field">
          <label for="clientSecret">Client Secret</label>
          <Password id="clientSecret" v-model="config.clientSecret" :feedback="false" />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" icon="pi pi-times" @click="showConfigDialog = false" class="p-button-text" />
        <Button label="Save" icon="pi pi-check" @click="saveConfig" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import Card from 'primevue/card';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import http from '@/common/services/HttpClient.js';
import alertsSvc from '@/common/services/Alerts.js';
import util from '@/common/services/Util.js';

export default {
  name: 'EpicollectIntegration',
  
  components: {
    Card,
    Button,
    DataTable,
    Column,
    Tag,
    Dialog,
    InputText,
    Password
  },

  setup() {
    const importing = ref(false);
    const connectionStatus = ref('Unknown');
    const status = ref({});
    const fieldMappings = ref([]);
    const importLogs = ref([]);
    const showConfigDialog = ref(false);
    const config = ref({
      clientId: '',
      clientSecret: ''
    });

    const loadStatus = async () => {
      try {
        const resp = await http.get('epicollect/status');
        status.value = resp.data;
        
        // Test connection
        const testResp = await http.get('epicollect/test');
        connectionStatus.value = testResp.data.status === 'success' ? 'Connected' : 'Disconnected';
      } catch (error) {
        connectionStatus.value = 'Error';
        console.error('Error loading status:', error);
      }
    };

    const loadMappings = async () => {
      try {
        const resp = await http.get('epicollect/mappings');
        const mappings = resp.data.fieldMappings || {};
        const privacy = resp.data.privacyRules || {};
        
        fieldMappings.value = Object.keys(mappings).map(key => ({
          epicollectField: key,
          liimsField: mappings[key],
          privacyRule: privacy[key] || 'RETAIN'
        }));
      } catch (error) {
        console.error('Error loading mappings:', error);
      }
    };

    const loadImportLogs = () => {
      // Mock data for now - would come from API
      importLogs.value = [
        {
          timestamp: new Date(),
          action: 'Manual Import',
          count: 0,
          status: 'pending'
        }
      ];
    };

    const triggerImport = async () => {
      importing.value = true;
      try {
        const resp = await http.post('epicollect/import');
        alertsSvc.success({
          title: 'Import Started',
          text: resp.data.message || 'Epicollect import has been triggered'
        });
        
        // Reload status after a delay
        setTimeout(() => {
          loadStatus();
          loadImportLogs();
        }, 2000);
      } catch (error) {
        alertsSvc.error({
          title: 'Import Failed',
          text: error.message || 'Failed to trigger import'
        });
      } finally {
        importing.value = false;
      }
    };

    const saveConfig = async () => {
      try {
        await http.post('epicollect/config', config.value);
        alertsSvc.success({
          title: 'Configuration Saved',
          text: 'Epicollect configuration has been updated'
        });
        showConfigDialog.value = false;
        loadStatus();
      } catch (error) {
        alertsSvc.error({
          title: 'Save Failed',
          text: error.message || 'Failed to save configuration'
        });
      }
    };

    const formatDate = (date) => {
      if (!date) return 'Never';
      return util.formatDate(date, true);
    };

    const getStatusSeverity = () => {
      switch (connectionStatus.value) {
        case 'Connected': return 'success';
        case 'Disconnected': return 'warning';
        case 'Error': return 'danger';
        default: return 'info';
      }
    };

    const getPrivacySeverity = (rule) => {
      switch (rule) {
        case 'ANONYMIZE': return 'warning';
        case 'REMOVE': return 'danger';
        case 'RETAIN': return 'success';
        default: return 'info';
      }
    };

    onMounted(() => {
      loadStatus();
      loadMappings();
      loadImportLogs();
    });

    return {
      importing,
      connectionStatus,
      status,
      fieldMappings,
      importLogs,
      showConfigDialog,
      config,
      triggerImport,
      saveConfig,
      formatDate,
      getStatusSeverity,
      getPrivacySeverity
    };
  }
};
</script>

<style scoped>
.epicollect-integration {
  padding: 1.5rem;
}

.integration-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.integration-header h2 {
  margin: 0;
  color: #2e3d54;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-item label {
  font-weight: 600;
  color: #6c757d;
}

.epicollect-link {
  color: #007bff;
  text-decoration: none;
}

.epicollect-link:hover {
  text-decoration: underline;
}

.mt-3 {
  margin-top: 1rem;
}

.mt-4 {
  margin-top: 1.5rem;
}

.p-card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.p-card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>