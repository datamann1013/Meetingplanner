<script setup lang="ts">
import { ref, computed, defineComponent, PropType } from 'vue';
import DashboardBox from '@/components/admin/DashboardBox.vue';
import SidebarItem from '@/components/admin/SidebarItem.vue';
import TableEntry from '@/components/shared/TableEntry.vue';
import TextInput from '@/components/shared/TextInput.vue';
import InputButton from '@/components/shared/InputButton.vue';



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
  { key: 'actions', label: '' },
];

const selectedUsers = ref<number[]>([]);
const searchQuery = ref('');
const hoveredUser = ref<number|null>(null);
const hoveredField = ref<string|null>(null);



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
        <InputButton @click="filterModal = true">Filter</InputButton>
        <InputButton color="primary" @click="openUserModal(null)">Add User</InputButton>
        <InputButton disabled>Bulk Edit</InputButton>
        <InputButton disabled>Bulk Delete</InputButton>
      </div>
      <div class="event-table-inner-bg">
        <TableEntry :columns="columns" :rows="filteredUsers">
          <template #select="{ row }">
            <input type="checkbox" :value="row.id" v-model="selectedUsers" />
          </template>
          <template #name="{ row }">
            <span class="hoverable-cell" @mouseenter="hoveredUser = row.id; hoveredField = 'name'" @mouseleave="hoveredUser = null; hoveredField = null">
              <a href="#" @click.prevent="openUserModal(row)">{{ row.name }}</a>
              <div v-if="hoveredUser === row.id && hoveredField === 'name'" class="popup-info">
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
          <template #actions="{ row }">
            <span class="kebab-menu" @click="openUserModal(row)">⋮</span>
          </template>
        </TableEntry>
      </div>
    </DashboardBox>

    <!-- Filter Modal -->
    <div v-if="filterModal" class="modal-backdrop">
      <div class="modal-container">
        <div class="modal-header">
          Filter Users
          <button class="close-btn" @click="filterModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="filter-options">
            <label><input type="radio" value="all" v-model="userFilter" /> All Users</label><br />
            <label><input type="radio" value="active" v-model="userFilter" /> Active Users</label><br />
            <label><input type="radio" value="inactive" v-model="userFilter" /> Inactive Users</label><br />
            <label><input type="radio" value="verified" v-model="userFilter" /> Verified</label><br />
            <label><input type="radio" value="pending" v-model="userFilter" /> Pending</label>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="filterModal = false">Close</button>
        </div>
      </div>
    </div>
    <!-- User Modal Placeholder -->
    <div v-if="userModal" class="modal-backdrop">
      <div class="modal-container">
        <div class="modal-header">
          Edit User: {{ selectedUser?.name || '' }}
          <button class="close-btn" @click="userModal = false">×</button>
        </div>
        <div class="modal-body">
          <div>Form fields go here (placeholder)</div>
          <StatusIndicator :status="selectedUser?.verification as StatusType" type="verification" />
        </div>
        <div class="modal-actions">
          <button @click="userModal = false">Cancel</button>
          <button>Reset Password</button>
          <button>Save Changes</button>
        </div>
      </div>
    </div>
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

