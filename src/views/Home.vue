<template>
  <div class="home">
    <v-dialog v-model="showAlert" width="400">
      <div class="white px-4 py-2" fluid>
        <v-card class="my-2 white">
          <div class="red white--text text-center pa-2" style="font-size: 20px">
            <h2>خطا</h2>
          </div>

          <v-list-item
            v-for="error in errorMessages"
            :key="error"
            class="grey lighten-3 pa-2"
          >
            <v-list-item-content>
              {{ error }}
            </v-list-item-content>
          </v-list-item>
        </v-card>

        <div class="text-center">
          <v-btn
            @click="showAlert = false"
            class="orange lighten-3"
            style="font-size: 1rem"
          >
            بستن
          </v-btn>
        </div>
      </div>
    </v-dialog>

    <v-card class="wholePageContent">
      <v-app-bar-nav-icon
        style="background:#eee6"
        class="outNavToggler"
        @click.stop="drawer = !drawer"
        ><v-icon x-large>mdi-chevron-left</v-icon></v-app-bar-nav-icon
      >
      <v-navigation-drawer
        fixed
        right
        v-model="drawer"
        style="width:320px"
        hide-overlay
      >
        <template v-slot:prepend>
          <v-list-item two-line>
            <v-tabs>
              <v-tab @click="filterTabClick">
                فیلتر
              </v-tab>
              <v-tab @click="selectTabClicked">
                دروس انتخاب شده
              </v-tab>

              <v-tabs-slider color="blue"></v-tabs-slider>
            </v-tabs>
            <v-app-bar-nav-icon
              style="background:#eee6"
              @click.stop="drawer = !drawer"
              ><v-icon x-large>mdi-chevron-right</v-icon></v-app-bar-nav-icon
            >
          </v-list-item>
        </template>

        <v-divider></v-divider>

        <v-list v-if="filterTabActive" dense>
          <v-list-item>
            <v-autocomplete
              solo
              label="نیمسال تحصیلی*"
              v-model="filters.semester"
              :rules="rules"
              :items="getSemesters"
              hide-no-data
              hide-details="auto"
              class="mb-3"
              hide-selected
              chips
              :search-input.sync="searchInput1"
              @change="searchInput1 = ''"
            >
              <template v-slot:selection="data">
                <v-chip v-bind="data.attrs" close @click:close="remove(data)">
                  {{ data.item }}
                </v-chip>
              </template>
            </v-autocomplete>
          </v-list-item>

          <v-list-item>
            <v-autocomplete
              solo
              label="بخش"
              v-model="filters.unit"
              :items="getUnits"
              multiple
              hide-no-data
              hide-details="auto"
              class="mb-3"
              chips
              :search-input.sync="searchInput2"
              @change="searchInput2 = ''"
            >
              <template v-slot:selection="data">
                <v-chip v-bind="data.attrs" close @click:close="remove(data)">
                  {{ data.item }}
                </v-chip>
              </template>
            </v-autocomplete>
          </v-list-item>

          <v-list-item>
            <v-autocomplete
              solo
              label="درس"
              v-model="filters.course"
              :items="getCourses"
              multiple
              hide-no-data
              hide-details="auto"
              class="mb-3"
              chips
              :search-input.sync="searchInput3"
              @change="searchInput3 = ''"
            >
              <template v-slot:selection="data">
                <v-chip v-bind="data.attrs" close @click:close="remove(data)">
                  {{ data.item }}
                </v-chip>
              </template>
            </v-autocomplete>
          </v-list-item>

          <v-list-item>
            <v-autocomplete
              solo
              label="نام استاد"
              v-model="filters.teacherName"
              :items="getTeachers"
              hide-details="auto"
              class="mb-3"
              hide-no-data
              multiple
              chips
              :search-input.sync="searchInput4"
              @change="searchInput4 = ''"
            >
              <template v-slot:selection="data">
                <v-chip v-bind="data.attrs" close @click:close="remove(data)">
                  {{ data.item }}
                </v-chip>
              </template>
            </v-autocomplete>
          </v-list-item>

          <v-list-item>
            <v-autocomplete
              solo
              label="جنسیت"
              v-model="filters.gender"
              :items="getGenders"
              multiple
              hide-no-data
              hide-details="auto"
              class="mb-3"
              chips
              :search-input.sync="searchInput7"
              @change="searchInput7 = ''"
            >
              <template v-slot:selection="data">
                <v-chip v-bind="data.attrs" close @click:close="remove(data)">
                  {{ data.item }}
                </v-chip>
              </template>
            </v-autocomplete>
          </v-list-item>

          <v-list-item>
            <v-autocomplete
              solo
              label="مکان برگزاری کلاس"
              v-model="filters.place"
              chips
              multiple
              hide-no-data
              hide-details="auto"
              class="mb-3"
              :items="getPlaces"
              :search-input.sync="searchInput6"
              @change="searchInput6 = ''"
            >
              <template v-slot:selection="data">
                <v-chip v-bind="data.attrs" close @click:close="remove(data)">
                  {{ data.item }}
                </v-chip>
              </template>
            </v-autocomplete>
          </v-list-item>

          <v-list-item>
            <v-menu
              ref="menu1"
              v-model="menuStart"
              :close-on-content-click="false"
              :nudge-right="40"
              :return-value.sync="timeStart"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="timeStart"
                  label="از ساعت"
                  prepend-icon="mdi-clock-time-four-outline"
                  readonly
                  hide-details="auto"
                  class="mb-3"
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
                <v-icon class="closeTime" @click="clearFromTime"
                  >mdi-close</v-icon
                >
              </template>
              <v-time-picker
                v-if="menuStart"
                v-model="timeStart"
                format="24hr"
                full-width
                @click:minute="$refs.menu1.save(timeStart)"
              ></v-time-picker>
            </v-menu>
          </v-list-item>

          <v-list-item>
            <v-menu
              ref="menu2"
              v-model="menuEnd"
              :close-on-content-click="false"
              :nudge-right="40"
              :return-value.sync="timeEnd"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="timeEnd"
                  label="تا ساعت"
                  prepend-icon="mdi-clock-time-four-outline"
                  readonly
                  hide-details="auto"
                  class="mb-3"
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
                <v-icon class="closeTime" @click="clearToTime"
                  >mdi-close</v-icon
                >
              </template>
              <v-time-picker
                v-if="menuEnd"
                v-model="timeEnd"
                format="24hr"
                full-width
                @click:minute="$refs.menu2.save(timeEnd)"
              ></v-time-picker>
            </v-menu>
          </v-list-item>

          <v-list-item>
            <v-btn
              width="100%"
              x-large
              class="blue white--text"
              @click="search"
            >
              <h3>جستجو</h3>
            </v-btn>
          </v-list-item>
        </v-list>

        <v-list v-if="selectedTabActive">
          <div v-if="selectedList.length">
            <v-dialog v-model="dialog" width="500">
              <v-card>
                <v-card-title class="grey lighten-2">
                  {{ dialogContent.title }}
                </v-card-title>

                <v-card-text class="mt-4">
                  <v-list>
                    <v-list-item>
                      <span style="font-weight: bold;">بخش: </span
                      >{{ dialogContent.unit }}
                    </v-list-item>

                    <v-list-item>
                      <span style="font-weight: bold;">نام استاد: </span
                      >{{ dialogContent.teacher }}
                    </v-list-item>

                    <v-list-item>
                      <span style="font-weight: bold;">گروه: </span
                      >{{ dialogContent.group }}
                    </v-list-item>

                    <v-list-item>
                      <span style="font-weight: bold;">واحد: </span
                      >{{ dialogContent.vahed }}
                    </v-list-item>

                    <v-list-item>
                      <span style="font-weight: bold;">جنسیت: </span
                      >{{ dialogContent.gender }}
                    </v-list-item>

                    <v-list-item>
                      <span style="font-weight: bold;">امتحان نهایی: </span
                      >{{
                        dialogContent.final_date +
                          " (" +
                          dialogContent.final_time +
                          ")"
                      }}
                    </v-list-item>

                    <v-list-item>
                      <span style="font-weight: bold;">زمان و مکان کلاس: </span
                      >{{ dialogContent.time_room }}
                    </v-list-item>

                    <v-list-item>
                      <span style="font-weight: bold;">ظرفیت: </span
                      >{{ dialogContent.capacity }}
                    </v-list-item>

                    <v-list-item>
                      <span style="font-weight: bold;">ساعت در هفته: </span
                      >{{ dialogContent.time_in_week }}
                    </v-list-item>
                  </v-list>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" text @click="dialog = false">
                    بستن
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <div class="text-center">
              <v-badge
                v-if="
                  interferenceClassTimeCourse.length +
                    interferenceFinalTimeCourses.length !==
                    0
                "
                :content="
                  interferenceClassTimeCourse.length +
                    interferenceFinalTimeCourses.length
                "
                :value="
                  interferenceClassTimeCourse.length +
                    interferenceFinalTimeCourses.length
                "
                color="red"
                left
                overlap
                class="my-2 text-center"
              >
                <v-btn
                  color="white"
                  class="pa-4"
                  elevation="0"
                  small
                  fab
                  dark
                  @click="showSelectedListAlert = true"
                >
                  <v-icon large color="red">
                    mdi-alert
                  </v-icon>
                </v-btn>
              </v-badge>

              <p>مجموع واحدها: {{ vahedsSum }}</p>
            </div>

            <div
              v-for="item in selectedList"
              :key="item.index"
              class="class-list-card"
            >
              <div class="class-item-name-box">
                <div>
                  <label class="group-name"> {{ item.title }} </label>
                  <!-- <label class="class-name">{{ item.group }}</label> -->
                </div>
                <label class="proff-name"> {{ item.teacher }} </label>
              </div>
              <div>
                <v-btn icon>
                  <v-icon @click="setDialogContent(item)"
                    >mdi-information</v-icon
                  >
                </v-btn>
                <v-btn icon>
                  <v-icon @click="removeFromSelected(item.id)"
                    >mdi-close-circle</v-icon
                  >
                </v-btn>
              </div>
            </div>
          </div>
        </v-list>
      </v-navigation-drawer>

      <v-dialog v-model="showSelectedListAlert" width="60rem">
        <v-card>
          <v-card-title class="pa-5 red darken-1 white--text">
            <h2>تداخل دروس</h2>
          </v-card-title>

          <v-card-text class="mt-4">
            <v-list
              v-if="interferenceClassTimeCourse.length !== 0"
              class="text-center"
            >
              <h2 class="">تداخل ساعت کلاسی</h2>
              <v-list-item
                v-for="list in interferenceClassTimeCourse"
                :key="list.id"
              >
                <v-row>
                  <v-col cols="6" class="mt-12">
                    <span style="font-weight: bold;">{{ list[0].title }}</span>
                    <br />
                    <span>{{
                      list[0].time_room.split(/\(.*?\)/).join("")
                    }}</span>
                    <br />
                    <span>{{ list[0].teacher }}</span>
                  </v-col>
                  <v-col cols="6" class="mt-12">
                    <span style="font-weight: bold;">{{ list[1].title }}</span>
                    <br />
                    <span>{{
                      list[1].time_room.split(/\(.*?\)/).join("")
                    }}</span>
                    <br />
                    <span>{{ list[1].teacher }}</span>
                  </v-col>
                  <hr />
                </v-row>
              </v-list-item>
            </v-list>

            <v-list
              v-if="interferenceFinalTimeCourses.length !== 0"
              class="text-center"
            >
              <v-divider
                v-if="interferenceClassTimeCourse.length !== 0"
              ></v-divider>
              <h2 class="mt-8">تداخل ساعت امتحان نهایی</h2>
              <v-list-item
                v-for="list in interferenceFinalTimeCourses"
                :key="list.id"
              >
                <v-row>
                  <v-col cols="6" class="mt-12">
                    <span style="font-weight: bold;">{{ list[0].title }}</span>
                    <br />
                    <span>{{ list[0].final_date }}</span>
                    <br />
                    <span>{{ list[0].final_time }}</span>
                    <br />
                    <span>{{ list[0].teacher }}</span>
                  </v-col>
                  <v-col cols="6" class="mt-12">
                    <span style="font-weight: bold;">{{ list[1].title }}</span>
                    <br />
                    <span>{{ list[1].final_date }}</span>
                    <br />
                    <span>{{ list[1].final_time }}</span>
                    <br />
                    <span>{{ list[1].teacher }}</span>
                  </v-col>
                  <hr />
                </v-row>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="showSelectedListAlert = false">
              بستن
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-snackbar v-model="snackbarAlert" timeout="-1" color="red darken-1">
        <span class="white--text">تداخل دروس!</span>
        <template v-slot:action="{ attrs }">
          <v-btn @click="showSelectedListAlert = true" color="white" text>
            جزئیات
          </v-btn>

          <v-btn
            color="white"
            text
            v-bind="attrs"
            @click="snackbarAlert = false"
          >
            بستن
          </v-btn>
        </template>
      </v-snackbar>

      <div :class="drawer ? 'exeptNav' : ''">
        <div fluid>
          <v-layout row wrap align-center class="d-none d-lg-flex d-xl-none">
            <v-flex
              align-self="center"
              class="text-center white--text ma-2"
              lg4
            >
              <h3 class="font-weight-bold">{{ updateTimeDateText }}</h3>
              <h4 class="font-weight-bold">{{ updateTimeClockText }}</h4>
            </v-flex>

            <v-flex align-self="center" lg4 class="ma-2 text-center">
              <h1 class="white--text">برنامه کلاسی نیمسال</h1>
              <h3 class="orange--text">دانشگاه شیراز</h3>
            </v-flex>

            <v-flex align-self="center" class="text-center ma-2">
              <h3 class="font-weight-bold white--text">نسخه 0.1.5</h3>
            </v-flex>
          </v-layout>

          <!-- Another layout -->
          <v-layout row wrap align-center class="d-lg-none d-xl-flex">
            <v-flex align-self="center" xs12 class="ma-1 text-center">
              <h1 class="white--text">برنامه کلاسی نیمسال</h1>
              <h3 class="orange--text">دانشگاه شیراز</h3>
            </v-flex>

            <v-flex
              align-self="center"
              class="text-center white--text mt-6"
              xs12
            >
              <h4 class="font-weight-bold">{{ updateTimeDateText }}</h4>
              <h4 class="font-weight-bold">{{ updateTimeClockText }}</h4>
            </v-flex>
          </v-layout>
        </div>

        <v-spacer class="mt-6"></v-spacer>

        <div class="white rounded-lg justify-content-center ma-2" fluid>
          <div
            v-if="results.length !== 0 && results[0] !== -1"
            :class="mobileDevice ? 'pa-3' : 'pa-6'"
          >
            <div class="results-heading">
              <h2 class="text-center my-4" id="search-h">نتایج جستجو</h2>
              <div class="results-heading-actions">
                <v-btn
                  color="primary"
                  class="calendar-export-button"
                  @click="exportCalendar"
                >
                  <v-icon left>mdi-calendar-export</v-icon>
                  خروجی تقویم
                </v-btn>
                <v-btn color="primary" @click="finalsDialogOpen = true">
                  <v-icon left>mdi-calendar-check</v-icon>
                  برنامه امتحانات
                </v-btn>
              </div>
            </div>
            <!-- Calendar -->
            <div
              v-if="selectedList.length"
              class="calenderShower light-blue darken-2"
            >
              <v-icon
                large
                @click="taggleCalender"
                color="white"
                :class="calenderOpen ? 'calnderCloseIcon' : ''"
              >
                mdi-chevron-down
              </v-icon>
              <span style="margin:auto 1rem auto 2rem" class="white--text"
                >نمایش تقویم</span
              >
              <div class="calenderHolder">
                <template>
                  <div class="theCalender" dir="ltr">
                    <v-sheet
                      v-if="calenderOpen"
                      :height="mobileDevice ? 400 : 600"
                      class="ma-2 rounded-lg"
                    >
                      <v-calendar
                        ref="calendar"
                        v-model="value"
                        :weekdays="weekday"
                        :type="type"
                        :events="events"
                        :first-interval="6"
                        :interval-count="16"
                        :event-overlap-mode="mode"
                        :event-overlap-threshold="30"
                        :event-color="getEventColor"
                        @click:event="showEvent"
                      ></v-calendar>
                      <v-menu
                        v-model="selectedOpen"
                        :close-on-content-click="false"
                        :activator="selectedElement"
                        offset-x
                      >
                        <v-card color="grey lighten-4" min-width="290px" flat>
                          <v-toolbar :color="selectedEvent.color" dark>
                            <v-toolbar-title
                              v-html="selectedEvent.name"
                            ></v-toolbar-title>
                          </v-toolbar>
                          <v-list style="background:none">
                            <v-list-item>
                              <span style="font-weight: bold;">نام استاد: </span
                              >{{ selectedEvent.teacher }}
                            </v-list-item>

                            <v-list-item>
                              <span style="font-weight: bold;">گروه: </span
                              >{{ selectedEvent.group }}
                            </v-list-item>

                            <v-list-item>
                              <span style="font-weight: bold;"
                                >امتحان نهایی: </span
                              >{{
                                selectedEvent.final_date +
                                  " (" +
                                  selectedEvent.final_time +
                                  ")"
                              }}
                            </v-list-item>
                          </v-list>
                          <v-card-actions style="flex-direction: row-reverse;">
                            <v-btn
                              text
                              color="primary"
                              @click="selectedOpen = false"
                            >
                              بستن
                            </v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-menu>

                    </v-sheet>

                  </div>
                </template>
                <v-dialog v-model="finalsDialogOpen" max-width="700">
                  <v-card>
                    <v-card-title class="grey lighten-2">
                      امتحانات نهایی دروس انتخاب شده
                    </v-card-title>
                    <v-data-table
                      :headers="finalTableHeaders"
                      :items="finalExams"
                      :items-per-page="-1"
                      hide-default-footer
                      class="finals-table"
                    >
                      <template v-slot:no-data>
                        درسی انتخاب نشده است
                      </template>
                    </v-data-table>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" text @click="exportFinalExams">
                        <v-icon left>mdi-download</v-icon>
                        خروجی متنی
                      </v-btn>
                      <v-btn
                        color="primary"
                        text
                        @click="finalsDialogOpen = false"
                      >
                        بستن
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </div>
            </div>
            <v-spacer v-if="selectedList.length" class="my-8"><hr /></v-spacer>

            <div id="app-back">
              <v-layout class="d-flex" align-center child-flex>
                <v-data-table
                  :headers="dataTableHeaders"
                  :items="results"
                  class="elevation-1 row-pointer"
                  v-model="selectedList"
                  show-select
                  hide-default-footer
                  item-key="id"
                  show-expand
                  :expanded.sync="expanded"
                  :page.sync="page"
                  :items-per-page="itemsPerPage"
                  @page-count="pageCount = $event"
                >
                  <template v-slot:expanded-item="{ headers, item }">
                    <td :colspan="headers.length">
                      <div
                        class="white rounded-lg"
                        :class="mobileDevice ? 'pa-1 mt-2 mb-2' : 'pa-3 ma-4'"
                      >
                        <v-row>
                          <h2>
                            {{ item["title"] }} | {{ item["vahed"] }} واحد
                          </h2>
                        </v-row>

                        <div class="body-font mt-8">
                          <v-row>
                            <v-col class="screen-expanded">
                              <span class="title-font-weight"
                                >نام استاد :
                              </span>
                              <span>{{ item["teacher"] }}</span>
                            </v-col>
                            <v-col class="screen-expanded">
                              <span class="title-font-weight">نام بخش : </span>
                              <span>{{ item["unit"] }}</span>
                            </v-col>

                            <v-col class="screen-expanded">
                              <span class="title-font-weight"
                                >تاریخ امتحان :
                              </span>
                              <span>{{ item["final_date"] }}</span>
                            </v-col>
                            <v-col class="screen-expanded">
                              <span class="title-font-weight"
                                >ساعت امتحان :
                              </span>
                              <span>{{ item["final_time"] }}</span>
                            </v-col>
                          </v-row>

                          <v-row>
                            <v-col class="screen-expanded">
                              <span class="title-font-weight"
                                >شماره گروه :
                              </span>
                              <span>{{ item["group"] }}</span>
                            </v-col>

                            <v-col class="screen-expanded">
                              <span class="title-font-weight">واحد : </span>
                              <span>{{ item["vahed"] }}</span>
                            </v-col>

                            <v-col class="screen-expanded">
                              <span class="title-font-weight">جنسیت : </span>
                              <span>{{ item["gender"] }}</span>
                            </v-col>

                            <v-col class="screen-expanded">
                              <span class="title-font-weight"
                                >زمان و مکان کلاس :
                              </span>
                              <span>{{ item["time_room"] }}</span>
                            </v-col>
                          </v-row>
                        </div>
                      </div>
                    </td>
                  </template>
                </v-data-table>
              </v-layout>
            </div>

            <div class="pagination-controls text-center pt-2">
              <v-pagination v-model="page" :length="pageCount"></v-pagination>
              <v-select
                v-model="itemsPerPage"
                :items="itemsPerPageOptions"
                label="تعداد"
                dense
                outlined
                hide-details
                class="items-per-page-select"
                @change="page = 1"
              ></v-select>
            </div>

            <v-row v-if="results[0] === -1" class="ma-2 pa-4" justify="center">
              <h2 class="text-center">موردی پیدا نشد</h2>
            </v-row>
          </div>
          <v-row v-else class="ma-2 pa-4" justify="center">
            <h2 class="text-center">برای نمایش نتایج، فیلتر ها را پر کنید</h2>
          </v-row>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script>
