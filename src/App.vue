<template>
  <v-app>
    <v-main>
        <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import { mapFields } from "vuex-map-fields";
import "./assets/css/font.css";
import { teacherNameDivider } from './helpers/teacherName';
import  { toFarsiNumber} from './helpers/english_to_persian';

const semesterFiles = require.context(
  "./data",
  false,
  /^\.\/data-\d{4}-[12]\.json$/
);


export default {
  name: "App",

  computed: {
    ...mapFields(["filtersItems", "json", "filters"]),
  },
  mounted() {
    const semesters = semesterFiles
      .keys()
      .map((file) => file.match(/data-(\d{4}-[12])\.json$/)[1])
      .sort()
      .reverse();

    this.filtersItems.semesters = semesters.length ? semesters : ["1405-1"];
    if (!this.filters.semester || !this.filtersItems.semesters.includes(this.filters.semester)) {
      this.filters.semester = this.filtersItems.semesters[0];
    }
    this.loadSemester(this.filters.semester);
  },
  watch: {
    "filters.semester": function loadSelectedSemester(semester) {
      if (semester && this.filtersItems.semesters.includes(semester)) {
        this.loadSemester(semester);
      }
    },
  },
  methods: {
    loadSemester(semester) {
      const file = `./data-${semester}.json`;
      const loadedData = semesterFiles(file);
      const semesterData = loadedData.default || loadedData;
      this.json = JSON.parse(JSON.stringify(semesterData));
      this.filtersItems.units = [];
      this.filtersItems.course = [];
      this.filtersItems.teachersName = [];
      this.filtersItems.places = [];
      this.filtersItems.genders = [];

      for (const unit in this.json) {
        for (const course in this.json[unit]) {
          const item = this.json[unit][course];
          item.id = course;
          item.teacher = teacherNameDivider(item.teacher);
          item.vahed = toFarsiNumber(item.vahed);
          item.group = toFarsiNumber(item.group);
          item.time_room = toFarsiNumber(item.time_room);
          item.unit = item.unit.slice(0, -1).replaceAll("*", "|");

          item.seperated_time_and_place.forEach((place) => {
            place.place = toFarsiNumber(place.place);
          });

          this.filtersItems.units.push(unit);
          this.filtersItems.course.push(item.title);
          item.teacher.split(" | ").forEach((teacher) => {
            this.filtersItems.teachersName.push(teacher);
          });
          this.filtersItems.genders.push(item.gender);
          item.seperated_time_and_place.forEach((place) => {
            this.filtersItems.places.push(place.place);
          });
        }
      }

      this.filtersItems.units = [...new Set(this.filtersItems.units)];
      this.filtersItems.course = [...new Set(this.filtersItems.course)];
      this.filtersItems.teachersName = [...new Set(this.filtersItems.teachersName)];
      this.filtersItems.places = [...new Set(this.filtersItems.places)];
      this.filtersItems.genders = [...new Set(this.filtersItems.genders)];
    },
  },
};
</script>

<style>

html{
  overflow: overlay!important;
  overflow-x:hidden!important;
}


#app {
  font-family: 'Vazir', sans-serif;
}

.v-chip .v-chip__content {
  white-space: pre-wrap;
  text-align: right;
}
.v-chip.v-size--default {
  min-height: 32px; 
  height: auto !important;
}
.v-data-table > .v-data-table__wrapper .v-data-table__mobile-row {
  min-height: 35px!important;
}

tr.v-data-table__mobile-table-row{
  display: block!important;

}
.v-data-table__mobile-row:nth-child(6n-5){
  display: inline-grid;
  float: left;
  background: none!important;
}
.v-data-table__mobile-row:nth-child(6n-4){
  display: inline-grid;
}

.v-data-table__mobile-row:last-child{
  padding-bottom: 1.5rem!important;
}
.v-list-item .v-list-item__title, .v-list-item .v-list-item__subtitle {
  line-height: 1.1;
  font-size:small;
  font-family: 'Vazir', sans-serif;
}
.v-tab {
  min-width: 40px!important;
  letter-spacing:0rem!important;
}
.v-slide-group__prev{
  display: none !important;
}
.v-slide-group__next{
  display: none !important;
}
.v-application .pl-1 {
  white-space: pre-wrap;
}
.v-btn {
  letter-spacing: 0!important;
}
::-webkit-scrollbar {
  width: 9px;
}

::-webkit-scrollbar-track {
  background: #e6e6e600;
}

::-webkit-scrollbar-thumb {
  background: #b0b0b099;
  border-radius: 0px;
}

::-webkit-scrollbar-thumb:hover {
  background: #b0b0b0dd;
  transition: background .5s;
}
.row {
  margin: 0px!important;
}
@media screen and (max-width: 768px) {
  ::-webkit-scrollbar {
    width: 0px;
  }
}

</style>
