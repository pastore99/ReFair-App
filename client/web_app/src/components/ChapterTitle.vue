<template>
  <div class="chapter_title title">
    <span><h2 class="tag">#</h2></span>
    <h2 class="chapter chap_one">{{ chapterTitle }}</h2>
  </div>
  <hr />
</template>

<script>
export default {
  name: "ChapterTitle",
  props: {
    chapterTitle: {
      type: String,
      required: true,
    },
  },
};
</script>