import { mapFields } from "vuex-map-fields";
import { mapGetters } from "vuex";
import { isTimeInBetween } from "../helpers/timeCalculator";
import { placeSearchHelper } from "../helpers/placeSearch";
import {
  checkClassTimeInterference,
  checkFinalTimeInterference,
} from "../helpers/timeInterference";
import { convertPersianNumToEng } from "../helpers/persianNumber_To_English";
import { toFarsiNumber } from "../helpers/english_to_persian";
import { teacherSearch } from "../helpers/teacherName";
export default {
  name: "Home",
  data() {
    return {
      timeStart: "",
      menuStart: false,

      timeEnd: "",
      menuEnd: false,

      drawer: true,
      filterTabActive: true,
      selectedTabActive: false,
      page: 1,
      pageCount: 0,
      itemsPerPage: 10,
      itemsPerPageOptions: [
        { text: "۱۰", value: 10 },
        { text: "۲۰", value: 20 },
        { text: "۵۰", value: 50 },
        { text: "۱۰۰", value: 100 },
        { text: "همه", value: -1 },
      ],

      mobileDevice: window.innerWidth < 780,

      calenderOpen: false,
      // Start calender
      type: "week",
      mode: "stack",
      modes: ["stack", "column"],
      weekday: [6, 0, 1, 2, 3, 4, 5],
      weekdays: [{ text: "Sun - Sat", value: [1, 2, 3, 4, 5, 6, 0] }],
      value: "",
      selectedEvent: {},
      selectedElement: null,
      selectedOpen: false,
      finalsDialogOpen: false,
      finalTableHeaders: [
        { text: "نام درس", value: "title" },
        { text: "تاریخ امتحان", value: "final_date" },
        { text: "ساعت امتحان", value: "final_time" },
        { text: "فاصله تا امتحان قبل", value: "study_gap" },
      ],
      events: [],
      colors: [
        "#222831",
        "#00ADB5",
        "#F08A5D",
        "#B83B5E",
        "#6A2C70",
        "#903749",
        "#3282B8",
        "#00ADB5",
        "#FF5722",
        "#086972",
        "#17B978",
      ],
      // End calender
      expanded: [],
      dialog: false,
      dialogContent: {
        title: null,
        teacher: null,
        group: null,
        gender: null,
        final_date: null,
        final_time: null,
        time_room: null,
        capacity: null,
        time_in_week: null,
        vahed: null,
      },
      vahedsSum: null,
      snackbarAlert: false,
      showSelectedListAlert: false,
      interferenceClassTimeCourse: [],
      interferenceFinalTimeCourses: [],
      searchInput1: "",
      searchInput2: "",
      searchInput3: "",
      searchInput4: "",
      searchInput6: "",
      searchInput7: "",
      showAlert: false,

      errorMessages: [],

      rules: [(value) => !!value || "نیمسال تحصیلی باید انتخاب شود."],

      dataTableHeaders: [
        { text: "درس", value: "title" },
        { text: "استاد", value: "teacher" },
        { text: "گروه", value: "group" },
        // { text: "واحد", value: "vahed" },
        { text: "زمان و مکان کلاس", value: "time_room" },
      ],

      selectedList: [],
      updateTimeDateText: "به روز شده در 11 شهریور",
      updateTimeClockText: "ساعت 21:00",
    };
  },

  created() {
    this.filters.semester = this.getFilterItems.semesters[0];
  },
  mounted() {},
  watch: {
    "filters.semester": function resetSemesterState() {
      this.filters.unit = [];
      this.filters.course = [];
      this.filters.teacherName = [];
      this.filters.place = [];
      this.filters.gender = [];
      this.results = [];
      this.selectedList = [];
      this.page = 1;
    },
    selectedList: function getEvents() {
      const convertDayName = [
        "یکشنبه",
        "دوشنبه",
        "سهشنبه",
        "چهارشنبه",
        "پنجشنبه",
        "جمعه",
        "شنبه",
      ];

      const events = [];
      const today = new Date();
      for (let i = 0; i < this.selectedList.length; i++) {
        for (
          let j = 0;
          j < this.selectedList[i]["seperated_time_and_place"].length;
          j++
        ) {
          let differenceToToDay =
            convertDayName.indexOf(
              this.selectedList[i]["seperated_time_and_place"][j].day
            ) - today.getDay();
          if (today.getDay() == 6) {
            differenceToToDay =
              differenceToToDay < 0 ? differenceToToDay + 7 : differenceToToDay;
          } else {
            differenceToToDay =
              differenceToToDay < -today.getDay() - 1
                ? differenceToToDay + 5 - today.getDay()
                : differenceToToDay > 5 - today.getDay()
                ? differenceToToDay - 7
                : differenceToToDay;
          }

          let thisDateStart = new Date();
          let thisDateEnd = new Date();
          thisDateStart.setDate(today.getDate() + differenceToToDay);
          thisDateStart.setHours(
            this.selectedList[i]["seperated_time_and_place"][j].startHour
          );
          thisDateStart.setMinutes(
            this.selectedList[i]["seperated_time_and_place"][j].startMinute
          );
          thisDateStart.setSeconds(0);
          thisDateEnd.setDate(today.getDate() + differenceToToDay);
          thisDateEnd.setHours(
            this.selectedList[i]["seperated_time_and_place"][j].endHour
          );
          thisDateEnd.setMinutes(
            this.selectedList[i]["seperated_time_and_place"][j].endMinute
          );
          thisDateEnd.setSeconds(0);
          events.push({
            name: this.selectedList[i].title,
            start: thisDateStart,
            end: thisDateEnd,
            color: this.colors[i % this.colors.length],
            timed: 1,
            teacher: this.selectedList[i].teacher,
            group: this.selectedList[i].group,
            final_time: this.selectedList[i].final_time,
            final_date: this.selectedList[i].final_date,
          });
        }
      }

      this.events = events;

      // Check time interference
      this.interferenceClassTimeCourse = [];
      this.interferenceFinalTimeCourses = [];
      for (let i = 0; i < this.selectedList.length; i++) {
        for (let j = i + 1; j < this.selectedList.length; j++) {
          let course1 = this.selectedList[i];
          let course2 = this.selectedList[j];
          if (checkClassTimeInterference(course1, course2))
            this.interferenceClassTimeCourse.push([course1, course2]);
          if (checkFinalTimeInterference(course1, course2))
            this.interferenceFinalTimeCourses.push([course1, course2]);
        }
      }
      if (
        this.interferenceClassTimeCourse.length +
          this.interferenceFinalTimeCourses.length >
        0
      ) {
        this.snackbarAlert = true;
      } else {
        this.snackbarAlert = false;
      }

      this.vahedsSum = toFarsiNumber(this.sumOfVaheds());
    },

    // End calender
  },
  methods: {
    sumOfVaheds() {
      let sum = 0;
      for (let i = 0; i < this.selectedList.length; i++) {
        let course = this.selectedList[i];
        sum += convertPersianNumToEng(course["vahed"]);
      }
      return sum;
    },
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event;
        this.selectedElement = nativeEvent.target;
        requestAnimationFrame(() =>
          requestAnimationFrame(() => (this.selectedOpen = true))
        );
      };

      if (this.selectedOpen) {
        this.selectedOpen = false;
        requestAnimationFrame(() => requestAnimationFrame(() => open()));
      } else {
        open();
      }

      nativeEvent.stopPropagation();
    },
    clearFromTime() {
      this.timeStart = "";
    },
    clearToTime() {
      this.timeEnd = "";
    },
    filterTabClick() {
      this.filterTabActive = true;
      this.selectedTabActive = false;
    },
    selectTabClicked() {
      this.filterTabActive = false;
      this.selectedTabActive = true;
    },
    taggleCalender() {
      this.calenderOpen = !this.calenderOpen;
    },
    getEventColor(event) {
      return event.color;
    },
    finalExamSortValue(exam) {
      const dateParts = (exam.final_date || "").split("/").map((part) =>
        convertPersianNumToEng(part)
      );
      const timeStart = (exam.final_time || "")
        .split("-")[0]
        .trim()
        .split(":")
        .map((part) => convertPersianNumToEng(part));

      return [
        dateParts[0] || 0,
        dateParts[1] || 0,
        dateParts[2] || 0,
        timeStart[0] || 0,
        timeStart[1] || 0,
      ];
    },
    hasFinalExamDateAndTime(exam) {
      const sortValue = this.finalExamSortValue(exam);
      const hasTime = /^\s*[0-9۰-۹]{1,2}:[0-9۰-۹]{2}\s*-\s*[0-9۰-۹]{1,2}:[0-9۰-۹]{2}\s*$/.test(
        exam.final_time || ""
      );
      return (
        sortValue[0] > 0 &&
        sortValue[1] > 0 &&
        sortValue[2] > 0 &&
        hasTime
      );
    },
    finalExamTimestamp(exam) {
      const sortValue = this.finalExamSortValue(exam);
      const year = sortValue[0];
      const month = sortValue[1];
      const day = sortValue[2];
      const daysInPreviousMonths = month <= 6 ? (month - 1) * 31 : 186 + (month - 7) * 30;

      return (
        year * 365 +
        Math.floor((year * 8 + 21) / 33) +
        daysInPreviousMonths +
        day -
        1
      ) * 1440 + sortValue[3] * 60 + sortValue[4];
    },
    formatStudyGap(minutes) {
      const days = Math.floor(minutes / 1440);
      const hours = Math.floor((minutes % 1440) / 60);
      const remainingMinutes = minutes % 60;
      const parts = [];
      if (days) parts.push(`${days} روز`);
      if (hours) parts.push(`${hours} ساعت`);
      if (remainingMinutes) parts.push(`${remainingMinutes} دقیقه`);
      return parts.length ? parts.join(" و ") : "همان زمان";
    },
    exportFinalExams() {
      const rows = [
        "نام درس\tتاریخ امتحان\tساعت امتحان\tفاصله تا امتحان قبل",
      ];
      this.finalExams.forEach((exam) => {
        rows.push(
          [exam.title, exam.final_date, exam.final_time, exam.study_gap]
            .map((value) => String(value || "").replace(/[\r\n\t]/g, " "))
            .join("\t")
        );
      });

      const blob = new Blob(["\ufeff", rows.join("\n")], {
        type: "text/plain;charset=utf-8",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "final-exams.txt";
      link.click();
      URL.revokeObjectURL(link.href);
    },
    escapeCalendarText(value) {
      return String(value || "")
        .replace(/\\/g, "\\\\")
        .replace(/;/g, "\\;")
        .replace(/,/g, "\\,")
        .replace(/[\r\n]/g, "\\n");
    },
    padCalendarNumber(value) {
      return String(value).padStart(2, "0");
    },
    formatCalendarDate(date, endOfDay = false) {
      return [
        date.getFullYear(),
        this.padCalendarNumber(date.getMonth() + 1),
        this.padCalendarNumber(date.getDate()),
      ].join("") + "T" + [
        endOfDay ? "23" : this.padCalendarNumber(date.getHours()),
        endOfDay ? "59" : this.padCalendarNumber(date.getMinutes()),
        endOfDay ? "59" : this.padCalendarNumber(date.getSeconds()),
      ].join("");
    },
    jalaliToGregorian(jalaliYear, jalaliMonth, jalaliDay) {
      let year = jalaliYear - 979;
      let dayNumber =
        365 * year +
        Math.floor(year / 33) * 8 +
        Math.floor(((year % 33) + 3) / 4);
      for (let month = 1; month < jalaliMonth; month++) {
        dayNumber += month <= 6 ? 31 : 30;
      }
      dayNumber += jalaliDay - 1;

      let gregorianDayNumber = dayNumber + 79;
      let gregorianYear = 1600 + 400 * Math.floor(gregorianDayNumber / 146097);
      gregorianDayNumber %= 146097;

      let leap = true;
      if (gregorianDayNumber >= 36525) {
        gregorianDayNumber--;
        gregorianYear += 100 * Math.floor(gregorianDayNumber / 36524);
        gregorianDayNumber %= 36524;
        if (gregorianDayNumber >= 365) gregorianDayNumber++;
        else leap = false;
      }

      gregorianYear += 4 * Math.floor(gregorianDayNumber / 1461);
      gregorianDayNumber %= 1461;
      if (gregorianDayNumber >= 366) {
        leap = false;
        gregorianDayNumber--;
        gregorianYear += Math.floor(gregorianDayNumber / 365);
        gregorianDayNumber %= 365;
      }

      const monthDays = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
      let gregorianMonth = 0;
      while (
        gregorianMonth < 12 &&
        gregorianDayNumber >= monthDays[gregorianMonth]
      ) {
        gregorianDayNumber -= monthDays[gregorianMonth];
        gregorianMonth++;
      }

      return new Date(
        gregorianYear,
        gregorianMonth,
        gregorianDayNumber + 1
      );
    },
    finalExamDate(exam) {
      const sortValue = this.finalExamSortValue(exam);
      const date = this.jalaliToGregorian(
        sortValue[0],
        sortValue[1],
        sortValue[2]
      );
      date.setHours(sortValue[3], sortValue[4], 0, 0);
      return date;
    },
    finalExamEndDate(exam) {
      const timeParts = (exam.final_time || "")
        .split("-")[1]
        .trim()
        .split(":")
        .map((part) => convertPersianNumToEng(part));
      const date = this.finalExamDate(exam);
      date.setHours(timeParts[0] || 0, timeParts[1] || 0, 0, 0);
      return date;
    },
    classStartDate(clickedDate, day, hour, minute) {
      const date = new Date(clickedDate);
      const daysUntilClass = (day - date.getDay() + 7) % 7;
      date.setDate(date.getDate() + daysUntilClass);
      date.setHours(hour, minute, 0, 0);
      return date;
    },
    exportCalendar() {
      const dayNames = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"];
      const dayNamesInPersian = [
        "یکشنبه",
        "دوشنبه",
        "سهشنبه",
        "چهارشنبه",
        "پنجشنبه",
        "جمعه",
        "شنبه",
      ];
      const clickedDate = new Date();
      const calendarEvents = [];
      const addEvent = (lines) => {
        calendarEvents.push("BEGIN:VEVENT", ...lines, "END:VEVENT");
      };

      this.selectedList.forEach((course, courseIndex) => {
        const finalDate = this.finalExamDate(course);
        course.seperated_time_and_place.forEach((classTime, classIndex) => {
          const day = dayNamesInPersian.indexOf(classTime.day);
          if (day === -1) return;

          const start = this.classStartDate(
            clickedDate,
            day,
            classTime.startHour,
            classTime.startMinute
          );
          const end = new Date(start);
          end.setHours(classTime.endHour, classTime.endMinute, 0, 0);
          const lastClassDate = new Date(finalDate);
          lastClassDate.setHours(0, 0, 0, 0);
          lastClassDate.setDate(lastClassDate.getDate() - 1);

          if (start > lastClassDate) return;
          const lines = [
            `UID:class-${course.id}-${courseIndex}-${classIndex}@sess-semester`,
            `DTSTAMP:${this.formatCalendarDate(new Date())}`,
            `DTSTART:${this.formatCalendarDate(start)}`,
            `DTEND:${this.formatCalendarDate(end)}`,
            `SUMMARY:${this.escapeCalendarText(course.title)}`,
            `LOCATION:${this.escapeCalendarText(classTime.place)}`,
            `DESCRIPTION:${this.escapeCalendarText(`استاد: ${course.teacher}`)}`,
            `RRULE:FREQ=WEEKLY;BYDAY=${dayNames[day]};UNTIL=${this.formatCalendarDate(lastClassDate, true)}`,
          ];
          addEvent(lines);
        });

        const finalStart = this.finalExamDate(course);
        const finalEnd = this.finalExamEndDate(course);
        addEvent([
          `UID:final-${course.id}-${courseIndex}@sess-semester`,
          `DTSTAMP:${this.formatCalendarDate(new Date())}`,
          `DTSTART:${this.formatCalendarDate(finalStart)}`,
          `DTEND:${this.formatCalendarDate(finalEnd)}`,
          `SUMMARY:${this.escapeCalendarText(`امتحان نهایی: ${course.title}`)}`,
          `DESCRIPTION:${this.escapeCalendarText(`گروه: ${course.group}`)}`,
        ]);
      });

      const calendar = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Sess Semester//Class Schedule//EN",
        "CALSCALE:GREGORIAN",
        "X-WR-CALNAME:برنامه کلاسی و امتحانات",
        ...calendarEvents,
        "END:VCALENDAR",
      ].join("\r\n");
      const blob = new Blob(["\ufeff", calendar], {
        type: "text/calendar;charset=utf-8",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "class-schedule-and-finals.ics";
      link.click();
      URL.revokeObjectURL(link.href);
    },
    setDialogContent(item) {
      this.dialogContent.title = item.title;
      this.dialogContent.teacher = item.teacher;
      this.dialogContent.group = item.group;
      this.dialogContent.final_date = item.final_date;
      this.dialogContent.final_time = item.final_time;
      this.dialogContent.time_room = item.time_room;
      this.dialogContent.capacity = item.capacity;
      this.dialogContent.unit = item.unit;
      this.dialogContent.time_in_week = item.time_in_week;
      this.dialogContent.vahed = item.vahed;
      this.dialogContent.gender = item.gender;
      this.dialog = true;
    },
    removeFromSelected: function(id) {
      this.selectedList = this.selectedList.filter((item) => item.id !== id);
    },
    search() {
      let flag = 0;
      this.errorMessages = [];

      if (!this.filters.semester) {
        this.errorMessages.push("نیمسال تحصیلی باید انتخاب شود");
        flag = 1;
      }
      if (
        !(
          this.filters.unit.length ||
          this.filters.course.length ||
          this.filters.teacherName.length
        )
      ) {
        this.errorMessages.push(
          "حداقل یکی از موارد بخش، درس یا نام استاد باید انتخاب شود."
        );
        flag = 1;
      }
      if (flag) {
        this.showAlert = true;
        return;
      }

      this.results = [];

      for (let unit in this.json) {
        if (
          this.filters.unit.length === 0 ||
          this.filters.unit.includes(unit)
        ) {
          for (let course in this.json[unit]) {
            if (
              this.filters.course.length === 0 ||
              this.filters.course.includes(this.json[unit][course]["title"])
            ) {
              if (
                this.filters.teacherName.length === 0 ||
                teacherSearch(
                  this.json[unit][course]["teacher"],
                  this.filters.teacherName
                )
              ) {
                if (
                  this.filters.gender.length === 0 ||
                  this.filters.gender.includes(
                    this.json[unit][course]["gender"]
                  )
                ) {
                  if (
                    this.filters.place.length === 0 ||
                    placeSearchHelper(
                      this.filters.place,
                      this.json[unit][course]
                    )
                  ) {
                    if (
                      (this.timeStart.length == 0 &&
                        this.timeEnd.length == 0) ||
                      isTimeInBetween(
                        this.timeStart,
                        this.timeEnd,
                        this.json[unit][course].seperated_time_and_place
                      )
                    ) {
                      this.results.push(this.json[unit][course]);
                    }
                  }
                }
              }
            }
          }
        }
      }
      if (this.results.length === 0) {
        this.results.push(-1);
      }
    },
    remove(item) {
      if (item.parent.label.includes("بخش")) {
        this.filters.unit.splice(this.filters.unit.indexOf(item.item), 1);
      } else if (item.parent.label.includes("درس")) {
        this.filters.course.splice(this.filters.course.indexOf(item.item), 1);
      } else if (item.parent.label.includes("نام استاد")) {
        this.filters.teacherName.splice(
          this.filters.teacherName.indexOf(item.item),
          1
        );
      } else if (item.parent.label.includes("نیمسال تحصیلی")) {
        this.filters.semester = "";
      } else if (item.parent.label.includes("مکان برگزاری کلاس")) {
        this.filters.place.splice(this.filters.place.indexOf(item.item), 1);
      } else if (item.parent.label.includes("جنسیت")) {
        this.filters.gender.splice(this.filters.place.indexOf(item.item), 1);
      }
    },
  },
  computed: {
    ...mapFields(["filters", "json", "course", "results"]),
    ...mapGetters([
      "getSemesters",
      "getUnits",
      "getCourses",
      "getTeachers",
      "getFilterItems",
      "getSele",
      "getPlaces",
      "getGenders",
    ]),
    finalExams() {
      const examsWithFinalData = this.selectedList.filter((exam) =>
        this.hasFinalExamDateAndTime(exam)
      );
      const examsWithoutFinalData = this.selectedList.filter(
        (exam) => !this.hasFinalExamDateAndTime(exam)
      );
      const sortedExams = examsWithFinalData.sort((firstExam, secondExam) => {
        const firstValue = this.finalExamSortValue(firstExam);
        const secondValue = this.finalExamSortValue(secondExam);
        for (let i = 0; i < firstValue.length; i++) {
          if (firstValue[i] !== secondValue[i]) {
            return firstValue[i] - secondValue[i];
          }
        }
        return 0;
      });

      return sortedExams.map((exam, index) => ({
        ...exam,
        study_gap:
          index === 0
            ? "اولین امتحان"
            : this.formatStudyGap(
                this.finalExamTimestamp(exam) -
                  this.finalExamTimestamp(sortedExams[index - 1])
              ),
      })).concat(
        examsWithoutFinalData.map((exam) => ({
          ...exam,
          study_gap: "تاریخ نامشخص",
        }))
      );
    },
  },
};
</script>

<style scoped>
.wholePageContent {
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
  margin-top: 0;
  padding-top: 2rem;
  padding-bottom: 2rem;
  border-radius: 0px !important;
}

.home {
  font-family: "Vazir", sans-serif;
}

.filter-color {
  background-color: #ffffff;
}

.mobile-expanded {
  font-size: small;
}
.screen-expanded {
  font-size: medium;
}
.results-heading {
  position: relative;
}
.results-heading-actions {
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  gap: 0.5rem;
}
.calendar-export-button {
  position: static;
}
.calenderShower {
  width: 100%;
  background: #ddd5;
  padding: 1rem 1rem;
  border-radius: 0.4rem;
}
@media screen and (max-width: 768px) {
  .results-heading-actions {
    position: static;
    flex-wrap: wrap;
    justify-content: center;
    margin: 0 auto 1rem;
  }
  .calenderShower {
    overflow-x: scroll;
  }
  .theCalender {
    min-width: 600px;
  }
}
.calnderCloseIcon {
  transform: rotate(-180deg);
}

#app-back {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  flex-direction: row;
}

.pagination-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}
.items-per-page-select {
  max-width: 110px;
}

#search-h {
  margin-top: 50px;
}

.class-list-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: row;
  min-width: 247px;
  width: 300px;
  padding: 7px;
  margin-top: 5px;
  margin: 7px auto;
  background-color: #c0dbe4;
  border-radius: 4px;
  font-size: 12px;
  box-shadow: 3px 3px 6px #d9d9d9, -3px -3px 6px #ffffff;
}

/* nav */
.outNavToggler {
  position: fixed;
  top: 1rem;
  right: 1rem;
}
.exeptNav {
  width: calc(100% - 320px);
  margin-right: 320px;
}

@media screen and (max-width: 768px) {
  .exeptNav {
    width: 100%;
    margin-right: auto;
  }

  .pagination-controls {
    flex-direction: column;
  }
}

.dialog-content {
  margin: 0 1rem;
}
.closeTime {
  position: absolute !important;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
}
</style>
