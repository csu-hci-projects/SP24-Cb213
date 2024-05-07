Our group comprised of Liam Hartman and Mason Stencel sought to improve the human computer interaction during race driving with a digital HUD to improve shifting and time looking at the road. 
Mason and I evenly split up the work and worked together for nearly everthing. 
We utilized a raspberry pi 4B connected to a bluetooth OBDII reader and an LCD Screen to display the information.
The OBDII reader can process data from the car such as engine codes, temperatures, and in our case gps data and engine speed. 
By far the greatest challenge was creating the script and getting it to work with data pulled from the car through the OBDII reader. This was an almost 20 hour process just to get a proper working connection.
There were endless small bugs throughout. Minor issues, such as the bluetooth on one of our phones being on, caused the program to not work and took countless hours to diagnose. 
Not to mention fine tuning the GUI and getting it to actually parse in values read in from the python script from the OBDII reader. 
Even though we used an existing plugin for the OBDII connection, it was still extremely difficult to setup and instantize. 
In the end we finally got it all to work and made a GUI that parsed the rpm reading from the OBDII reader as a String and utilized substrings to alter when and how text appeared warning you to shift.
The latency was suprisingly fast and the HUD kept updated with real time RPM to the thousandth. 
We jumped around with having different designs for the HUD many times, initially wanting to replicate a similar design to the one pictured below with red, yellow, and green lights indicating shift points and dynamically updating light/dark images to show progress through the RPM range,
but for the sake of visibility and experimentation, we decided that just using simple to understand dynamically updating text was more beneficial. 
![Alt text](data/Images/ExampleRPM.jpg?raw=true "Title")
![Alt text](data/Images/RectangleVersion.png?raw=true "Title")
The HUD displays a constantly updating numeric RPM count and the cars speed in MPH, it also displays text that changes from a green 'OK' to a yellow 'READY' 500 RPM before the optimal shift point, the optimal shift point is 
right at the top of the car's powerband which lies at about 5500 rpm in a Mazda CX-9. Which is the car we used for testing and trials as our more track spec car does not have the necessary registration to be driven on the public roads. 
The HUD updates bright red 'SHIFT' at the optimal shift point, clearly informing thedriver when to shift as to not hit the redline for too long and possible damage or overheat the engine, and to keep within the optimal powerband for the best overall carried speed. 
This is essential in track driving as even milliseconds shaved off with quality shifting can result in seconds better laptimes, which may seem insignificant on paper, but means a lot in racing. 

