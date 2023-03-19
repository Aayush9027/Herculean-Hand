# Herculean Hand👆✌🖐👌
An AI-based application which let us do tasks by moving our Hand in Air. It is developed in python using OpenCv and MediaPipe 

## Tech Stacks:💻
- OpenCV (for image processing and drawing)
- Mediapipe (for Hand Tracking)
- PyAutoGui (for controlling mouse movement and click)
- Pycaw (to link up with the system's volume)
- Numpy

## Prerequisites:
- You should install python version 3.7 or more
- Import all modules required for the project using this command
```
pip install <module name>
```
## Features :

* Can track your hand in real-time
* Can Move Your Cursor corresponding to your Index finger movement
* Can draw on your System screen based on your Index finger movement
* Can change your computer's volume based on your hand activity

## Working :

* As You Run the Code , a window will pop-up to see How many Fingers of your Hand are Up.
* According to the count of Fingers which are Up ,User will be redirected to that numbered task. 
* Tasks which User can perform are- 
  ### 1. AI Virtual Mouse :☝✌ 
  
     * As soon as the user shows up his hand in the camera the application detects it & draws a bounding box around the hand.
     * If User shows only Index Finger than he/she can Move Cursor.
     * To Click, User's Index and Middle finger both should be Up simultaneously. 

     ![final](https://user-images.githubusercontent.com/78357575/123516002-93aed580-d6b7-11eb-835b-ac7b284850d5.jpg)

  ### 2. AI Virtual Paint :☝✌ 
  
     * As soon as the user shows up his hand in the camera the application detects it & draws a bounding box around the hand.
     * If User shows only Index Finger than he/she is in drawing mode.
     * To Select different color or eraser from the top of Canvas, User must select it by taking his both Index and Middle finger together at the top of icon.
 
     ![Ai-Virtual-Painter_f](https://user-images.githubusercontent.com/78357575/123515066-b808b300-d6b3-11eb-8082-97a67f5493c9.jpg)
  
  ### 3. Gesture Volume Control :🤏👌
  
    * As soon as the user shows up his hand in the camera the application detects it & draws a bounding box around the hand.
    * According to the distance between user's Index finger and Thumb it displays the volume in the volume bar on the screen
    * To set the volume as the system's volume user has to bend his pinky finger simultaneously.

     ![volume-control_f](https://user-images.githubusercontent.com/78357575/123513770-9952ee00-d6ac-11eb-9c55-de3e368c2641.png)
    
## Note :📝 
Feel free to file a new issue with a respective title and description on the **Herculean-Hand**. If you already found a solution to your problem, I would love to review your pull request! 

## Contribution :📲
1. Clone the repository 
```
$git clone https://github.com/Aayush9027/Herculean-Hand.git
```
2. Check the status of your file 
```
$git status
```

3.For using VScode for editing your files 
```
$git code .
```
4. To directly add your files to github
```
$git add .
```
5. After writing your code commit your changes 
```
$git commit -m  <message>
```
6. To push your code to reposoitory
```
$git push origin master
```
Thats all about installation and version control with **Git**
