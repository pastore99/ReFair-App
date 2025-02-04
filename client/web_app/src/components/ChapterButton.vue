<template>
  <button :class="btnClass" :data-chapter="dataChapter" @click="handleClick">
    {{ buttonText }}
  </button>
</template>

<script>
export default {
  name: "ChapterButton",
  props: {
    btnClass: {
      type: String,
      required: true,
    },
    dataChapter: {
      type: String,
      required: true,
    },
    buttonText: {
      type: String,
      required: true,
    },
    chapterId: {
      type: String,
      required: true,
    },
  },
  methods: {
    handleClick() {
      this.$emit("scrollToChapter", this.chapterId);
    },
  },
};
</script>
