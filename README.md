# Selenium job to automate queries to check last posts of Module Data Structures &amp; Algorithms

Web-testing for course Data Structures &amp; Algorithms

## Structure

- Inside the src folder is the main script that executes the selenium job
- Inside the src/report folder is a csv file containing the report of the last sessions checked with selenium for the module Data &amp; Algorithms. The report stores the date of selenium session, the date of last feed posted, the name of the person who posted the last feed, and the title of the last feed. Note: The idea is that if the professor writes an important feed, we can see quickly because is the professor and probably the title will be something relevant.
- Inside the folder video is a live demo of how the selenium job is executed.

### Notes

- The .env file containing my credentials is not uploaded in the GitHub to secure my password. Upon request, I can send my credentials to verify the code.
- A possible extension of the code could be the deployment via containers like Docker. Using Docker we could add a scheduler that runs the web testing task every day. The only challenge to this extension is tackling the two-factor authentication.
- At the moment the two-factor authentication is the only part that is not automated.
