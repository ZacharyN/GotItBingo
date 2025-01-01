// src/services/bingoApi.js
const getCsrfToken = () => {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
};

const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken()
};

export const createBingoCard = async () => {
    const response = await fetch('/api/bingo-cards/', {
        method: 'POST',
        headers,
        body: JSON.stringify({
            year: 2025
        })
    });
    if (!response.ok) throw new Error('Failed to create bingo card');
    return response.json();
};

export const fetchMyCards = async () => {
    const response = await fetch('/api/bingo-cards/');
    if (!response.ok) throw new Error('Failed to fetch bingo cards');
    return response.json();
};

export const updatePrediction = async (cardId, predictionData) => {
    const response = await fetch(`/api/bingo-cards/${cardId}/update_prediction/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(predictionData)
    });
    if (!response.ok) throw new Error('Failed to update prediction');
    return response.json();
};

export const finalizeCard = async (cardId) => {
    const response = await fetch(`/api/bingo-cards/${cardId}/finalize/`, {
        method: 'POST',
        headers
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to finalize card');
    }
    return response.json();
};