import pytest
import os.path
from fixture.application import Application
from fixture.db import DbFixture
import json
import importlib
import jsonpickle

fixture = None
target = None

@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = config["web"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    fixture.session.ensure_login(username=config['webadmin']['username'], password=config['webadmin']['password'])
    return fixture

@pytest.fixture(scope = 'session', autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

#описание опций
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")


#функция для загрузки конфигурации
def load_config(file):
    global target
    if target is None:
        #определяем путь относительно директории проекта
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target

#прописываем фикстуру в conftest, т.к. предполагается, что не все тесты будут с ДБ, если все тесты с ДБ, то нужно в апликейшн добавить фикстуру
#помечаем фикстурой функцией. session - в начале активируем класс,в конце останавливаем
@pytest.fixture(scope = 'session')
def db(request, config):
    db_config = load_config(request.config.getoption("--target"))["db"]
    #класс
    dbfixture = DbFixture(host=db_config["host"], name=db_config["name"], user=db_config["user"], password=db_config["password"])
    #объявляем финализацию для него
    def fin():
        dbfixture.destroy()
    #регистрируем
    request.addfinalizer(fin)
    return dbfixture

# генератор тестов, динамически подставляет значения параметров
#обработка фикстур, которые начинаются с префикса дата
def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])

def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_json(file):
    # os.path.abspath(__file__) - 'это путь к текущему файлу конфтест
    # dirname получаем директорию, в которой он находится - это корневая дир проекта
    # join подклеиваем путь к json файлу
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        # перекодируем обратно в в формат объектов питон
        return jsonpickle.decode(f.read())

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))



