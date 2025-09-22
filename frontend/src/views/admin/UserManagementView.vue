<script setup lang="ts">
import { ref, computed, defineComponent, PropType } from 'vue';
import DashboardBox from '@/components/admin/DashboardBox.vue';
import SidebarItem from '@/components/admin/SidebarItem.vue';
import TableEntry from '@/components/shared/TableEntry.vue';
import TextInput from '@/components/shared/TextInput.vue';

import InputButton from '@/components/shared/InputButton.vue';
import Modal from '@/components/shared/Modal.vue';

const showFilter = ref(false);
const showBulkEdit = ref(false);
const showBulkDelete = ref(false);

function confirmBulkDelete() {
  // Implement your bulk delete logic here
  showBulkDelete.value = false;
}



const users = ref([
  { id: 1, name: 'John Doe', email: 'john@orchestra.org', phone: '555-1234', role: 'Board Member', status: 'Active', verification: 'Verified' },
  { id: 2, name: 'Jane Smith', email: 'jane@orchestra.org', phone: '555-5678', role: 'IT Member', status: 'Inactive', verification: 'Pending' },
  { id: 3, name: 'Alice Brown', email: 'alice@orchestra.org', phone: '555-8765', role: 'Normal Member', status: 'Active', verification: 'Pending' },
]);

const columns = [
  { key: 'select', label: '' },
  { key: 'name', label: 'Name' },
  { key: 'role', label: 'Role' },
  { key: 'status', label: 'Status' },
  { key: 'verification', label: 'Verification' },
];

const selectedUsers = ref<number[]>([]);
const searchQuery = ref('');




const userModal = ref(false);
const selectedUser = ref<any>(null);
function openUserModal(user: any) {
  selectedUser.value = user;
  userModal.value = true;
}

const confirmModal = ref(false);
const confirmAction = ref('');
const confirmUsers = ref<any[]>([]);
function openConfirm(action: string, users: any[]) {
  confirmAction.value = action;
  confirmUsers.value = users;
  confirmModal.value = true;
}


const filterModal = ref(false);
const userFilter = ref('all');

