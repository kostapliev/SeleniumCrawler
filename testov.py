from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time
import json
from ConnectionManager import ConnectionManager


cm = ConnectionManager()
compare = ""
dictionary = {}
driver = webdriver.Chrome("/home/konstantin/Downloads/chromedriver_linux64/chromedriver")
driver.get("http://search.rfbr.ru/")
dictionary_state = {"conquest_type": 0, "conquest_name": 0, "conquest_id": 0, "main_fok_id": 0, "fok_id": 0}
dictionary_state_copy = {}


# поставь влажок в True, чтобы считать json из файла
flajok = True
if flajok:
    with open("save_state.json", "r") as f:
        data = json.load(f)
        dictionary_state_copy = data.copy()
else:
    dictionary_state_copy = dictionary_state.copy()


def innerfunction(drivemecrazy):
    for tr1 in drivemecrazy.find_elements_by_xpath('/html/body/div[5]/div[2]/table/tbody/tr'):
        key1 = tr1.find_element_by_xpath('./td[1]')
        value1 = tr1.find_element_by_xpath('./td[2]')
        key1 = str(key1)
        value1 = str(value1)
        dictionary.update({key1: value1})
        try:
            # captchaclose(driver1)
            # тут так же не меняется xpath(на 1 увеличивается как и в других местах индекс
            input_ = drivemecrazy.find_elements_by_xpath('/html/body/div[5]/input')
            input_.click()
        except NoSuchElementException:
            return


# функция обхода по ссылкам проектов и сохранения их текстов
def project_tour(driver1):
    # находим ссылки проектов
    element_links = driver1.find_elements_by_xpath('/html/body/div[2]/div[3]/table[1]/tbody/tr/td/a')
    for iss in element_links:
        # compare = str(check_project(iss))
        iss.click()
        time.sleep(3)
        try:
            if driver.find_element_by_xpath('//*[@id="g-recaptcha"]'):
                # смена ip
                cm.new_identity()
                # функция с обходом капчи
                captchaclose1(driver, iss)
        except Exception:
            print("Нормальная ошибка")
        try:
            for tr in driver.find_elements_by_xpath('//*[@id="project_faded"]/div[2]/table/tbody/tr'):
                key = tr.find_element_by_xpath('./td[1]').text
                value = tr.find_element_by_xpath('./td[2]').text
                key = str(key)
                value = str(value)
                print(key + ": " + value)
                with open("test.txt", "a") as file:
                    file.write(key)
                    file.write(" - ")
                    file.write(value)
                    file.write("\n")
                file.close()
                dictionary.update({key: value})
                # with open("text.json", "w") as file:
                #    file.write(json.dumps(dictionary))

        except Exception:
            print('Can\'t find elements! Check xpath Ошибка в главной функции в записи дикт')
        try:
            closecrest()
        except Exception:
            print('Ошибка заключается в закрытии файла')


def closecrest():
    time.sleep(1)
    try:
        driver.find_element_by_xpath('//*[@id="project_faded"]/input').click()
        time.sleep(1)
    except Exception:
        print('Не могу найти крестик!!!')


def check_project1(driverg, compares, iss1):
    try:
        elem = driverg.find_element_by_xpath('/html/body/div[4]/div[2]/table/tbody/tr[3]/td[2]')
        print(compares)
        if elem.text == compares:
            return
        if elem.text != compares:
            closecrest()
            iss1.click()
            check_project1(driverg, compares, iss1)
    except NoSuchElementException:
        try:
            elem1 = driverg.find_element_by_xpath('/html/body/div[5]/div[2]/table/tbody/tr[3]/td[2]')
            if elem1.text == compares:
                return
            if elem1.text != compares:
                closecrest()
                iss1.click()
                check_project1(driverg, compares, iss1)
        except NoSuchElementException:
            try:
                elem2 = driverg.find_element_by_xpath('/html/body/div[6]/div[2]/table/tbody/tr[3]/td[2]')
                if elem2.text == compares:
                    return
                if elem2.text != compares:
                    closecrest()
                    iss1.click()
                    check_project1(driverg, compares, iss1)
            except NoSuchElementException:
                print('Can\'t find elements! Check xpath Ошибка в функции чекпроджект1 ')


