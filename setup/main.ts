import { defineAppSetup } from '@slidev/types'

export default defineAppSetup(({ app, router }) => {
  if (typeof window === 'undefined') return

  const hideNav = () => {
    // The nav bar in play.vue is: div.absolute.bottom-0.left-0 containing NavControls
    document.querySelectorAll([
      // Bottom nav bar (contains arrows, page number, overview toggle)
      'div[class*="absolute"][class*="bottom-0"][class*="left-0"]',
      // Any icon buttons (arrows, toggles)
      '.slidev-icon-btn',
      'button[title]',
      // Quick overview panel
      '[class*="quick-overview"]',
    ].join(',')).forEach(el => {
      const htmlEl = el as HTMLElement
      // Don't hide the slide content itself
      if (htmlEl.closest('#slide-content') || htmlEl.closest('.slidev-layout')) return
      htmlEl.style.setProperty('display', 'none', 'important')
    })
  }

  // Run after each navigation
  router.afterEach(() => {
    setTimeout(hideNav, 50)
    setTimeout(hideNav, 200)
  })

  // Also run periodically for initial load
  const interval = setInterval(hideNav, 300)
  setTimeout(() => clearInterval(interval), 5000)
  // Then just on route changes
  setInterval(hideNav, 2000)
})
