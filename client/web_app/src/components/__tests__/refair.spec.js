import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import refair from '../refair.vue'

describe('refair.vue', () => {
  it('should mount the component and check absence of non-existent element (EXAMPLE)', () => {
    const wrapper = mount(refair)
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('does-not-exist').exists()).toBe(false)
  })
})