def check_project(iss2):
    el1 = iss2.find_element_by_xpath('//a/../following-sibling::td[2]')
    check = el1.text
    return check


def captchaclose1(drivercap, iss1):
    times = 0
    if drivercap.find_element_by_xpath('//*[@id="g-recaptcha"]'):
        try:
            drivercap.find_element_by_xpath('/html/body/div[3]/input').click()
            time.sleep(2)
            iss1.click()
            time.sleep(3)
        except Exception:
            try:
                drivercap.find_element_by_xpath('/html/body/div[4]/input').click()
                time.sleep(2)
                iss1.click()
                time.sleep(3)
            except Exception:
                try:
                    drivercap.find_element_by_xpath('/html/body/div[5]/input').click()
                    time.sleep(2)
                    iss1.click()
                    time.sleep(3)
                except Exception:
                    try:
                        drivercap.find_element_by_xpath('/html/body/div[6]/input').click()
                        time.sleep(2)
                        iss1.click()
                        time.sleep(3)
                    except Exception:
                        try:
                            drivercap.find_element_by_xpath('//*[@id="project_faded"]/input').click()
                            iss1.click()
                            time.sleep(2)
                        except Exception:
                            print('Can\'t find closing button')
    try:
        if drivercap.find_element_by_xpath('//*[@id="g-recaptcha"]'):
            print('Нашел новую капчу')
            times += 1
            if (times == 40):
                time.sleep(60)
            captchaclose1(drivercap, iss1)
    except:
        print('тут ошибка в функции капчаклоуз. ')


