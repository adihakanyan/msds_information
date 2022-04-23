from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


def start_search():
    """The function asks the user to enter a name of material and returns information on: Hazards Identification,
    First Aid Measures, Fire Fighting Measures(NFPA Rating), Physical and Chemical Properties of the material.
    """

    search = user_input_material()
    quit_program(search)
    parameters = params(search)
    google_soup_driver = creat_beautifulSoup_google(parameters)
    url = url_material(google_soup_driver)
    driver = creat_drive_website(url)
    scrolling_pade(driver)
    soup_driver = creat_beautifulSoup_website(driver)
    data = extricate_data_form_beautiful(soup_driver)
    print(f"\n{data}\n")
    write_data_to_file(data, search)
    close_driver(driver)
    start_search()


def extricate_data_form_beautiful(soup_driver):
    """The function pulling data from the html to a 'data'(string)  object.

    soup_driver(BeautifulSoup): represent the information of Fisher Scientific website
    """

    # string that contains all the data necessary
    data = ""

    # section 3
    data = Separation_between_sections(data, 3)
    names_to_find_3 = ["Potential Health Effects", "Eye:", "Skin:", "Ingestion:", "Inhalation:", "Chronic:"]
    data = extricate_info_from_section(soup_driver, data, 3, names_to_find_3)

    # section 4
    data = Separation_between_sections(data, 4)
    names_to_find_4 = ["Eyes:", "Skin:", "Ingestion:", "Inhalation:", "Notes to Physician:"]
    data = extricate_info_from_section(soup_driver, data, 4, names_to_find_4)

    # section 5
    data = Separation_between_sections(data, 5)
    names_to_find_5 = ["NFPA Rating:"]
    data = extricate_info_from_section(soup_driver, data, 5, names_to_find_5)

    # section 9
    data = Separation_between_sections(data, 9)
    names_to_find_9 = ["Physical State:", "Vapor Pressure:", "Boiling Point:", "Solubility:",
                       "Specific Gravity/Density:",
                       "Molecular Formula:", "Molecular Weight:"]
    data = extricate_info_from_section(soup_driver, data, 9, names_to_find_9)

    return data


def extricate_info_from_section(soup_driver, data, section_number, names_to_find):
    """The function extricate specific information('names_to_find') from the driver('soup_driver') in a specific section
    ('section').

    soup_driver(BeautifulSoup): represent the information of fisher scientific website
    data(string): a string that contains all the information we have stored
    num_of_section(int): represent the number of the section in the website
    names_to_find(list): a list of all the title of the information we want to extract
    """
    p_list = soup_driver.findAll("p")
    # add 1 to get the correct section in "inspect" of the website
    p = p_list[section_number + 1]
    # all the info in the paragraph
    title_and_data = p.findChildren()

    for i in title_and_data:
        if str(i.next_element) in names_to_find:
            # title
            data += str(i.next_element)
            # data
            data += str(i.nextSibling) + "\n\n"

    return data


def user_input_material():
    """The function get an input of material or 'q' (quit) from the user."""

    print("If you wants to quit press 'q'")
    return input("Please enter the name of the material you want to get information about: ")


def quit_program(string):
    """If the given string is 'q' the program will be treatment safely.

     string(string): input the user entered
     """

    if string == "q":
        print("Goog bye :)")
        quit()


def params(search):
    """The function receive string and return map that contain search value.

    search(string): input the user entered.
    """

    return {"q": "fscimage.fishersci.com " + search}


def creat_beautifulSoup_google(parameters):
    """The function receive a map that contains search value and return google search in a form of a beautifulSoup and
    google driver.

    parameters(map): map that contains the search value in the key 'q'
    """
    driver_service = Service(executable_path="C:\webdrivers\chromedriver.exe")
    google_driver = webdriver.Chrome(service=driver_service)
    google_url = "https://www.google.com/search?q=" + str(parameters['q'])
    google_driver.get(google_url)
    # get the text of the page
    google_html = google_driver.page_source  # type - str
    close_driver(google_driver)
    # create a beautifulSoup .
    return BeautifulSoup(google_html, "html.parser")


def url_material(google_soup_driver):
    """The function receive a beautifulSoup of google search and return url of a website.

    google_soup_driver(beautifulSoup): represent the information of google search website
    """

    url_msds = google_soup_driver.find("div", {"class": "yuRUbf"})
    return url_msds.next.attrs["href"]


def creat_drive_website(url):
    """The function get url, open the website and return the driver

    url(string): represent the url of Fisher Scientific
    """

    driver_service = Service(executable_path="C:\webdrivers\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    driver.get(url)
    return driver


def scrolling_pade(driver):
    """The function scroll the pade till the end.

    driver(selenium.webdriver.chrome.webdriver.WebDriver): a website
    """

    time.sleep(3)
    previous_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        time.sleep(3)

        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
        previous_height = new_height


def creat_beautifulSoup_website(driver):
    """The function receive driver of the website and return a beautifulSoup of that website

    driver(selenium.webdriver.chrome.webdriver.WebDriver): a website
    """

    # get the text of the page
    html = driver.page_source  # type - str
    print()
    # create a beautifulSoup .
    return BeautifulSoup(html, "html.parser")


def write_data_to_file(data, file_name):
    """The function receive the name of the file and creat it if it does not exist and that put the data in to the
    file.

    data(string): a string that contains all the information we have stored
    file_name(string): the name of the file we want to open
    """

    with open(file_name + ".txt", 'w') as f:
        f.write(data)


def close_driver(driver):
    """The function receive drivers and close them

    driver(selenium.webdriver.chrome.webdriver.WebDriver): a website

    """

    driver.close()


def Separation_between_sections(data, section_number):
    """The function get the data and creat a dashed line whit title of the number section

    data(string): a string that contains all the information we have stored
    num_of_section(int): represent the number of the section in the website
    """

    data += "Section" + str(section_number) + "\n"
    data += "---------------------------------------------------------------------------\n\n"
    return data


def main():
    start_search()


if __name__ == "__main__":
    main()
