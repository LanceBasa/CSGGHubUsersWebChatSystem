
# CITS3403-Web-23

## Project collaboration for CITS3403


### Members:
Lance Basa - 23420659  
Sahil Narula -23313963  
Midhin Viju - 22850881  

  
  

### Introduction

This is a CITS3403 - Agile Web Development Project in Collaboration with Lance, Sahil and Midhin.

The purpose of this project is to create a chat system that enables users to signup/register and login. The system will have a back-end database that will log all registered users and their chat history. Information about the game will be integrated in a chat bot system. Users can chat with other user to pair up and create a perfect team to dominate in CSGO!

  

### How to run

Please note, it is required to run this in linux terminal. Google Chrome (updated) is recommended to run this application. Other applications might cause some issues when running the application

1. Unzip the file in your directory  
2. Please install venv environment. This will require python and other packages. Click [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)for instructions on how to set-up venv environment (follow only up to installing flask).
3. Make sure that you are in venv environment. Type the following in console to set up the environment for the app to run
	> pip install -r requirements.txt
4. You should be in a directory where the app directory is visible(not inside app direcory). To run the program, type the following code in your terminal. 
	> flask run
	
you should see something like this

```
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
5. Hold CTRL key and click the http link to launch the website. Alternatively, you can copy the link and paste it into url bar.
6. User should now have access to the website (locally)


#### Running selTest.py and 

* Google chrome and firefox must be set up in venv to run tests
* requirements.txt should be installed before running tests (see How to run step 3)
* Server should be running before running selfTest.py (see How to run step 4)
* To run selTest.py, type the follwing in terminal, outside of app directory
 > python3 selTest.py

* To run unitTest.pytype the follwing in terminal, outside of app directory
 > python3 unitTest.py


  

### References links
https://cooltext.com/Edit-Logo?LogoID=732429307&732429307_Font=11840 - navs  
https://www.pxfuel.com/en/desktop-wallpaper-hkeus - bg for myprofile
https://wallpapers.com/wallpapers/cs-go-gun-display-window-eydtv0lpt70a7b9j.html - bg for chat  
https://www.pxfuel.com/en/desktop-wallpaper-ippfo - bg for login/register  
https://www.pxfuel.com/en/desktop-wallpaper-hmsog - bg for landing page  
https://www.pxfuel.com/en/desktop-wallpaper-wcvnv - bg for edit profile
https://counterstrike.fandom.com/wiki/Counter-Strike:_Global_Offensive - data
https://chat.openai.com/
