import os
import pytest
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

@pytest.fixture
def driver():
    options = Options()
    options.headless = True
    options.binary_location = "/usr/bin/firefox"
    service = Service(executable_path='/usr/bin/geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    driver.quit()


@pytest.fixture
def driver_with_options(request):

    name_dir = request.param

    directory = os.path.join(
        os.path.dirname(__file__),
        '..', 'data', name_dir
    )

    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.listdir(directory) and "report.json" in os.listdir(directory):
        os.remove(os.path.join(directory, "report.json"))

    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", directory)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/json")

    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1920, 1080)

    yield driver

    driver.quit()


@pytest.fixture
def load_tc_1_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_1_(2.1.1.2.0.2.0.2.0.3.0)', 'This file name should not be accepted.xlsx'
    )


@pytest.fixture
def load_tc_2_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_2_(1.2.0.0.0.0.0.0.0.0.0)', 'stories.txt'
    )


@pytest.fixture
def load_tc_3_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_3_(1.1.1.1.0.0.0.0.0.0.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_4_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_4_(1.1.1.3.0.2.0.2.0.3.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_5_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_5_(1.1.2.2.3.2.1.2.0.3.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_6_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_6_(1.1.1.2.0.1.0.0.0.0.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_7_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_7_(1.1.1.2.0.2.0.1.0.0.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_8_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_8_(1.1.1.2.0.2.0.4.0.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_9_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_9_(1.1.2.2.2.2.2.2.1.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_10_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_10_(1.1.1.2.0.2.0.2.0.1.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_11_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_11_(1.1.2.2.2.2.2.2.2.3.1.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_12_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_12_(1.1.2.2.2.2.2.2.2.3.2.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_13_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_13_(1.1.1.2.0.2.0.2.0.2.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_14_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_14_(1.1.1.2.0.2.0.2.0.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_15_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_15_(1.1.1.2.0.2.0.3.0.2.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_16_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_16_(1.1.1.2.0.2.0.3.0.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_17_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_17_(1.1.2.2.1.2.0.2.0.2.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_18_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_18_(1.1.2.2.1.2.0.2.0.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_19_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_19_(1.1.2.2.1.2.0.3.0.2.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_20_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_20_(1.1.2.2.1.2.0.3.0.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_21_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_21_(1.1.2.2.2.2.1.2.0.2.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_22_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_22_(1.1.2.2.2.2.1.2.0.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_23_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_23_(1.1.2.2.2.2.1.3.0.2.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_24_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_24_(1.1.2.2.2.2.1.3.0.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_25_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_25_(1.1.2.2.2.2.2.2.2.2.3.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_26_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_26_(1.1.2.2.2.2.2.2.2.3.3.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_27_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_27_(1.1.2.2.2.2.2.3.2.2.3.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_28_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_28_(1.1.2.2.2.2.2.3.2.3.3.)', 'stories.xlsx'
    )


@pytest.fixture
def analyze_tc_1_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..','data', 'analyze_tc_1', 'stories.xlsx'
    ), os.path.join(
        os.path.dirname(__file__),
        '..','data', 'analyze_tc_1', 'oracle.json'
    ),

@pytest.fixture
def report_tc_2():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'report_tc_2', 'stories.xlsx'
    ), os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'report_tc_2', 'oracle.json'
    ),

@pytest.fixture
def desktop_download_all_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'desktop_download_all', 'desktop_app_results.json'
    ), os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'desktop_download_all', 'oracle.json'
    ),

@pytest.fixture
def desktop_single_us_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'desktop_single_us', 'desktop_app_single_us.json'
    ), os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'desktop_single_us', 'oracle.json'
    ),