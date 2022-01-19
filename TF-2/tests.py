from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

url = "https://athensresearch.github.io/athens/"
driver = webdriver.Chrome()
skip = 0.3
actionChains = ActionChains(driver)

def create_page(driver, name):
    form = driver.find_element_by_xpath('//*[text()=\"Find or Create a Page\"]')
    sleep(skip)
    form.click()
    sleep(skip)
    form = driver.find_element_by_xpath('//*[@placeholder=\"Find or Create Page\"]')
    sleep(skip)
    form.send_keys(name)
    sleep(skip)
    form.send_keys(Keys.ENTER);
    sleep(skip)

def go_to_page(driver, name):
    create_page(driver, name)

def get_first_block(driver):
    return driver.find_element_by_xpath('//*[@class=\"block-content\"]/textarea')

def copy_first_block_ref(driver):
        bullet = driver.find_element_by_xpath('//button[@class=\"bullet\"]')
        sleep(skip)
        actionChains.context_click(bullet).perform()
        sleep(skip)
        driver.find_element_by_xpath('//*[text()="Copy block ref"]').click()
        sleep(skip)

def write_to_first_block(driver, text):
    form = get_first_block(driver)
    get_first_block(driver).click()
    sleep(skip)
    form.send_keys(text)
    sleep(skip)
    form.send_keys(Keys.ENTER);
    sleep(skip)

def paste_to_n_block(n):
    form = get_first_block(driver)
    get_first_block(driver).click()
    sleep(skip)
    for i in range(n):
        form.send_keys(Keys.ENTER);
        sleep(skip)
    form.send_keys(Keys.COMMAND, 'v')
    sleep(skip)

def click_on_reference(driver, text):
    driver.find_element_by_xpath(f'//*[@class="block"]//*[text()=\"{text}\"]').click()
    sleep(skip)

def remove_first_block(driver):
    first = get_first_block(driver)
    first.clear()
    sleep(skip)
    first.click()
    sleep(skip)
    first.send_keys(Keys.BACKSPACE);
    sleep(skip)

def is_on_the_page(driver, text):
    return driver.find_elements_by_xpath(f'//*[text()=\"{text}\"]') != []

def open_unlinked_references(driver):
    driver.find_element_by_xpath('//*[text()=\"Unlinked References\"]/parent::*/preceding-sibling::*').click()
    sleep(skip)

def open_linked_references(driver):
    driver.find_element_by_xpath('//*[text()=\"Linked References\"]/parent::*/preceding-sibling::*').click()
    sleep(skip)

# CRINGETF-29
def test_create_and_delete_linked_reference():
    try:
        driver.get(url)
        first_page_name = "Test page title Ą"
        second_page_name = "Test linked reference Ą <random_letters>"
        create_page(driver, first_page_name)
        write_to_first_block(driver, f"[[{second_page_name}]]")
        click_on_reference(driver, f"{second_page_name}")
        driver.find_element_by_xpath(f'//*[text()=\"{first_page_name}\"]')
        go_to_page(driver, first_page_name)
        remove_first_block(driver)
        go_to_page(driver, second_page_name)
        assert driver.find_elements_by_xpath(f'//*[text()=\"{first_page_name}\"]') == []
    except:
        print("Test test_create_and_delete_linked_reference failed")
    finally:
        driver.close()


# CRINGETF-30
def test_create_linked_references_for_existing_site():
    try:
        driver.get(url)
        first_page_name = "Test page title Ą"
        second_page_name = "Test linked reference Ą <random_letters>"
        create_page(driver, first_page_name)
        create_page(driver, second_page_name)
        go_to_page(driver, first_page_name)
        write_to_first_block(driver, f"[[{second_page_name}]]")
        click_on_reference(driver, f"{second_page_name}")
        driver.find_element_by_xpath(f'//*[text()=\"{first_page_name}\"]')
        go_to_page(driver, first_page_name)
        remove_first_block(driver)
        go_to_page(driver, second_page_name)
        assert driver.find_elements_by_xpath(f'//*[text()=\"{first_page_name}\"]') == []
    except:
        print("Test test_create_linked_references_for_existing_site failed")
    finally:
        driver.close()


# CRINGETF-31
def test_automatic_detection_unlinked_references():
    try:
        driver.get(url)
        first_page_name = "PageTitle1"
        second_page_name = "PageTitle2"
        third_page_name = "PageTitle3"
        refered_page_name = "ReferedSubject"
        for p in [first_page_name, second_page_name, third_page_name, refered_page_name]:
            create_page(driver, p)

        go_to_page(driver, first_page_name)
        write_to_first_block(driver, f"I like ReferedSubject")

        go_to_page(driver, second_page_name)
        write_to_first_block(driver, f"I likeReferedSubject")

        go_to_page(driver, third_page_name)
        write_to_first_block(driver, f"I like ReferedSubject very very much")

        go_to_page(driver, refered_page_name)
        open_unlinked_references(driver)
        assert is_on_the_page(driver, first_page_name)
        assert is_on_the_page(driver, second_page_name)
        assert is_on_the_page(driver, third_page_name)
        driver.find_element_by_xpath('//*[text()=\"Link\"]').click()

    except:
        print("Test test_create_linked_references_for_existing_site failed")
    finally:
        driver.close()

