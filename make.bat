@ECHO OFF

REM Nicked this from Hy
REM https://github.com/hylang/hy/blob/master/make.bat

if "%1" == "" goto help

if "%1" == "help" (
	 :help
	 echo. No default step. Use setup.py
	 echo.
	 echo.  Other targets:
	 echo.
	 echo.	 - docs
	 echo.	 - full
	 echo.
	 echo.	 - dev "test & flake"
	 echo.	 - flake
	 echo.	 - test
	 echo.	 - diff
	 echo.	 - d
	 echo.	 - r
	 echo.	 - clean
	 echo.
	 goto :EOF
)

if "%1" == "docs" (
:docs
	 cd docs
	 make.bat html
	 cd ..
goto :EOF
)

if "%1" == "upload" (
:upload
	 python setup.py sdist upload
goto :EOF
)

if "%1" == "clear" (
:clear
	 cls
goto :EOF
)

if "%1" == "d" (
:d
	 call :clear
	 call :dev
goto :EOF
)

if "%1" == "test" (
:test
	 call :venv
	 nosetests -sv
goto :EOF
)

if "%1" == "venv" (
:venv
	 echo.%VIRTUAL_ENV% | findstr /C:"ccarps" 1>nul
	 if errorlevel 1 (
		  echo.You're not in a ccarps virtualenv. Exiting.
	 ) ELSE (
		  echo.We're properly in a virtualenv. Going ahead.
	 )
goto :EOF
)

if "%1" == "flake" (
:flake
	 echo.flake8 ccarps tests
	 flake8 ccarps tests
goto :EOF
)

if "%1" == "dev" (
:dev
	 call :test
	 call :flake
goto :EOF
)

if "%1" == "d" (
:d
	 call :clear
	 call :dev
goto :EOF
)

if "%i" == "diff" (
:diff
	 git diff --color
goto :EOF
)

if "%1" == "r" (
:r
	 call :d
	 call :diff
goto :EOF
)

if "%1" == "full" (
	 call :docs
	 call :d
goto :EOF
)

if "%1" == "clean" (
:clean
	if EXIST ccarps\*.pyc cmd /C del /S /Q ccarps\*.pyc
	if EXIST tests\*pyc cmd /C del /S /Q tests\*pyc
	for /r %%R in (__pycache__) do if EXIST %%R (rmdir /S /Q %%R)
	if EXIST dist\NUL cmd /C rmdir /S /Q dist
	if EXIST ccarps.egg-info\NUL cmd /C rmdir /S /Q ccarps.egg-info
	if EXIST docs\_build\NUL cmd /C rmdir /S /Q docs\_build
	goto :EOF
)

echo.Error: '%1' - unknown target
echo.
goto :help