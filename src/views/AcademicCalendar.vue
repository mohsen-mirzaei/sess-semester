<template>
  <div class="academic-calendar" dir="rtl">
    <v-app-bar color="primary" dark flat class="top-toolbar">
      <v-toolbar-title>تقویم آموزشی</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text class="navigation-button" :to="{ name: 'Home' }">
        <v-icon>mdi-arrow-right</v-icon>
        برنامه درسی
      </v-btn>
    </v-app-bar>

    <v-container class="py-6">
      <div class="calendar-heading text-center mb-6">
        <h1>تقویم آموزشی نیمسال {{ calendarData.semester.year }}-{{ calendarData.semester.term }}</h1>
        <p class="mb-0">{{ calendarData.semester.unit }}</p>
      </div>

      <v-row>
        <v-col cols="12" md="6">
          <v-card outlined>
            <v-card-title>بازه‌های ثبت نام</v-card-title>
            <v-simple-table>
              <thead><tr><th>مرحله</th><th>شروع</th><th>پایان</th></tr></thead>
              <tbody>
                <tr v-for="period in calendarData.registration_periods" :key="period.name">
                  <td>{{ period.name }}</td><td>{{ period.start }}</td><td>{{ period.end }}</td>
                </tr>
                <tr v-for="extra in calendarData.registration_extras" :key="extra.name">
                  <td>{{ extra.name }}</td><td colspan="2">{{ extra.value }}</td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card outlined>
            <v-card-title>شروع ثبت نام مرحله اول</v-card-title>
            <v-simple-table>
              <thead><tr><th>ورودی</th><th>زمان شروع</th></tr></thead>
              <tbody>
                <tr v-for="opening in calendarData.stage_one_registration_openings" :key="opening.cohort">
                  <td>{{ opening.cohort }}</td>
                  <td>{{ opening.datetime }}</td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-2">
        <v-col cols="12" md="4">
          <v-card outlined class="summary-card">
            <v-card-title><v-icon left color="primary">mdi-school</v-icon>نیمسال تحصیلی</v-card-title>
            <v-card-text>
              <div class="date-line"><span>شروع نیمسال</span><strong>{{ calendarData.semester.semester_start }}</strong></div>
              <div class="date-line"><span>پایان نیمسال</span><strong>{{ calendarData.semester.semester_end }}</strong></div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card outlined class="summary-card">
            <v-card-title><v-icon left color="primary">mdi-account-clock</v-icon>ارزیابی</v-card-title>
            <v-card-text>
              <div class="date-line"><span>شروع ارزیابی</span><strong>{{ calendarData.semester.evaluation_start }}</strong></div>
              <div class="date-line"><span>پایان ارزیابی</span><strong>{{ calendarData.semester.evaluation_end }}</strong></div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card outlined class="summary-card">
            <v-card-title><v-icon left color="primary">mdi-calendar-check</v-icon>امتحانات</v-card-title>
            <v-card-text>
              <div class="date-line"><span>شروع امتحانات</span><strong>{{ calendarData.semester.exam_start }}</strong></div>
              <div class="date-line"><span>پایان امتحانات</span><strong>{{ calendarData.semester.exam_end }}</strong></div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-2">
        <v-col cols="12" md="6">
          <v-card outlined>
            <v-card-title>مهلت ورود نمرات</v-card-title>
            <v-simple-table>
              <thead><tr><th>مقطع</th><th>تاریخ</th></tr></thead>
              <tbody>
                <tr v-for="deadline in calendarData.grade_deadlines" :key="deadline.name">
                  <td>{{ deadline.name }}</td><td>{{ deadline.date }}</td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card outlined>
            <v-card-title>جزئیات نیمسال</v-card-title>
            <v-simple-table>
              <thead><tr><th>عنوان</th><th>مقدار</th></tr></thead>
              <tbody>
                <tr v-for="detail in calendarData.semester_details" :key="detail.key">
                  <td>{{ detail.name }}</td>
                  <td>{{ detail.value || "ثبت نشده است" }}</td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-2">
        <v-col cols="12" md="6">
          <v-card outlined>
            <v-card-title>تقویم فرآیندهای دانشجویی</v-card-title>
            <v-simple-table>
              <thead><tr><th>ردیف</th><th>فرآیند</th><th>از تاریخ</th><th>تا تاریخ</th></tr></thead>
              <tbody>
                <tr v-for="process in calendarData.student_processes" :key="process.row">
                  <td>{{ process.row }}</td>
                  <td>{{ process.process }}</td>
                  <td>{{ process.start }}</td>
                  <td>{{ process.end }}</td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card outlined>
            <v-card-title>مهلت‌های مهم</v-card-title>
            <v-card-text>
              <v-list dense>
                <v-list-item><v-list-item-content>آخرین مهلت دفاع تحصیلات تکمیلی</v-list-item-content><v-list-item-icon>{{ calendarData.semester.graduate_defense_deadline }}</v-list-item-icon></v-list-item>
                <v-list-item><v-list-item-content>آخرین مهلت ثبت نام گروهی</v-list-item-content><v-list-item-icon>{{ calendarData.semester.registration_batch_end }}</v-list-item-icon></v-list-item>
                <v-list-item><v-list-item-content>حداکثر واحد ثبت نام گروهی</v-list-item-content><v-list-item-icon>{{ calendarData.semester.registration_batch_max_units }}</v-list-item-icon></v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import calendarData from "../data/semester-calendar.json";

export default {
  name: "AcademicCalendar",
  data() {
    return { calendarData };
  },
};
</script>

<style scoped>
.academic-calendar {
  min-height: 100vh;
  background: #f5f7fa;
}
.top-toolbar {
  width: 100%;
  margin: 0;
}
.navigation-button .v-icon {
  margin-left: 0.5rem !important;
}
.calendar-heading h1 {
  color: #263238;
  font-size: 1.7rem;
}
.calendar-heading p {
  color: #607d8b;
}
.summary-card {
  height: 100%;
}
.date-line {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.45rem 0;
}
.date-line + .date-line {
  border-top: 1px solid #eceff1;
}
.v-list-item__icon {
  min-width: 90px;
  justify-content: flex-start;
}
</style>
