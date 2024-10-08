from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import json
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

    data['title'] = arabicToPersian(Driver.find_element(By.ID,  'edName').text)
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
    

Driver = webdriver.Chrome()

all_data = {}

Driver.get(r'http://sess.shirazu.ac.ir/')

input('Navigate to semester schedule page and press enter to continue ')

select_element = Driver.find_element(By.ID,  'edDepartment')
select_object = Select(select_element)

all_obj_name = [arabicToPersian(string.text) for string in select_object.options[1:]]
# select units 

toCrawlIndexes = [1,9,10,12,18,41,74,77,78,91]

for j in toCrawlIndexes:
    datas = dict()
    select_element = Driver.find_element(By.ID,  'edDepartment')
    select_object = Select(select_element)
    select_object.select_by_index(j)
    Driver.find_element(By.ID,  'edDisplay').click()
    print("crawling ",select_element, " ...")
    

    listOdd = 'listOdd'
    listEven = 'listEven'

    time.sleep(2)
    
    coursesOdd = Driver.find_elements(By.CLASS_NAME, listOdd)
    coursesEven = Driver.find_elements(By.CLASS_NAME, listEven)
    lengthOdd = len(coursesOdd)

    for i in range(lengthOdd):

        # Odd list
        coursesOdd = Driver.find_elements(By.CLASS_NAME, listOdd)

        coursesOdd[i].click()
        serial, data = get_course_details()
        datas[serial] = data
        Driver.back()

        # Even list
        coursesEven = Driver.find_elements(By.CLASS_NAME, listEven)

        try:
            coursesEven[i].click()
            serial, data = get_course_details()
            datas[serial] = data
            Driver.back()
        except Exception as e:
            pass
    
    all_data[all_obj_name[j-1]] = datas
    Driver.back()

with open('data.json', 'w', encoding="utf-8") as f:
    print("saving...")
    json.dump(all_data, f, ensure_ascii=False)
