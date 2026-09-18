from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import json
import os
import re
import time


def arabicToPersian(text):
    obj = {"ك":"ک","دِ":"د","بِ":"ب","زِ":"ز","ذِ":"ذ","شِ":"ش","سِ":"س","ى":"ی","ي":"ی","١":"۱","٢":"۲","٣":"۳","٤":"۴","٥":"۵","٦":"۶","٧":"۷","٨":"۸","٩":"۹","٠":"۰","1":"۱","3":"۲","3":"۳","4":"۴","5":"۵","6":"۶","7":"۷","8":"۸","9":"۹","0":"۰"}
    regex = re.compile('|'.join(map(re.escape, obj)))
    return regex.sub(lambda match: obj[match.group(0)], text)

def convertIfPersianToEng(numberInString):
    difference = ord("۱")- ord("1")
    result = 0
    for i in numberInString:
        result*=10    
        if(ord(i)<256):
            result+=int(i)
            pass
        else:
            result += int(chr(ord(i)-difference))
    return result

def seperateTimeAndPlace(timeAndDate):
    # timeAndDate
    justDateAndTime = timeAndDate.replace("\n","")
    places = re.findall(r'\(.*?\)',justDateAndTime)
    justDateAndTime = justDateAndTime.replace(" ","")
    justDateAndTime = re.sub(r'\(.*?\)', " ", justDateAndTime).split(" ")[:-1]

    thsCourseDaysAndPlace = []
    for i in range(len(justDateAndTime)):
        dictOneOfCourseDays ={}
        dictOneOfCourseDays["place"] = places[i].replace("(","").replace(")","")
        seperated = justDateAndTime[i].split("-")
        dictOneOfCourseDays["day"]= seperated[0]
        seperatedTimes = seperated[1].split(":")
        dictOneOfCourseDays["startHour"] = convertIfPersianToEng(seperatedTimes[0])
        dictOneOfCourseDays["startMinute"] = convertIfPersianToEng(seperatedTimes[1])
        dictOneOfCourseDays["endHour"] = convertIfPersianToEng(seperatedTimes[2])
        dictOneOfCourseDays["endMinute"] = convertIfPersianToEng(seperatedTimes[3])
        thsCourseDaysAndPlace.append(dictOneOfCourseDays)

    return thsCourseDaysAndPlace

def get_course_details():
    global Driver
    data = dict()
    title_element = WebDriverWait(Driver, 15).until(
        EC.visibility_of_element_located((By.ID, 'edName'))
    )

    data['title'] = arabicToPersian(title_element.text)
    data['vahed'] = Driver.find_element(By.ID,  'edTotalUnit').text
    data['group'] = Driver.find_element(By.ID,  'edGroup').text
    data['teacher'] = arabicToPersian(Driver.find_element(By.ID,  'edTch').text)
    data['gender'] = arabicToPersian(Driver.find_element(By.ID,  'edSex').text)
    data['unit'] = arabicToPersian(Driver.find_element(By.ID,  'edUnit').text)
    data['time_in_week'] = arabicToPersian(Driver.find_element(By.ID,  'edTimeInWeek').text)
    data['time_room'] = arabicToPersian(Driver.find_element(By.ID,  'edTimeRoom').text)
    data['midterm_date'] = Driver.find_element(By.ID,  'edMidDate').text
    data['midterm_time'] = Driver.find_element(By.ID,  'edMidTime').text
    data['capacity'] = arabicToPersian(Driver.find_element(By.ID,  'edCapacity').text)
    data['id'] = Driver.find_element(By.ID,  'edSrl').text + '^' + data['group']
    data['final_time'] = Driver.find_element(By.ID,  'edFinalTime').text
    data['final_date'] = Driver.find_element(By.ID,  'edFinalDate').text

    try:
        splitedTime = Driver.find_element(By.ID,  'edFinalTime').text.replace(" ","").split("-")
        splitedTimeStart = splitedTime[0].split(":")
        splitedTimeEnd = splitedTime[1].split(":")
        data['final_time_split'] = {"start_hour":convertIfPersianToEng(splitedTimeStart[0]),"start_minute":convertIfPersianToEng(splitedTimeStart[1]), "end_hour":convertIfPersianToEng(splitedTimeEnd[0]),"end_minute":convertIfPersianToEng(splitedTimeEnd[1])}
    except:
        data['final_time_split'] = {"start_hour":0,"start_minute":0, "end_hour":0,"end_minute":0}

    try:
        splitedDate = Driver.find_element(By.ID,  'edFinalDate').text.split("/")
        data['final_date_split'] = {"d":convertIfPersianToEng(splitedDate[2]),"m":convertIfPersianToEng(splitedDate[1]),"y":convertIfPersianToEng(splitedDate[0])} 
    except:
        data['final_date_split'] = {"d":0,"m":0,"y":0} 

    try:
        data['seperated_time_and_place']=seperateTimeAndPlace(arabicToPersian(data['time_room']))
    except:
        data['seperated_time_and_place']={}
    return [data['id'], data]


def wait_for_schedule():
    WebDriverWait(Driver, 15).until(
        EC.presence_of_element_located((By.ID, 'edDepartment'))
    )


def wait_for_courses(class_name):
    return WebDriverWait(Driver, 15).until(
        lambda driver: driver.find_elements(By.CLASS_NAME, class_name)
    )


def click_course(course_index, class_name):
    course_locator = (
        By.XPATH,
        f"(//*[contains(concat(' ', normalize-space(@class), ' '), ' {class_name} ')])[{course_index + 1}]",
    )

    def click_live_course(driver):
        try:
            course = driver.find_element(*course_locator)
            if not course.is_enabled():
                return False
            course.click()
            return True
        except StaleElementReferenceException:
            return False

    WebDriverWait(Driver, 15).until(click_live_course)