# CRINGETF-32
def test_references_to_existing_blocks():
    try:
        driver.get(url)
        first_page_name = "PageTitle1"
        second_page_name = "PageTitle2"
        for p in [first_page_name, second_page_name]:
            create_page(driver, p)

        go_to_page(driver, first_page_name)
        write_to_first_block(driver, f"Test block")
        assert is_on_the_page(driver, f"Test block")

        copy_first_block_ref(driver) 

        
        go_to_page(driver, second_page_name)
        paste_to_n_block(0)
        assert is_on_the_page(driver, f"Test block")

        go_to_page(driver, first_page_name)
        breakpoint()
        paste_to_n_block(1)
        assert is_on_the_page(driver, f"Test block")
    except:
        print("Test test_create_linked_references_for_existing_site failed")
    finally:
        driver.close()

# CRINGETF-33
def test_unlinked_to_linked_references():
    try:
        driver.get(url)
        first_page_name = "PageTitle1"
        second_page_name = "PageTitle2"
        third_page_name = "PageTitle3"
        refered_page_name = "PageTitle4"
        for p in [first_page_name, second_page_name, third_page_name, refered_page_name]:
            create_page(driver, p)
        
        for p in [first_page_name, second_page_name, third_page_name]:
            go_to_page(driver, p)
            write_to_first_block(driver, refered_page_name)
        
        go_to_page(driver, refered_page_name)
        open_unlinked_references(driver)
        driver.find_element_by_xpath('//*[text()="Link All"]').click()
        sleep(skip)
        for p in [first_page_name, second_page_name, third_page_name]:
            assert is_on_the_page(driver, p)
    except:
        print("Test test_create_linked_references_for_existing_site failed")
    finally:
        driver.close()
    
# CRINGETF-34
def test_editing_linked_references():
    try:
        driver.get(url)
        first_page_name = "A"
        second_page_name = "B"
        for p in [first_page_name, second_page_name]:
            create_page(driver, p)
        
        go_to_page(driver, second_page_name)
        open_linked_references(driver)
        assert not is_on_the_page(driver, "A")

        go_to_page(driver, "A")
        write_to_first_block(driver, f"[[{second_page_name}]]")

        go_to_page(driver, "B")
        linked_block = driver.find_element_by_xpath('//*[text()=\"Linked References\"]/parent::*/parent::*/following-sibling::*//*[@class=\"block-content\"]/textarea')
        linked_block.click()
        linked_block.send_keys("content")

        go_to_page(driver, "A")
        assert is_on_the_page(driver, "[[B]]content")

        go_to_page(driver, "B")
        linked_block = driver.find_element_by_xpath('//*[text()=\"Linked References\"]/parent::*/parent::*/following-sibling::*//*[@class=\"block-content\"]/textarea')
        linked_block.click()
        linked_block.send_keys(Keys.COMMAND, "a")
        sleep(skip)
        linked_block.send_keys(Keys.BACKSPACE) 
        sleep(skip)

        go_to_page(driver, "B")
        assert not is_on_the_page(driver, "A")

        go_to_page(driver, "A")
        assert not is_on_the_page(driver, "[[B]]content")
    except:
        print("Test test_create_linked_references_for_existing_site failed")
    finally:
        driver.close()

# CRINGETF-44
def test_editing_unlinked_references():
    try:
        driver.get(url)
        first_page_name = "A"
        second_page_name = "B"
        for p in [first_page_name, second_page_name]:
            create_page(driver, p)
        
        go_to_page(driver, second_page_name)
        open_linked_references(driver)
        assert not is_on_the_page(driver, "A")

        go_to_page(driver, "A")
        write_to_first_block(driver, f"{second_page_name}")

        go_to_page(driver, "B")
        open_unlinked_references(driver)
        linked_block = driver.find_element_by_xpath('//*[text()=\"Unlinked References\"]/parent::*/parent::*/following-sibling::*//*[@class=\"block-content\"]/textarea')
        linked_block.click()
        linked_block.send_keys("content")

        go_to_page(driver, "A")
        assert is_on_the_page(driver, "Bcontent")

        go_to_page(driver, "B")
        open_unlinked_references(driver)
        linked_block = driver.find_element_by_xpath('//*[text()=\"Unlinked References\"]/parent::*/parent::*/following-sibling::*//*[@class=\"block-content\"]/textarea')
        linked_block.click()
        linked_block.send_keys(Keys.COMMAND, "a")
        sleep(skip)
        linked_block.send_keys(Keys.BACKSPACE) 
        sleep(skip)

        go_to_page(driver, "B")
        assert not is_on_the_page(driver, "A")

        go_to_page(driver, "A")
        assert not is_on_the_page(driver, "Bcontent")
    except:
        print("Test test_create_linked_references_for_existing_site failed")
    finally:
        driver.close()

# CRINGETF-52
def test_create_page_with_existing_references():
    try:
        driver.get(url)
        first_page_name = "A"
        create_page(driver, first_page_name)
        write_to_first_block(driver, "abcd")
        go_to_page(driver, "abcd")

        open_unlinked_references(driver)

        assert is_on_the_page(driver, "A")
    except:
        print("Test test_create_linked_references_for_existing_site failed")
    finally:
        driver.close()


test_create_and_delete_linked_reference()
test_create_linked_references_for_existing_site()
test_automatic_detection_unlinked_references()
test_references_to_existing_blocks()
test_unlinked_to_linked_references()
test_editing_linked_references()
test_page_delete_deletes_references()
test_create_page_with_existing_references()



