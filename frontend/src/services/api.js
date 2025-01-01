// src/services/api.js
export const fetchTeams = async () => {
  const response = await fetch('/api/teams/');
  if (!response.ok) {
    throw new Error('Failed to fetch teams');
  }
  return response.json();
};

export const createTeam = async (teamData) => {
  const response = await fetch('/api/teams/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(teamData),
  });
  if (!response.ok) {
    throw new Error('Failed to create team');
  }
  return response.json();
};

export const joinTeam = async (teamId) => {
  const response = await fetch(`/api/teams/${teamId}/join/`, {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error('Failed to join team');
  }
  return response.json();
};