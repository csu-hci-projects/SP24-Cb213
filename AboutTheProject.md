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
