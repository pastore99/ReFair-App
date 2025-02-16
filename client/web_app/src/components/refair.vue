<template>
  <div class="container">
    <div class="row">
      <div>
        <h1>ReFair App</h1>

        <!-- Chapter 1 content -->
        <div id="chapter1">
          <ChapterTitle chapterTitle="ReFair framework" />

          <div
            class="btn-toolbar mb-3 justify-content-between"
            role="toolbar"
            aria-label="Toolbar with button groups"
          >
            <!-- Upload Button-->
            <div class="file-upload">
              <input
                type="file"
                id="file"
                class="form-control"
                @change="handleStoriesUpload($event)"
              />

              <!---->

              <SelectButton
                buttonType="button"
                labelFor="file"
                labelClass="button__text"
                labelText="Select file"
              />

              <span id="file-name" class="file-name">No file selected</span>
            </div>

            <!-- Load Button-->
            <div>
              <ButtonComponent
                :clickHandler="submitFile"
                buttonType="button"
                buttonClass="button load"
                buttonStyle="margin-right: 20px"
                iconName="cloud-upload-outline"
                labelClass="button__text"
                labelText="Load"
              />

              <!-- Download all Button-->
              <ButtonComponent
                :clickHandler="reportStories"
                buttonType="button"
                buttonClass="button report"
                buttonId="report"
                iconName="cloud-download-outline"
                labelClass="button__text"
                labelText="Download all"
                :disabled="!fileLoaded"
              />
            </div>
          </div>

          <hr />
          <!-- Single US and analyze button -->
          <div class="entry_area">
            <input v-model="inputStory" placeholder="" />
            <div class="labelline">Enter an US</div>

            <ButtonComponent
              :clickHandler="analyzeSingleStory"
              buttonType="button"
              buttonClass="button analyze"
              iconName="analytics-outline"
              labelClass="button__text"
              labelText="Analyze"
              class="analyze"
            />
          </div>

          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">
                  <ParagraphTitle paragraphTitle="User Stories" />
                </th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(story, index) in paginatedStories" :key="index">
                <td>{{ story }}</td>
                <td>
                  <div>
                    <!-- Analyze Button-->
                    <ButtonComponent
                      :clickHandler="() => toggleAnalyzeStoryModal(story)"
                      buttonType="button"
                      buttonClass="button analyze"
                      iconName="analytics-outline"
                      labelClass="button__text"
                      labelText="Analyze"
                    />
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination checks -->
          <div v-if="fileLoaded" class="pagination">
            <!-- Previous Button-->
            <ButtonComponent
              :clickHandler="() => changePage(currentPage - 1)"
              buttonType="button"
              buttonClass="button previous"
              :isDisabled="currentPage === 1"
              iconName="chevron-back-outline"
              labelClass="button_text"
              labelText="Previous"
            />

            <!-- Input needed to insert a page number -->
            <input
              type="number"
              v-model.number="currentPageInput"
              @change="changePage(currentPageInput)"
              :min="1"
              :max="totalPages"
              class="input_number"
            />

            <!-- Shows the pages -->
            <span v-if="currentPage > 2">
              <label class="button_text page"> 1 </label>
            </span>
            <span v-if="currentPage > 3"
              ><label class="button_text page"> ... </label></span
            >
            <span v-if="currentPage > 1">
              <label class="button_text page">
                {{ currentPage - 1 }}
              </label></span
            >
            <span
              ><label class="button_text current page">
                {{ currentPage }}
              </label></span
            >
            <span v-if="currentPage < totalPages"
              ><label class="button_text page">
                {{ currentPage + 1 }}
              </label></span
            >
            <span v-if="currentPage < totalPages - 2">
              <label class="button_text page"> ... </label>
            </span>
            <span v-if="currentPage < totalPages - 1"
              ><label class="button_text page">
                {{ totalPages }}
              </label></span
            >

            <!-- Next Button-->
            <ButtonComponent
              :clickHandler="() => changePage(currentPage + 1)"
              buttonType="button"
              buttonClass="button next"
              :isDisabled="currentPage === totalPages"
              iconName="chevron-forward-outline"
              labelClass="button_text"
              labelText="Next"
            />
          </div>
        </div>

        <br />
        <br />
        <!-- Chapter 2 content -->
        <div class="content">
          <div id="chapter2">
            <ChapterTitle chapterTitle="ReFair in a nutshell" />

            <ParagraphTitle paragraphTitle="What is ReFair?" />

            <div class="paragraph_content">
              ReFair is an
              <strong>innovative context-aware automated framework</strong>
              designed to support fairness requirements engineering. It utilizes
              natural language processing (NLP) and word embedding techniques to
              identify sensitive features in user stories (USs), alerting
              developers early on to potential concerns.
            </div>

            <ParagraphTitle paragraphTitle="Main functionalities" />

            <div class="paragraph_content">
              ReFair is a model that consists of two main components:
              <ul>
                <li>
                  <strong> Application Domain Classification. </strong> This
                  component is responsible for classifying the most likely
                  application domain of the US among the 34 domains available in
                  the ontology;
                </li>
                <li>
                  <strong> Machine Learning Tasks Classification. </strong> This
                  is responsible for classifying the ML tasks likely to be
                  employed when imple menting the US. The problem has been
                  modeled as a multi-label classification task, as a US may be
                  operationalized using multiple ML techniques;
                </li>
                <li>
                  <strong> Sensitive Features Recommendation. </strong> The
                  application domain and ML tasks classified in the previous
                  step are finally used to recommend sensitive features. ReFair
                  exploits the base ontology to identify the sensitive features
                  connected to both the application domain and ML tasks
                  concerned with the the classified domain. The intersection of
                  those sensitive features represents the final outcome of the
                  framework. In other terms the outcome comprises the set of
                  sensitive features relevant when jointly con sidering the
                  application domain and the learning tasks.
                </li>
              </ul>
            </div>

            <ParagraphTitle paragraphTitle="Technical aspects" />

            <div class="paragraph_content">
              The framework has been designed to be conservative enough and
              identify all the potential ML tasks that may lead to unfairness.
              From a practical perspective, this choice may allow the users to
              receive a larger set of sensitive features, hence
              <strong> favoring recall over precision</strong>.
            </div>
          </div>

          <br /><br />
          <!-- Chapter 3 content -->
          <div id="chapter3">
            <ChapterTitle chapterTitle="How to use ReFair" />

            <ParagraphTitle paragraphTitle="Recommendation" />

            <div class="paragraph_content">
              To properly run the ReFair analysis, you should upload a file that
              meets specific conditions:
              <ul>
                <li>The file should be in <strong>xlsx format</strong>;</li>
                <li>
                  The spreadsheet can contain an arbitrary number of columns,
                  but at least
                  <strong>one column should be named "User Story"</strong> and
                  should contain all the User Stories you want to be analyzed.
                </li>
              </ul>
            </div>

            <ParagraphTitle paragraphTitle="Web-app functionalities" />

            <div class="paragraph_content">
              In detail:
              <ul>
                <li>
                  The <strong> Select File </strong> Button allows you to select
                  an User Stories spreadsheet from your machine;
                </li>
                <li>
                  The <strong> Load </strong> Button allows you to upload the
                  User Stories spreadsheet;
                </li>
                <li>
                  The <strong> Download all </strong> Button allows you to
                  download a structured JSON report containing the results for
                  all the User Stories analyzed by ReFair;
                </li>
                <li>
                  The
                  <strong> Analyze </strong> Button allows you to visualize the
                  ReFair analysis for a single User Story.
                </li>
                <li>
                  The <strong> Download </strong> Button (in the pop-up window)
                  allows you to download a structured JSON report containing the
                  results of the single User Story analyzed by ReFair;
                </li>
                <li>
                  The <strong> Close </strong> Button simply closes the pop-up
                  window.
                </li>
              </ul>
            </div>
          </div>

          <br /><br />
        </div>
      </div>
    </div>

    <!-- Navigation chapter -->

    <div class="sidebar">
      <p class="title_sidebar">ON THIS PAGE</p>
      <div
        class="indicator"
        :style="{ transform: `translateY(${indicatorPosition}px)` }"
      ></div>
      <ChapterButton
        btnClass="btn_chapter"
        dataChapter="chapter1"
        buttonText="ReFair framework"
        chapterId="chapter1"
        @scrollToChapter="scrollToChapter"
      />
      <ChapterButton
        btnClass="btn_chapter"
        dataChapter="chapter2"
        buttonText="ReFair in a nutshell"
        chapterId="chapter2"
        @scrollToChapter="scrollToChapter"
      />
      <ChapterButton
        btnClass="btn_chapter"
        dataChapter="chapter3"
        buttonText="How to use ReFair"
        chapterId="chapter3"
        @scrollToChapter="scrollToChapter"
      />
      <br /><br />
      <!-- ReFair model Github link -->
      <p class="title_sidebar">REFAIR REPOSITORY</p>
      <SidebarLinkComponent
        sidebarHref="https://github.com/gianwario/ReFair-App"
        iconName="logo-github"
        linkText="ReFair repository"
        customClass="sidebar_element model"
      />

      <br />
      <!-- Collaborators Github links -->
      <p class="title_sidebar">COLLABORATORS</p>
      <SidebarLinkComponent
        sidebarHref="https://github.com/DG266"
        iconName="logo-github"
        linkText="Daniele Galloppo"
        customClass="sidebar_element collaborators"
      />
      <SidebarLinkComponent
        sidebarHref="https://github.com/MarioPeluso"
        iconName="logo-github"
        linkText="Mario Peluso"
        customClass="sidebar_element collaborators"
      />
      <SidebarLinkComponent
        sidebarHref="https://github.com/LucoMoro"
        iconName="logo-github"
        linkText="Luca Morelli"
        customClass="sidebar_element collaborators"
      />
    </div>

    <!-- analyze Story Modal -->
    <div
      ref="analyzeStoryModal"
      class="modal fade"
      :class="{
        show: activeAnalyzeStoryModal,
        'd-block': activeAnalyzeStoryModal,
      }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <ParagraphTitle
              paragraphTitle="Story Details"
              style="margin-left: 15px"
            />
            <div>
              <!-- Close Button-->
              <ButtonComponent
                buttonType="button"
                buttonClass="button close"
                :clickHandler="closeAnalyzeStoryModal"
                buttonStyle="margin-right: 10px"
                iconName="close-circle-outline"
                labelClass="button__text"
                labelText="Close"
              />
            </div>
          </div>
          <div class="modal-body">
            <p class="pt-3 mx-4"><strong>User Story: </strong> {{ story }}</p>
            <p class="pt-3 mx-4">
              <strong>Story Domain: </strong> {{ story_domain }}
            </p>
            <div class="pt-3 mx-4">
              <strong>Story Tasks</strong>
              <hr />
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th scope="col"><strong>Task</strong></th>
                    <th scope="col"><strong>Sensitive Features</strong></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(features, task) in story_tasks" :key="task">
                    <td>{{ task }}</td>
                    <td>
                      {{ features.toString().replaceAll(",", " - ") }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div
              v-if="
                series[0]['data'].length != null &&
                series[0]['data'].length > 0 != []
              "
              class="pt-3 mx-4"
            >
              <apexchart
                width="1000"
                type="bar"
                :options="options"
                :series="series"
                style="color: #212223; background-color: white"
              ></apexchart>
            </div>
            <div v-else class="pt-3 mx-4">No sensitive features suggested</div>
          </div>
          <div class="modal-footer">
            <ButtonComponent
              :clickHandler="showRatingModal"
              buttonType="button"
              buttonClass="button rating"
              iconName="star-outline"
              labelClass="button__text"
              labelText="Valuta"
            />

            <ButtonComponent
              buttonType="button"
              buttonClass="button report"
              buttonId="report"
              :clickHandler="reportStory"
              iconName="cloud-download-outline"
              labelClass="button__text"
              labelText="Download"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAnalyzeStoryModal" class="modal-backdrop fade show"></div>

    <!-- Modal per il Rating -->
    <div
      v-if="activeRatingModal"
      class="modal-backdrop fade show"
      @click="closeRatingModal"
    ></div>
    <div
      v-if="activeRatingModal"
      class="modal"
      tabindex="-1"
      role="dialog"
      style="display: block;"
    >
      <div class="modal-dialog modal-sm" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Rate this Story</h5>
            <button
              type="button"
              class="btn-close"
              aria-label="Close"
              @click="closeRatingModal"
            ></button>
          </div>
          <div class="modal-body text-center">
            <!-- Rating per Domain Identification -->
            <div class="rating-section">
              <p class="rating-label">How accurate is the domain identification?</p>
              <div class="rating-container">
                <span
                  v-for="star in 5"
                  :key="'domain-' + star"
                  class="rating-star"
                  :class="{ 'selected-star': ratingDomain >= star }"
                  @click="setRating('domain', star)"
                >
                  ★
                </span>
              </div>
              <p class="mt-1">You selected: {{ ratingDomain }} star(s)</p>
            </div>

            <!-- Rating per Task Identification -->
            <div class="rating-section">
              <p class="rating-label">How accurate is the task identification?</p>
              <div class="rating-container">
                <span
                  v-for="star in 5"
                  :key="'task-' + star"
                  class="rating-star"
                  :class="{ 'selected-star': ratingTask >= star }"
                  @click="setRating('task', star)"
                >
                  ★
                </span>
              </div>
              <p class="mt-1">You selected: {{ ratingTask }} star(s)</p>
            </div>
          </div>
          <div class="modal-footer">
            <ButtonComponent
              :clickHandler="submitRating"
              buttonType="button"
              buttonClass="button submit-rating"
              iconName="send-outline"
              labelClass="button__text"
              labelText="Submit Rating"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import downloadjs from "downloadjs";
import VueApexCharts from "vue-apexcharts";

import ChapterButton from "./ChapterButton.vue";
import ChapterTitle from "./ChapterTitle.vue";
import ParagraphTitle from "./ParagraphTitle.vue";
import SelectButton from "./SelectButton.vue";
import ButtonComponent from "./ButtonComponent.vue";
import SidebarLinkComponent from "./SidebarLinkComponent.vue";

const server = "http://localhost:8080";

export default {
  components: {
    ChapterButton,
    ChapterTitle,
    ParagraphTitle,
    SelectButton,
    ButtonComponent,
    SidebarLinkComponent,
  },
  data() {
    return {
      activeAnalyzeStoryModal: false,
      story: "",
      story_domain: "",
      story_tasks: [],
      stories: [],
      file: "",
      inputStory: "",
      options: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          categories: [],
        },
      },
      series: [
        {
          name: "series-1",
          data: [],
        },
      ],
      activeButton: null, // New property to track the active button
      indicatorPosition: 0, // Position of the line
      currentPage: 1,
      storiesPerPage: 30, // Number of user stories per page
      fileLoaded: false, // Variable to track if a file has been loaded
      currentPageInput: 1, // Variable to track the user's input for the page number
      activeRatingModal: false, // Controlla lo stato della modal
      ratingDomain: 0,
      ratingTask: 0,
      story: "Example User Story", // Esempio di storia
    };
  },
  methods: {
    handleStoriesUpload(event) {
      this.file = event.target.files[0];
    },

    reportStories() {
      // Assicuriamoci che le storie siano nel formato corretto
      if (!this.stories || this.stories.length === 0) {
        alert("No user stories available to download.");
        return;
      }

      // Costruisco l'oggetto JSON con la struttura che il backend si aspetta
      const payload = {
        user_stories: this.stories,  // Il backend si aspetta un array di user stories
      };

      // Faccio la richiesta POST con JSON corretto
      axios
        .post(server + "/generate/report", payload, {
          headers: {
            "Content-Type": "application/json", // Assicuro che il server riceva JSON
          },
        })
        .then((res) => {
          console.log(res.data);

          // Converto la risposta in JSON e la scarico
          downloadjs(
            JSON.stringify(res.data, null, 2), // Stringify per formattare il JSON
            "report.json",
            "application/json"
          );
        })
        .catch((error) => {
          console.error("Errore nel download del report:", error);
          alert("Errore nel generare il report. Controlla la console.");
        });
    },

    reportStory() {
      let payload = {
        user_stories: [this.story]  // Il backend si aspetta un array
      };

      axios
        .post(server + "/generate/report", payload, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          console.log(res.data);
          downloadjs(
            JSON.stringify(res.data, null, 2),
            "report-" + this.story + ".json",
            "application/json"
          );
        })
        .catch((error) => {
          console.log("Errore nella generazione del report:", error);
        });
    },

    submitFile() {
      if (!this.file) {
        alert('No file loaded');
        return;
      }

      const fileExtension = this.file.name.split('.').pop().toLowerCase();
        if (fileExtension !== "xlsx") {
          alert("This type of file is not supported. Upload an xlsx file.");
          return;
        }

      let formData = new FormData();
      formData.append("stories", this.file);

      axios
        .post(server + "/storiesload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log("Response data:", res.data); // Debug: verifica la struttura della risposta

          if (res.data.error) {
            alert("Error: " + res.data.error);
            this.stories = [];
            this.fileLoaded = false;
          } else if (res.data.stories && res.data.stories.stories) {
            // Se la risposta è strutturata correttamente, estraiamo l'array di storie
            this.stories = res.data.stories.stories;
            this.currentPage = 1;
            this.fileLoaded = true;

            if (res.data.stories.warning) {
              alert(res.data.stories.warning);
            }
          } else {
            console.error("Invalid response format:", res.data);
            alert("Invalid response format received from server.");
            this.stories = []; // Evita problemi con .slice()
          }
        })
        .catch((error) => {
          console.error("Upload failed:", error);
          alert("Error uploading file. Please check the console.");
          this.stories = [];
          this.fileLoaded = false;
        });
    },

    analyzeSingleStory() {
      if (!this.inputStory.trim()) {
        alert("The User Story did not match the required format.");
        return;
      }

      this.toggleAnalyzeStoryModal(this.inputStory);
    },

    toggleAnalyzeStoryModal(story) {
      if (story) {
        this.story = story;

        axios
          .post(server + "/predict/domain", { user_story: this.story }, {
            headers: { "Content-Type": "application/json" },
          })
          .then((domainRes) => {
            this.story_domain = domainRes.data.domain;
            console.log("Dominio ottenuto:", this.story_domain);

            return axios.post(server + "/predict/tasks", {
              user_story: this.story,
              domain: this.story_domain,
            }, {
              headers: { "Content-Type": "application/json" },
            });
          })
          .then((tasksRes) => {
            console.log("Risposta tasks:", tasksRes.data);
            this.story_tasks = tasksRes.data.tasks_features;

            // Creiamo la mappa feature → numero di occorrenze nei task
            let featureCounts = {};

            Object.values(this.story_tasks).forEach(features => {
              features.forEach(feature => {
                featureCounts[feature] = (featureCounts[feature] || 0) + 1;
              });
            });

            // Convertiamo i dati in formato ApexCharts
            let data = Object.keys(featureCounts).map(feature => ({
              x: feature,
              y: featureCounts[feature],
            }));

            this.series = [{ name: "Occurrencies", data: data }];
            console.log("Dati aggiornati per il grafico:", this.series);

            this.activeAnalyzeStoryModal = true;
          })
          .catch((error) => {
            console.error("Errore nelle chiamate API:", error);
          });
      }
    },


    showRatingModal() {
      this.activeRatingModal = true;
    },

    closeRatingModal() {
      this.activeRatingModal = false;
      this.ratingDomain = 0;
      this.ratingTask = 0;
    },

    setRating(type, star) {
      if (type === "domain") {
        this.ratingDomain = star;
      } else if (type === "task") {
        this.ratingTask = star;
      }
    },

    submitRating() {
      // Controlla che entrambi i rating siano stati selezionati
      if (this.ratingDomain === 0 || this.ratingTask === 0) {
        alert("Please select a rating for both domain and task identification.");
        return;
      }

      // Costruiamo il payload per il feedback del dominio
      const domainPayload = {
        user_story: this.story,
        predicted_domain: this.story_domain,  // Assicurati che questa proprietà sia disponibile
        feedback_value: this.ratingDomain
      };

      // Costruiamo il payload per il feedback dei task
      const tasksPayload = {
        user_story: this.story,
        domain: this.story_domain,
        predicted_tasks: Object.keys(this.story_tasks),
        feedback_value: this.ratingTask
      };

      // Invio delle richieste POST in sequenza
      axios
        .post("http://127.0.0.1:8080/feedback/domain", domainPayload)
        .then((responseDomain) => {
          // Dopo che il feedback per il dominio è stato inviato con successo,
          // inviamo il feedback per i task.
          return axios.post("http://127.0.0.1:8080/feedback/tasks", tasksPayload);
        })
        .then((responseTasks) => {
          alert("Rating submitted successfully!");
          this.closeRatingModal();
        })
        .catch((error) => {
          console.error(error);
          alert("An error occurred while submitting the rating.");
        });
    },

    // Pagination
    changePage(page) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
        this.currentPageInput = page; // Updates the input of the current page
      }
    },

    // Chapters
    scrollToChapter(chapterId) {
      const button = this.$el.querySelector(`[data-chapter="${chapterId}"]`);
      this.activeButton = button; // Update the active button
      this.updateIndicator(); // Update the position of the indicator

      document.getElementById(chapterId).scrollIntoView({ behavior: "smooth" });
    },

    updateIndicator() {
      if (!this.activeButton) return;
      const buttonRect = this.activeButton.getBoundingClientRect();
      const sidebarRect = this.$el
        .querySelector(".sidebar")
        .getBoundingClientRect();
      const indicatorY = buttonRect.top - sidebarRect.top;

      this.indicatorPosition = indicatorY; // Update the position of the line
    },

    closeAnalyzeStoryModal() {
      const body = document.querySelector("body");
      this.activeAnalyzeStoryModal = !this.activeAnalyzeStoryModal;
      body.classList.remove("modal-open");
    },
  },
  computed: {
    totalPages() {
      return Math.ceil(this.stories.length / this.storiesPerPage);
    },
    paginatedStories() {
      const start = (this.currentPage - 1) * this.storiesPerPage;
      const end = start + this.storiesPerPage;
      return this.stories.slice(start, end);
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.activeButton = this.$el.querySelector(".btn_chapter"); // Initialize the first button as active
      this.updateIndicator(); // Set the initial position of the indicator
    });
  },
};

// Function needed to show the loaded file name
function handleStoriesUpload(event) {
  const fileInput = event.target;
  const fileNameElement = document.getElementById("file-name");
  const file = fileInput.files[0];

  if (file) {
    fileNameElement.textContent = file.name;
  } else {
    fileNameElement.textContent = "No file selected";
  }
}

// Assicurati che il DOM sia caricato prima di aggiungere l'evento
document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.querySelector(".form-control");
  fileInput.addEventListener("change", handleStoriesUpload);
});
</script>

<style>
.rating-section {
  margin-bottom: 20px;
}

.rating-label {
  font-weight: bold;
  margin-bottom: 5px;
}

.rating-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  font-size: 2rem;
  cursor: pointer;
}

.rating-star {
  color: #ccc;
  transition: color 0.2s;
}

.rating-star:hover,
.rating-star.selected-star {
  color: #ffca28;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}
</style>