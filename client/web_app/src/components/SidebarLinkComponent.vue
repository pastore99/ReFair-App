<template>
  <span :class="customClass">
    <a :href="safeHref" target="_blank" rel="noopener noreferrer">
      <ion-icon :name="iconName"></ion-icon>
      {{ linkText }}
    </a>
  </span>
</template>

<script>
import DOMPurify from "dompurify";

export default {
  name: "SidebarLinkComponent",
  props: {
    sidebarHref: {
      type: String,
      required: true,
    },
    iconName: {
      type: String,
      required: true,
    },
    linkText: {
      type: String,
      required: true,
    },
    customClass: {
      type: String,
      required: true,
    },
  },
  computed: {
    safeHref() {
      return this.sanitizeUrl(this.sidebarHref);
    },
  },
  methods: {
    sanitizeUrl(url) {
      // Use DOMPurify to sanitize the URL
      return DOMPurify.sanitize(url);
    },
  },
};
</script>
