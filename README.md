# PyQt-Projects

This repository contains my desktop applications created using the **PyQt5** library.

## The Ruffier Test

This application will allow you to use the *Ruffier test* to conduct a primary diagnosis of your health.
There are 2 variants of the application. 

The task 1 folder contains a simple version of the application. 
In this version, there are only 3 windows: The Greeting, the main part, and the result. 
Eventually, the user will receive the Rufier index, which will report the health status. 

In the second version of the application, each stage is shown in a separate window and a new timer is added that counts down the time of the stage. 
Compared to the first option, you can not skip any stage, as the buttons are locked until the timer ends.

## Psychological test

There are 3 variants of this application in the psytest folder.

1) In the simple version, all the questions are in one window. Only 10 questions. The answer appears in a new window
2) In the medium difficulty version, only 1 question is visible in the window.
   The code added the AllQuestions class with the methods of which the logic of pressing the forward and backward buttons was implemented.
3) In the most complex version of the application, a separate file is added with the correct answers. 
   With this approach, the original answers will be correct and there will be no errors in the test. 
   The test_dataclasses contains the data object model. 
   There is a transition to the object form which simplifies the work since we can access the fields. 
   The Main_Window class also appears which controls the operation of the program. 
   At the end of the program, the ResultTable class runs which shows the results window. 
   Compared to the "easy" and "medium" levels here you can see which answers influenced this profession

## Financial Calculator
This project implements the logic of a financial calculator. You can understand how long it will take for the project to pay off. You can specify the bid, amount, and time and find out how many investments you need now to get this investment

## Memo Card
The app is designed for learning a foreign language. You can create a card, correct and incorrect answers. After that, there are 4 possible answers, choosing one of them we will find out whether it is the correct answer or not. This way you can easily learn new words of a foreign language