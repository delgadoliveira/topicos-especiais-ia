import { defineAppSetup } from '@slidev/types'

export default defineAppSetup(({ app }) => {
  if (typeof window !== 'undefined') {
    const hideNav = () => {
      const selectors = [
        '.slidev-nav',
        '.slidev-controls', 
        '.slidev-navigation',
        '[class*="slidev-icon-btn"]',
      ]
      document.querySelectorAll(selectors.join(',')).forEach(el => {
        ;(el as HTMLElement).style.setProperty('display', 'none', 'important')
      })
    }
    
    // Hide on load and periodically (covers route changes)
    window.addEventListener('load', hideNav)
    setInterval(hideNav, 300)
  }
})
