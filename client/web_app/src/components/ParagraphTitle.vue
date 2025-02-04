<template>
  <div class="paragraph_title title">
    <span><h4 class="tag">#</h4></span>
    <h4 class="chapter chap_one">{{ paragraphTitle }}</h4>
  </div>
</template>

<script>
export default {
  name: "ParagraphTitle",
  props: {
    paragraphTitle: {
      type: String,
      required: true,
    },
  },
};
</script>
