# PTM_endpoint
Pedestrian Traffic Manager - Endpoint
### Objective
  The Pedestrian Traffic Manager (PTM) helps pedestrians to cross traffic signals and regulate traffic. 
### Working: 
- The camera detects pedestrians using face recognition 
- When a person starts waiting, the counter is initialized and a timer is started  
- When the counter reaches 10 or the timer is called, a request is made to the main traffic controller  

### Technical Specification  
- The application is built using Python 
- A camera is used as an endpoint  
- DNN is used for face recognition  

### Steps to run: 
- Open Command Prompt 
- Go to the file path that contains `Main.py`
- Type the command `python Main.py`

### Dependencies Needed: 
```
OpenCV – python
Imutils
Numpy
Time
Threading
```
### Reference: 
- https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning 
 
 
 
 
