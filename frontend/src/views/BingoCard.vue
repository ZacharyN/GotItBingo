<!-- src/views/BingoCard.vue -->
<template>
  <div class="max-w-4xl mx-auto p-4">
    <button
      v-if="!cards.length"
      @click="createNewCard"
      class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mb-8"
    >
      Create 2025 Bingo Card
    </button>

    <div v-if="currentCard" class="bg-white rounded-lg shadow p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold">2025 Predictions</h2>
        <div class="text-sm text-gray-600">
          {{ currentCard.is_finalized ? 'Finalized' : 'Draft' }}
        </div>
      </div>

      <!-- 5x5 Grid -->
      <div class="grid grid-cols-5 gap-2">
        <div
          v-for="(prediction, index) in currentCard.predictions"
          :key="prediction.id"
          class="aspect-square border p-2 relative"
          :class="{
            'bg-green-100': prediction.status === 'correct',
            'bg-red-100': prediction.status === 'incorrect'
          }"
        >
          <textarea
            v-model="prediction.prediction_text"
            class="w-full h-full resize-none text-sm"
            :placeholder="getPlaceholder(index)"
            @blur="handlePredictionUpdate(prediction)"
            :disabled="currentCard.is_finalized"
          ></textarea>

          <select
            v-model="prediction.category"
            class="absolute bottom-0 right-0 text-xs bg-transparent p-1"
            @change="handlePredictionUpdate(prediction)"
            :disabled="currentCard.is_finalized"
          >
            <option value="pending">Select...</option>
            <option value="politics">Politics</option>
            <option value="economics">Economics</option>
            <option value="society">Society</option>
            <option value="wildcard">Wild Card</option>
          </select>

          <select
            v-model="prediction.target_period"
            class="absolute bottom-0 left-0 text-xs bg-transparent p-1"
            @change="handlePredictionUpdate(prediction)"
            :disabled="currentCard.is_finalized"
          >
            <option value="Q2">Apr-Jun</option>
            <option value="Q3">Jul-Sep</option>
            <option value="Q4">Oct-Dec</option>
          </select>
        </div>
      </div>

      <!-- Validation and Progress -->
      <div class="mt-6" v-if="!currentCard.is_finalized">
        <div v-if="error" class="bg-red-100 p-4 rounded mb-4 text-red-700">
          {{ error }}
        </div>

        <div class="grid grid-cols-4 gap-4 mb-4">
          <div
            v-for="(required, category) in requiredCategories"
            :key="category"
            class="bg-gray-100 p-2 rounded"
          >
            <div class="font-bold capitalize">{{ category }}</div>
            <div class="text-sm">
              {{ categoryCounts[category] || 0 }}/{{ required }}
            </div>
          </div>
        </div>

        <button
          @click="handleFinalize"
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Saving...' : 'Finalize Card' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed,onMounted } from 'vue';
import { createBingoCard, fetchMyCards, updatePrediction, finalizeCard } from '../services/bingoApi';


const cards = ref([]);
const currentCard = ref(null);
const requiredCategories = {
  'politics': 4,
  'economics': 4,
  'society': 4,
  'wildcard': 4
};

const createNewCard = async () => {
  try {
    const newCard = await createBingoCard({
      year: 2025,
      predictions: Array(25).fill({
        prediction_text: '',
        category: 'pending',
        status: 'pending',
        target_period: 'Q2' // Default to Q2 to avoid Q1 validation errors
      })
    });
    cards.value.push(newCard);
    currentCard.value = newCard;
  } catch (error) {
    console.error('Failed to create card:', error);
  }
};

const updatePrediction = async (index) => {
  if (!currentCard.value) return;

  try {
    const prediction = currentCard.value.predictions[index];
    await updatePrediction(currentCard.value.id, {
      position: index,
      prediction_text: prediction.prediction_text,
      category: prediction.category
    });
  } catch (error) {
    console.error('Failed to update prediction:', error);
  }
};

const getPlaceholder = (index) => {
  // Helper to suggest category based on position
  const row = Math.floor(index / 5);
  if (row === 0) return 'Politics prediction...';
  if (row === 1) return 'Economics prediction...';
  if (row === 2) return 'Society prediction...';
  return 'Wild card prediction...';
};

const categoryCounts = computed(() => {
  if (!currentCard.value) return {};

  return currentCard.value.predictions.reduce((counts, prediction) => {
    counts[prediction.category] = (counts[prediction.category] || 0) + 1;
    return counts;
  }, {});
});

const validationErrors = computed(() => {
  const errors = [];

  if (!currentCard.value) return errors;

  // Check category minimums
  Object.entries(requiredCategories).forEach(([category, required]) => {
    const count = categoryCounts.value[category] || 0;
    if (count < required) {
      errors.push(`Need ${required - count} more ${category} predictions`);
    }
  });

  // Check time periods
  const q1Predictions = currentCard.value.predictions.filter(p =>
    p.target_period === 'Q1'
  );
  if (q1Predictions.length > 0) {
    errors.push('Cannot make predictions for Q1 (January-March)');
  }

  return errors;
});

const saveBingoCard = async () => {
  if (validationErrors.value.length > 0) {
    alert(validationErrors.value.join('\n'));
    return;
  }

  try {
    await updateCard(currentCard.value);
  } catch (error) {
    console.error('Failed to save card:', error);
  }
};

const error = ref(null);
const isLoading = ref(false);

const handlePredictionUpdate = async (prediction) => {
  try {
    error.value = null;
    await updatePrediction(currentCard.value.id, {
      position: prediction.position,
      prediction_text: prediction.prediction_text,
      category: prediction.category,
      target_period: prediction.target_period
    });
  } catch (err) {
    error.value = 'Failed to update prediction';
    console.error(err);
  }
};

const handleFinalize = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    await finalizeCard(currentCard.value.id);
    currentCard.value.is_finalized = true;
  } catch (err) {
    error.value = err.message;
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  try {
    const fetchedCards = await fetchMyCards();
    cards.value = fetchedCards;
    if (fetchedCards.length) {
      currentCard.value = fetchedCards[0];
    }
  } catch (error) {
    console.error('Failed to fetch cards:', error);
  }
});
</script>