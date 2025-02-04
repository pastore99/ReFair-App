<template>
  <button :type="buttonType" class="button select">
    <ion-icon name="document-attach-outline"></ion-icon>
    <label :for="labelFor" :class="labelClass" class="button__text">{{
      labelText
    }}</label>
    <i></i>
  </button>
</template>

<script>
export default {
  name: "SelectButton",
  props: {
    buttonType: {
      type: String,
      required: true,
      default: "button",
    },
    labelFor: {
      type: String,
      required: true,
    },
    labelClass: {
      type: String,
      required: true,
      default: "button__text",
    },
    labelText: {
      type: String,
      required: true,
    },
  },
};
</script>
