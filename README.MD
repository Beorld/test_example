## Usage
#### Run tests locally

```
echo Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo Extract drivers
cd drivers
tar -xzvf geckodriver.tar.gz
tar -xavf chromedriver.tar.gz
cd ..

export CURRENT_SERVER=test
pytest --alluredir allure_results test_suites/OreFlow/ --os linux --browser firefox
```


#### Run tests in docker container using selenium-hub
Build image
```docker build -t tests:example .```
Run container
```docker run -d -it --name tests tests:example```
Run tests
```docker exec -e CURRENT_SERVER=master tests pytest test_suites/OreFlow/ --os linux --use_hub true --browser chrome```