def get_course_counts():
    try:
        return WebDriverWait(Driver, 15).until(
            lambda driver: (
                len(driver.find_elements(By.CLASS_NAME, 'listOdd')),
                len(driver.find_elements(By.CLASS_NAME, 'listEven')),
            ) if (
                driver.find_elements(By.CLASS_NAME, 'listOdd') or
                driver.find_elements(By.CLASS_NAME, 'listEven')
            ) else False
        )
    except TimeoutException:
        return 0, 0


def wait_for_department_results(previous_course):
    if previous_course is None:
        return

    WebDriverWait(Driver, 15).until(
        EC.staleness_of(previous_course)
    )


def recover_to_schedule():
    try:
        wait_for_schedule()
    except TimeoutException:
        Driver.back()
        wait_for_schedule()


def scrape_course(course_index, current_parity, datas):
    class_name = 'listOdd' if current_parity == 'odd' else 'listEven'
    last_error = None

    for attempt in range(1, 4):
        try:
            courses = wait_for_courses(class_name)
            if course_index >= len(courses):
                return False

            click_course(course_index, class_name)
            serial, data = get_course_details()
            datas[serial] = data
            Driver.back()
            wait_for_schedule()
            return True
        except Exception as error:
            last_error = error
            screenshot = (
                f'crawler-error-{course_index}-{current_parity}-attempt-{attempt}.png'
            )
            print(f'Course attempt {attempt}/3 failed: {error}')
            print(f'URL: {Driver.current_url}')
            print(f'Title: {Driver.title}')
            Driver.save_screenshot(screenshot)
            print(f'Screenshot saved to {screenshot}')

            if attempt < 3:
                recover_to_schedule()

    raise RuntimeError(
        f'Could not load course {course_index} ({current_parity}) after 3 attempts'
    ) from last_error
    

def save_progress(progress_file, all_data, department_position, course_index, parity):
    progress = {
        "all_data": all_data,
        "department_position": department_position,
        "course_index": course_index,
        "parity": parity,
    }
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False)


def load_progress(progress_file):
    with open(progress_file, 'r', encoding='utf-8') as f:
        progress = json.load(f)
    return (
        progress.get("all_data", {}),
        progress.get("department_position", 0),
        progress.get("course_index", 0),
        progress.get("parity", "odd"),
    )


output_file = input('Enter the output JSON file name [data.json]: ').strip() or 'data.json'
progress_file = output_file + '.progress.json'
all_data = {}
department_position = 0
course_index = 0
parity = "odd"

if os.path.exists(progress_file):
    answer = input(
        f'Found unfinished progress in {progress_file}. Continue (c) or start fresh (f)? [c]: '
    ).strip().lower() or 'c'
    if answer.startswith('c'):
        all_data, department_position, course_index, parity = load_progress(progress_file)
    else:
        os.remove(progress_file)

Driver = webdriver.Chrome()

try:
    Driver.get(r'http://sess.shirazu.ac.ir/')
    input('Navigate to semester schedule page and press enter to continue ')

    select_element = Driver.find_element(By.ID, 'edDepartment')
    select_object = Select(select_element)
    all_obj_name = [arabicToPersian(string.text) for string in select_object.options[1:]]

    # Add more department indexes here when they should be crawled.
    toCrawlIndexes = [1, 2, 3, 4, 6, 88, 89, 9, 75, 10, 12, 18, 41, 74, 77, 78, 92, 68, 17]

    for department_position in range(department_position, len(toCrawlIndexes)):
        j = toCrawlIndexes[department_position]
        department_name = all_obj_name[j - 1]
        datas = all_data.setdefault(department_name, {})
        previous_courses = Driver.find_elements(By.CLASS_NAME, 'listOdd')
        previous_course = previous_courses[0] if previous_courses else None
        select_element = Driver.find_element(By.ID, 'edDepartment')
        Select(select_element).select_by_index(j)
        Driver.find_element(By.ID, 'edDisplay').click()
        print("crawling ", department_name, " ... ", j)

        wait_for_department_results(previous_course)
        length_odd, length_even = get_course_counts()
        print(length_odd, length_even)

        if length_odd == 0 and length_even == 0:
            print(f'No courses found for {department_name}; skipping department.')
            course_index = 0
            parity = 'odd'
            department_position += 1
            save_progress(progress_file, all_data, department_position, course_index, parity)
            recover_to_schedule()
            continue

        resume_course_index = course_index
        resume_parity = parity
        for course_index in range(course_index, length_odd):
            for current_parity in ("odd", "even"):
                if (course_index == resume_course_index and
                        resume_parity == "even" and current_parity == "odd"):
                    continue

                save_progress(progress_file, all_data, department_position, course_index, current_parity)
                course_was_scraped = scrape_course(
                    course_index, current_parity, datas
                )
                if not course_was_scraped:
                    if current_parity == "even":
                        course_index += 1
                        parity = "odd"
                    continue

                if current_parity == "odd":
                    parity = "even"
                else:
                    course_index += 1
                    parity = "odd"
                save_progress(progress_file, all_data, department_position, course_index, parity)

        course_index = 0
        parity = "odd"
        department_position += 1
        save_progress(progress_file, all_data, department_position, course_index, parity)
        recover_to_schedule()

    with open(output_file, 'w', encoding='utf-8') as f:
        print("saving...")
        json.dump(all_data, f, ensure_ascii=False)
    os.remove(progress_file)
    print("Crawl completed.")
except Exception as error:
    save_progress(progress_file, all_data, department_position, course_index, parity)
    print(f"Crawl stopped: {error}")
    print(f"Progress saved to {progress_file}. Run again to continue.")
finally:
    Driver.quit()
