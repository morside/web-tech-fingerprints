<div id="logo", align="center">
    <h2>FINGERPRINTS<br>WEB TECHNOLOGY LOOKUP</h5>
</div>

#### showcase
<div id="showcase", align="center">
    <img src="https://github.com/morside/web-tech-fingerprints/src/assets/example.gif">
</div>

#### technologies:
this project contains 700 technologies, which are placed in the "tech_json.json" file. based on: https://www.wappalyzer.com/

#### requirements:
* kivy
* requests
* dnspython
* python3

#### install:
```bash
git clone https://github.com/morside/web-tech-fingerprints.git
cd /web-tech-fingerprints
```

#### install requirements:
install via requirements.txt file.
```bash
pip3 install -r requirements.txt
```
or install manually.
```bash
pip3 install Kivy requests dnspython
```

#### run:
```bash
python3 main.py
```

#### tests:
* tested on python v3.10.12 and v3.10.9
* tested on windows 10 and linux (ubuntu 22.04.3 LTS)

#### compile the android app:
linux and buildozer are required to compile the android app!

read the buildozer installation documentation: https://buildozer.readthedocs.io/en/latest/installation.html

after installing all the necessary dependencies.
```bash
buildozer android debug
```

to create your own init "buildozer.spec" file.
```bash
buildozer init
```

#### already compiled the android app:
```bash
bin/org.kivy.fingerprints-0.1-arm64-v8a_armeabi-v7a-debug.apk
```

#### android app tests:
* tested on android v6.0.1 (marshmallow) and v12 (snow cone)