def main():
    with open('test.txt', 'a') as f:
        f.write("Тут будут записываться данные: \n")
    f.close()
    select = Select(driver.find_element_by_xpath('//*[@id="conquest_type"]'))
    options = select.options
    for index in range(dictionary_state_copy["conquest_type"], len(options) - 1):
        dictionary_state.update({"conquest_type": index})
        select.select_by_index(index)
        time.sleep(3)

        try:
            select1 = Select(driver.find_element_by_xpath('//*[@id="conquest_name"]'))
            options1 = select1.options
        except Exception as e:
            print(e)
            print('EXC 1: Первый выбор из первого списка пуст')
            continue
        for index1 in range(dictionary_state_copy["conquest_name"], len(options1) - 1):
            dictionary_state.update({"conquest_name": index1})
            select1.select_by_index(index1)
            time.sleep(3)
            try:
                select2 = Select(driver.find_element_by_xpath('//*[@id="conquest_id"]'))
                options2 = select2.options
            except Exception as e1:
                print(e1)
                print('EXC 2: Первый выбор из второго списка пуст')
                continue
            for index2 in range(dictionary_state_copy["conquest_id"], len(options2) - 1):
                dictionary_state.update({"conquest_id": index2})
                select2.select_by_index(index2)
                time.sleep(3)
                try:
                    select3 = Select(driver.find_element_by_xpath('//*[@id="main_fok_id"]'))
                    options3 = select3.options
                except Exception as e2:
                    print(e2)
                    print('EXC 3: Первый выбор из  третьего списка пуст')
                    continue
                for index3 in range(dictionary_state_copy["main_fok_id"], len(options3) - 1):
                    dictionary_state.update({"main_fok_id": index3})
                    try:
                        select3.select_by_index(index3)
                    except Exception:
                        select3 = Select(driver.find_element_by_xpath('//*[@id="main_fok_id"]'))
                        options3 = select3.options
                        select3.select_by_index(index3)
                    time.sleep(3)
                    try:
                        select4 = Select(driver.find_element_by_xpath('//*[@id="fok_id"]'))
                        options4 = select4.options
                    except Exception as e3:
                        print(e3)
                        print('EXC 4: Первый выбор из четвертого списка пуст')
                        continue
                    for index4 in range(dictionary_state_copy["fok_id"], len(options4) - 1):
                        dictionary_state.update({"fok_id": index4})
                        select4.select_by_index(index4)
                        time.sleep(3)
                        with open("save_state.json", "w") as write_file:
                            json.dump(dictionary_state, write_file)

                        try:
                            time.sleep(2)
                            driver.find_element_by_xpath('/html/body/div[2]/div[3]/table[1]/tbody')
                        except NoSuchElementException as exs:
                            print(exs)
                            print("Не подгрузилась таблицы. Первый элемент из 5 списка пустой")
                            continue
                        try:
                            # находим ссылки проектов
                            element_links = driver.find_elements_by_xpath(
                                '/html/body/div[2]/div[3]/table[1]/tbody/tr/td/a')
                            for iss in element_links:
                                # compare = str(check_project(iss))
                                iss.click()
                                time.sleep(3)
                                try:
                                    if driver.find_element_by_xpath('//*[@id="g-recaptcha"]'):
                                        # смена ip
                                        cm.new_identity()
                                        # функция с обходом капчи
                                        captchaclose1(driver, iss)
                                except Exception:
                                    print("Нормальная ошибка")

                                # check_project1(driver, compare, iss)
                                try:
                                    for tr in driver.find_elements_by_xpath('//*[@id="project_faded"]/div[2]/table/tbody/tr'):
                                        key = tr.find_element_by_xpath('./td[1]').text
                                        value = tr.find_element_by_xpath('./td[2]').text
                                        key = str(key)
                                        value = str(value)
                                        print(key + ": " + value)
                                        with open("test.txt", "a") as file:
                                            file.write(key)
                                            file.write(" - ")
                                            file.write(value)
                                            file.write("\n")
                                        file.close()
                                        dictionary.update({key: value})
                                        # with open("text.json", "w") as file:
                                        #    file.write(json.dumps(dictionary))

                                except Exception:
                                    try:
                                        for tr in driver.find_elements_by_xpath(
                                                '/html/body/div[4]/div[2]/table/tbody/tr'):
                                            key = tr.find_element_by_xpath('./td[1]').text
                                            value = tr.find_element_by_xpath('./td[2]').text
                                            key = str(key)
                                            value = str(value)
                                            with open("test.txt", "a") as file:
                                                file.write(key)
                                                file.write("   -  ")
                                                file.write(value)
                                                file.write("\n")
                                            file.close()
                                            dictionary.update({key: value})
                                            # with open("text.json", "w") as file:
                                            #     file.write(json.dumps(dictionary))
                                    except Exception:
                                        try:
                                            for tr in driver.find_elements_by_xpath(
                                                    '//*[@id="project_faded"]/div[2]/table/tbody/tr'):
                                                key = tr.find_element_by_xpath('./td[1]').text
                                                value = tr.find_element_by_xpath('./td[2]').text
                                                key = str(key)
                                                value = str(value)
                                                with open("test.txt", "a") as file:
                                                    file.write(key)
                                                    file.write("   -  ")
                                                    file.write(value)
                                                    file.write("\n")
                                                file.close()
                                                dictionary.update({key: value})
                                                # with open("text.json", "w") as file:
                                                #     file.write(json.dumps(dictionary))
                                        except Exception:
                                            print(
                                                'Can\'t find elements! Check xpath Ошибка в главной функции в записи дикт')
                                try:
                                    closecrest()
                                    time.sleep(1)
                                except Exception as errr:
                                    print(errr)
                                    print('Ошибка заключается в закрытии файла')

                            time.sleep(3)
                            # это находит ссылки на переход страниц
                            sec = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/table[2]/tbody/tr/td/span/a')
                            for isn in sec:
                                try:
                                    isn.click()
                                    time.sleep(3)
                                except Exception as e:
                                    print(e)
                                    # continue
                                    try:
                                        driver.find_element_by_xpath('/html/body/div[2]/div[3]/table[2]/tbody/tr/td/span/a[1]').click()
                                        time.sleep(4)
                                    except Exception as r:
                                        print("Ошибка в переходе по страницам")
                                # тут необходимо вызывать функцию обхода по проектам
                                project_tour(driver)
                                time.sleep(3)

                        except Exception as es:
                            print(es)

    jsondata = json.dumps(dictionary)
    with open("data.json", "w") as file:
        file.write(jsondata)


if __name__ == "__main__":
    main()
