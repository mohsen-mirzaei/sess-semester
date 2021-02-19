import { getField, updateField} from 'vuex-map-fields';
 

const state = {

    filters: {
        semester: '',
        unit: [],
        course: [],
        teacherName: [],
        time: [],
        place: [],
    },

    filtersItems: {
        semesters: ['1399-2'], 
        units: [],
        course: [],
        teachersName: [],
        times: [],
        places: [],
    },

    json: null,
}

const getters = {
    getField,
    getFilterItems : state => state.filtersItems,
    getSemesters : state => state.filtersItems.semesters,
    getUnits: state => state.filtersItems.units,
    getCourses: state => state.filtersItems.course,
    getTeachers: state => state.filtersItems.teachersName,
}

const mutations = {
    updateField,
}

const actions = {}

export default {
    state,
    getters,
    mutations,
    actions
}
