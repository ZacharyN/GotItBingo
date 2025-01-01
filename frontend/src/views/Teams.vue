<!-- src/views/Teams.vue -->
<template>
  <div class="max-w-4xl mx-auto p-4">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-4">Teams</h1>

      <!-- Create Team Form -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <h2 class="text-xl font-semibold mb-4">Create New Team</h2>
        <form @submit.prevent="handleCreateTeam" class="flex gap-4">
          <input
            v-model="newTeamName"
            type="text"
            placeholder="Team name"
            class="flex-1 p-2 border rounded"
            required
          />
          <button
            type="submit"
            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Create Team
          </button>
        </form>
      </div>

      <!-- Teams List -->
      <div class="grid gap-4">
        <div v-for="team in teams" :key="team.id"
             class="bg-white p-4 rounded-lg shadow flex justify-between items-center">
          <div>
            <h3 class="text-lg font-semibold">{{ team.name }}</h3>
            <p class="text-gray-600">Created: {{ new Date(team.created_at).toLocaleDateString() }}</p>
          </div>
          <button
            @click="handleJoinTeam(team.id)"
            class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Join Team
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchTeams, createTeam, joinTeam } from '../services/api';

const teams = ref([]);
const newTeamName = ref('');
const error = ref(null);

const loadTeams = async () => {
  try {
    teams.value = await fetchTeams();
  } catch (err) {
    error.value = 'Failed to load teams';
    console.error(err);
  }
};

const handleCreateTeam = async () => {
  try {
    await createTeam({ name: newTeamName.value });
    newTeamName.value = '';
    await loadTeams();
  } catch (err) {
    error.value = 'Failed to create team';
    console.error(err);
  }
};

const handleJoinTeam = async (teamId) => {
  try {
    await joinTeam(teamId);
    await loadTeams();
  } catch (err) {
    error.value = 'Failed to join team';
    console.error(err);
  }
};

onMounted(loadTeams);
</script>