/**
 * Accessibility utilities for the Todo AI Chatbot
 */

/**
 * Focus trap for modal dialogs
 */
export const focusTrap = (container: HTMLElement, firstFocusable?: HTMLElement) => {
  const focusableElements = container.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as NodeListOf<HTMLElement>;

  if (focusableElements.length === 0) return;

  const firstElement = firstFocusable || focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  const handleTabKey = (e: KeyboardEvent) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      // Shift + Tab
      if (document.activeElement === firstElement) {
        lastElement.focus();
        e.preventDefault();
      }
    } else {
      // Tab
      if (document.activeElement === lastElement) {
        firstElement.focus();
        e.preventDefault();
      }
    }
  };

  container.addEventListener('keydown', handleTabKey);

  // Focus the first element
  firstElement.focus();

  return () => {
    container.removeEventListener('keydown', handleTabKey);
  };
};

/**
 * Announce a message to screen readers
 */
export const announceToScreenReader = (message: string) => {
  const announcement = document.createElement('div');
  announcement.setAttribute('aria-live', 'polite');
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;

  document.body.appendChild(announcement);

  // Remove the element after a delay to ensure it's announced
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
};

/**
 * Ensure proper ARIA attributes for dynamic content
 */
export const updateAriaAttributes = (element: HTMLElement, options: {
  busy?: boolean;
  live?: 'off' | 'polite' | 'assertive';
  label?: string;
  describedBy?: string;
}) => {
  if (options.busy !== undefined) {
    element.setAttribute('aria-busy', String(options.busy));
  }

  if (options.live) {
    element.setAttribute('aria-live', options.live);
  }

  if (options.label) {
    element.setAttribute('aria-label', options.label);
  }

  if (options.describedBy) {
    element.setAttribute('aria-describedby', options.describedBy);
  }
};

/**
 * Manage focus for dynamically added content
 */
export const manageFocusForDynamicContent = (element: HTMLElement) => {
  // If the element is interactive, focus it
  if (
    element.tagName === 'BUTTON' ||
    element.tagName === 'INPUT' ||
    element.tagName === 'SELECT' ||
    element.tagName === 'TEXTAREA' ||
    element.getAttribute('tabindex') !== null
  ) {
    element.focus();
    return;
  }

  // Otherwise, find the first focusable child
  const firstFocusable = element.querySelector(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as HTMLElement | null;

  if (firstFocusable) {
    firstFocusable.focus();
  } else {
    // If no focusable child, make the element itself focusable
    element.setAttribute('tabindex', '-1');
    element.focus();
  }
};

/**
 * Scroll to element with smooth behavior and focus management
 */
export const scrollToAndFocus = (element: HTMLElement, options?: ScrollIntoViewOptions) => {
  element.scrollIntoView({
    behavior: 'smooth',
    block: 'nearest',
    ...options
  });

  // Ensure the element is focused after scrolling
  if (element.tabIndex === -1) {
    element.focus();
  } else {
    element.focus({ preventScroll: true });
  }
};

/**
 * Check if high contrast mode is enabled
 */
export const isHighContrastMode = () => {
  if (typeof window === 'undefined') return false;

  // Check for high contrast mode using CSS media query
  return window.matchMedia('(prefers-contrast: high)').matches;
};

/**
 * Check if reduced motion is preferred
 */
export const isReducedMotionPreferred = () => {
  if (typeof window === 'undefined') return false;

  // Check for reduced motion preference
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
};