#Pyquino Makefile

all: build run

build: launchPyquino.py
	pyinstaller -F $< -i ./icons/usb.ico \
--path="C:\Users\Lin\AppData\Local\Programs\Python\Python35\Lib\site-packages\PyQt5\Qt\bin" \
--add-binary="core/vrep_remoAPI/remoteApi.dll;."

run: build dist\launchPyquino.exe
	dist\launchPyquino.exe

clean:
	rd build /s /q
	rd dist /s /q
	del launchPyquino.spec
