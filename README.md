# Project-Python_git_linux

First :

I created the bash file scrapping.sh which : scrap the souce code of the google finance page for S&P500 and put this code in a text file named : page_scrape.txt then it get the value of the S&P500 and put it along with the current date and time in a csv file named values.csv

Second :

I created the python file : create_dashboard.py that create the dashboard where there is : - The current value of S&P500
                                                                                            - Some statistics on differents period : daily, weekly and monthly
                                                                                             -the stats are : the min value, max, Mean and volatility
The page update each 5min. I didnt get the point of having the report only at 8pm because those stats can be interesting at any moment of the day so i decided to update it each time the tue dashboard is refreshing.

                                                                                              - A graph of the value of S&P 500 in function of the time
                                                                     
 Third :
 
 I tried to automatize the scrapping and the creation of the dashboard each 5min with a crontab but this dosnt work much here are the line of code to show the crontab :
                                                                                             
[ec2-user@ip-172-31-43-91 Project-Python_git_linux]$ pwd
/home/ec2-user/Projet_Younes_Bichra/Project-Python_git_linux
[ec2-user@ip-172-31-43-91 Project-Python_git_linux]$ ls
create_dashboard.py  page_scrape.txt  README.md  scrapping.sh  update_dashboard.sh  values.csv
[ec2-user@ip-172-31-43-91 Project-Python_git_linux]$ crontab -l
*/5 * * * * /bin/bash /home/ec2-user/Projet_Younes_Bichra/Project-Python_git_linux/scrapping.sh
*/5 * * * * /bin/bash /home/ec2-user/Projet_Younes_Bichra/Project-Python_git_linux/update_dashboard.sh
[ec2-user@ip-172-31-43-91 Project-Python_git_linux]$


In the first place I saw that it was probably because I was not erasing the old dashboard when trying to create a new one so i create a bash file named update_dashboard.sh that kill the old dashboard and run the create_dashboard script. Then I've put this script in the crontab instead of create_dashboard.py as you can see above  (click on the readme file to make it easier to read)
But I still have the same problem 

4th :

I've cloned this github repesitory and moved all the files inside 
