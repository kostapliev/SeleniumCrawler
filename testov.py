from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time
import json


# надо добавить функцию, которая закрывает капчу каждый раз перед основными действиями
def captchaclose(drivers):
    try:
        crest = drivers.find_element_by_xpath('/html/body/div[3]/input')
        # закрыть его
        crest.click()
        return
    except NoSuchElementException:
        print('Не нашел капчу')
        return


# эту функцию пока нигде не используем, но она понадобится в будушем
def domhaschanged(drivers):
    drivers.execute_script("""
        var s = false
        targetNode = document.getElementById('search_content');
        config = { attributes: true, childList: true, subtree: true };
        callback = function(mutationsList, observer) {
        for(mutation of mutationsList) {
            s = true
            if (mutation.type === 'childList') {
                console.log('A child node has been added or removed.');
            }
            else if (mutation.type === 'attributes') {
                console.log('The ' + mutation.attributeName + ' attribute was modified.');
            }
        }
        };
        const observer = new MutationObserver(callback);
        observer.observe(targetNode, config);
        if(s === true) {
            observer.disconnect();
        }
        """)


# функция обхода по ссылкам проектов и сохранения их текстов
def project_tour(driver1):
    element_links1 = driver1.find_elements_by_xpath('/html/body/div[2]/div[3]/table[1]/tbody/tr/td/a')
    for i in element_links1:
        i.click()
        time.sleep(2)
        for tr1 in driver.find_elements_by_xpath('/html/body/div[4]/div[2]/table/tbody/tr'):
            key1 = tr1.find_element_by_xpath('./td[1]')
            value1 = tr1.find_element_by_xpath('./td[2]')
            key1 = str(key1)
            value1 = str(value1)
            dictionary.update({key1: value1})
            try:
                # captchaclose(driver1)
                input_ = driver1.find_elements_by_xpath('/html/body/div[4]/input')
                input_.click()
            except NoSuchElementException:
                return

    return


dictionary = {}


driver = webdriver.Firefox()
driver.get("http://search.rfbr.ru/")

dat = open("output.json", "w")

select = Select(driver.find_element_by_xpath('//*[@id="conquest_type"]'))
options = select.options
for index in range(0, len(options) - 1):
    select.select_by_index(index)
    time.sleep(1)
    try:
        select1 = Select(driver.find_element_by_xpath('//*[@id="conquest_name"]'))
        options1 = select1.options
    except Exception as e:
        print(e)
        print('Exception 1')
        continue
    for index1 in range(0, len(options1) - 1):
        select1.select_by_index(index1)
        time.sleep(1)
        try:
            select2 = Select(driver.find_element_by_xpath('//*[@id="conquest_id"]'))
            options2 = select2.options
        except Exception as e1:
            print(e1)
            print('Exception 2')
            continue
        for index2 in range(0, len(options2) - 1):
            select2.select_by_index(index2)
            time.sleep(1)
            try:
                select3 = Select(driver.find_element_by_xpath('//*[@id="main_fok_id"]'))
                options3 = select3.options
            except Exception as e2:
                print(e2)
                print('Exception 3')
                continue
            for index3 in range(0, len(options3) - 1):
                select3.select_by_index(index3)
                time.sleep(3)
                try:
                    select4 = Select(driver.find_element_by_xpath('//*[@id="fok_id"]'))
                    options4 = select4.options
                except Exception as e3:
                    print(e3)
                    print('Exception 4')
                    continue
                for index4 in range(0, len(options4) - 1):
                    select4.select_by_index(index4)
                    time.sleep(3)
                    try:
                        els = driver.find_element_by_xpath('/html/body/div[2]/div[3]/table[1]/tbody')
                    except Exception as exs:
                        print(exs)
                        print("Не подгрузилась таблицы")
                        continue
                    try:
                        # находим ссылки проектов
                        element_links = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/table[1]/tbody/tr/td/a')
                        for iss in element_links:
                            iss.click()
                            time.sleep(3)
                            # Поменялся тут xpath. Причина: неизвестна
                            # for elemproftr in driver.find_elements_by_xpath('/html/body/div[5]/div[2]/table/tbody/tr')
                            for tr in driver.find_elements_by_xpath('/html/body/div[4]/div[2]/table/tbody/tr'):
                                key = tr.find_element_by_xpath('./td[1]')
                                value = tr.find_element_by_xpath('./td[2]')
                                key = str(key)
                                value = str(value)
                                dictionary.update({key: value})
                                # далее необходимо перевести в json и после этого сохранить в файл
                                # это происходит в конце
                            try:
                                elementos = driver.find_element_by_id('project_faded')
                                driver.execute_script("""
                                var elementos = arguments[0];
                                elementos.parentNode.removeChild(elementos);
                                """, elementos)
                            except Exception as errr:
                                print(errr)
                                print('Ошибка заключается в закрытии файла')
                                print('Есть альтернативный способ, более элегантный: просто через click() на крестик')
                        # это находит ссылки на переход страниц
                        sec = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/table[2]/tbody/tr/td/span/a')
                        for isn in sec:
                            isn.click()
                            # тут необходимо вызывать функцию обхода по проектам
                            project_tour(driver)
                            time.sleep(2)

                    except Exception as es:
                        print(es)

jsonData = json.dumps(dictionary)

with open("data.json", "w") as file:
    file.write(jsonData)
