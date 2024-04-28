# Final-Year-Project-TicketRadar-ADP
Instructions for Running TicketRadar
1. Install Python
Before running TicketRadar you need to have Python Installed on your computer. 
Python can be downloaded from the official website
2. Install Django
Django can be installed by running  the command: pip install django
3. Navigate to the TicketRadarProject
Change the directory through the terminal using the command: cd projectfiles
4. Run Migrations
run the following  command to make migrations: python manage.py migrate
5. Start the Development Server
run the development server by typing this command in the terminal : python manage.py runserver
The project can  be accesed in a browser at http://127.0.0.1:8000/
6. Create SuperUser 
 To access  the built-in admin panel you can use the terminal command: python manage.py createsuperuser
 7. Access the Admin Panel
 when the server is running you can access the admin panel navigating to http://127.0.0.1:8000/ and log in with the superuser credentials you created
 8. Granting Event Organiser Access 
 In order to have event organiser access you need to have a profile created.
 Access the admin panel, navigate to Account/Users, and tick the box "Is event organizer"
 Click Save to  save your changes
 9. Add funds
 To add funds to an account you have to access the admin panel and  navigatte to Account/Users/(your useranme). Click on the username, and scroll down until you see the Amount box. Enter the ammount  you want to add and click save.
 10. Use the platform