<template>
  <div class="timeline-container" ref="container">
    <div class="timeline-line"></div>
    <div class="timeline-eras">
      <div
        v-for="(era, i) in eras"
        :key="i"
        class="era-card"
        :class="{ visible: visibleCount > i }"
        :style="{ '--color': era.color, '--bg': era.bg, transitionDelay: `${i * 0.15}s` }"
      >
        <div class="era-dot"></div>
        <div class="era-year">{{ era.year }}</div>
        <div class="era-items">
          <div v-for="(item, j) in era.items" :key="j" class="era-item">{{ item }}</div>
        </div>
      </div>
    </div>
    <div class="timeline-insight" :class="{ visible: visibleCount > eras.length }">
      💡 De 1950 a 2020: modelos que <b>entendem</b>. De 2020 em diante: modelos que <b>AGEM</b>.
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, onBeforeUnmount } from 'vue'

export default defineComponent({
  name: 'TimelineAnimada',
  setup() {
    const container = ref(null)
    const visibleCount = ref(0)
    let interval = null

    const eras = [
      {
        year: '1950–1970',
        color: '#6b7280',
        bg: 'rgba(107,114,128,0.15)',
        items: ['Perceptron', 'Teste de Turing', 'ELIZA', '1º AI Winter']
      },
      {
        year: '1980–2000',
        color: '#6b7280',
        bg: 'rgba(107,114,128,0.15)',
        items: ['Expert Systems', 'Backpropagation', 'Deep Blue', 'N-grams']
      },
      {
        year: '2010–2019',
        color: '#3b82f6',
        bg: 'rgba(59,130,246,0.12)',
        items: ['Deep Learning', 'Word2Vec', 'Transformer (2017)', 'GPT-1 + BERT']
      },
      {
        year: '2020–2023',
        color: '#a855f7',
        bg: 'rgba(168,85,247,0.12)',
        items: ['GPT-3 (175B)', 'ChatGPT', 'ReAct + CoT', 'Function Calling']
      },
      {
        year: '2024–2025',
        color: '#22c55e',
        bg: 'rgba(34,197,94,0.12)',
        items: ['Claude + MCP', 'Cursor / Devin', 'Computer Use', '🤖 Era dos Agentes']
      }
    ]

    onMounted(() => {
      interval = setInterval(() => {
        if (visibleCount.value <= eras.length) {
          visibleCount.value++
        } else {
          clearInterval(interval)
        }
      }, 600)
    })

    onBeforeUnmount(() => {
      if (interval) clearInterval(interval)
    })

    return { eras, visibleCount, container }
  }
})
</script>

<style scoped>
.timeline-container {
  position: relative;
  padding: 0.5rem 0;
  overflow: hidden;
}

.timeline-line {
  position: absolute;
  top: 2.2rem;
  left: 2%;
  right: 2%;
  height: 3px;
  background: linear-gradient(90deg, #6b7280 0%, #3b82f6 40%, #a855f7 70%, #22c55e 100%);
  border-radius: 2px;
  opacity: 0.6;
}

.timeline-eras {
  display: flex;
  justify-content: space-between;
  gap: 0.4rem;
  padding-top: 2.8rem;
}

.era-card {
  flex: 1;
  background: var(--bg);
  border: 1px solid color-mix(in srgb, var(--color) 40%, transparent);
  border-radius: 10px;
  padding: 0.5rem;
  text-align: center;
  opacity: 0;
  transform: translateY(20px) scale(0.92);
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
}

.era-card.visible {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.era-dot {
  position: absolute;
  top: -1.6rem;
  left: 50%;
  transform: translateX(-50%);
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color);
  box-shadow: 0 0 8px var(--color);
}

.era-year {
  font-weight: 800;
  font-size: 0.8rem;
  color: var(--color);
  margin-bottom: 0.3rem;
}

.era-items {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.era-item {
  font-size: 0.65rem;
  opacity: 0.85;
  line-height: 1.3;
}

.timeline-insight {
  text-align: center;
  margin-top: 0.8rem;
  font-size: 0.8rem;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  transition-delay: 0.3s;
}

.timeline-insight.visible {
  opacity: 0.9;
  transform: translateY(0);
}
</style>
