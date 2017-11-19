#Pyquino Makefile

all: build

build: launchPyquino.py
	$(eval PYQTPATH = $(shell python -c "import PyQt5, os, sys;sys.stdout.write(os.path.dirname(PyQt5.__file__))"))
	pyinstaller -F $< -i ./icons/usb.ico --path="$(PYQTPATH)\Qt\bin"

run: build dist\launchPyquino.exe
	dist\launchPyquino.exe

clean:
	rd build /s /q
	rd dist /s /q
	del launchPyquino.spec