const filteredUsers = computed(() => {
  let filtered = users.value;
  if (userFilter.value === 'active') filtered = filtered.filter(u => u.status === 'Active');
  else if (userFilter.value === 'inactive') filtered = filtered.filter(u => u.status === 'Inactive');
  else if (userFilter.value === 'verified') filtered = filtered.filter(u => u.verification === 'Verified');
  else if (userFilter.value === 'pending') filtered = filtered.filter(u => u.verification === 'Pending');
  // Simple search filter
  return filtered.filter(u =>
    u.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    u.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Placeholder StatusIndicator component
const statusTypes = ['Active', 'Inactive', 'Verified', 'Pending'] as const;
type StatusType = typeof statusTypes[number];
const colorMap: Record<StatusType, string> = {
  Active: '#4caf50',
  Inactive: '#bdbdbd',
  Verified: '#2196f3',
  Pending: '#ff9800',
};
const StatusIndicator = defineComponent({
  name: 'StatusIndicator',
  props: {
    status: {
      type: String as PropType<StatusType>,
      default: 'Inactive',
    },
    type: String,
  },
  setup(props) {
    const dotColor = computed(() => colorMap[props.status as StatusType] || '#bdbdbd');
    return { dotColor };
  },
  template: `
    <span style="display: inline-flex; align-items: center;">
      <span :style="{ width: '8px', height: '8px', borderRadius: '50%', background: dotColor, marginRight: '6px', display: 'inline-block' }"></span>
      <span>{{ status }}</span>
    </span>
  `
});
</script>
<template>
  <div>
    <DashboardBox variant="long">
      <h3 class="event-section-title">User List</h3>
      <div class="event-list-top-bar">
        <TextInput class="event-search-input" id="user-search" label="Search users..." v-model="searchQuery" />
        <InputButton @click="showFilter = true">Filter</InputButton>
        <InputButton color="primary" @click="openUserModal(null)">Add User</InputButton>
        <InputButton @click="showBulkEdit = true">Bulk Edit</InputButton>
        <InputButton @click="showBulkDelete = true">Bulk Delete</InputButton>
      </div>
      <div class="event-table-inner-bg">
  <TableEntry :columns="columns" :rows="filteredUsers">
          <template #select="{ row }">
            <input type="checkbox" :value="row.id" v-model="selectedUsers" />
          </template>
          <template #name="{ row, hoveredRow }">
            <span class="hoverable-cell">
              <a href="#" @click.prevent="openUserModal(row)">{{ row.name }}</a>
              <div v-if="hoveredRow && hoveredRow.id === row.id" class="popup-info">
                <strong>Email:</strong> {{ row.email }}<br />
                <strong>Phone:</strong> {{ row.phone }}
              </div>
            </span>
          </template>
          <template #role="{ row }">
            <span>
              <span :class="['role-tag', row.role.replace(/\s/g, '-').toLowerCase()]">{{ row.role }}</span>
            </span>
          </template>
          <template #status="{ row }">
            <StatusIndicator :status="row.status as StatusType" />
          </template>
          <template #verification="{ row }">
            <StatusIndicator :status="row.verification as StatusType" type="verification" />
          </template>
        </TableEntry>
      </div>
    </DashboardBox>

    <Modal v-model="showFilter">
      <h3>Filter Users</h3>
      <div class="filter-options">
        <label><input type="radio" value="all" v-model="userFilter" /> All Users</label><br />
        <label><input type="radio" value="active" v-model="userFilter" /> Active Users</label><br />
        <label><input type="radio" value="inactive" v-model="userFilter" /> Inactive Users</label><br />
        <label><input type="radio" value="verified" v-model="userFilter" /> Verified</label><br />
        <label><input type="radio" value="pending" v-model="userFilter" /> Pending</label>
      </div>
      <div class="modal-actions">
        <button @click="showFilter = false">Close</button>
      </div>
    </Modal>
    <Modal v-model="showBulkEdit">
      <h3>Bulk Edit Users</h3>
      <p>Here you can add bulk edit options for users.</p>
      <div class="modal-actions">
        <button @click="showBulkEdit = false">Close</button>
      </div>
    </Modal>
    <Modal v-model="showBulkDelete">
      <h3>Bulk Delete Users</h3>
      <p>Are you sure you want to delete the selected users?</p>
      <div class="modal-actions">
        <button @click="confirmBulkDelete">Yes, Delete</button>
        <button @click="showBulkDelete = false">Cancel</button>
      </div>
    </Modal>
    <Modal v-model="userModal">
      <h3>{{ selectedUser ? `Edit User: ${selectedUser.name}` : 'Add User' }}</h3>
      <div class="modal-body">
        <div>Form fields go here (placeholder)</div>
        <StatusIndicator v-if="selectedUser" :status="selectedUser?.verification as StatusType" type="verification" />
      </div>
      <div class="modal-actions">
        <button @click="userModal = false">Cancel</button>
        <button v-if="selectedUser">Reset Password</button>
        <button>Save Changes</button>
      </div>
    </Modal>
    <!-- Confirmation Modal Placeholder -->
    <div v-if="confirmModal" class="modal-backdrop">
      <div class="modal-container">
        <div class="modal-header">
          Confirm {{ confirmAction.charAt(0).toUpperCase() + confirmAction.slice(1) }}
          <button class="close-btn" @click="confirmModal = false">×</button>
        </div>
        <div class="modal-body">
          <div>
            This will {{ confirmAction }} the following users:
            <ul>
              <li v-for="u in confirmUsers" :key="u.id">{{ u.name }} ({{ u.email }})</li>
            </ul>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="confirmModal = false">Cancel</button>
          <button>Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

