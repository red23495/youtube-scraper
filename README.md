# Instructions for running the application

The application requires mysql and redis databases to work properly. 
Make sure you have these 2 installed in your environment.

To run the application:
- install all the dependencies from requirements.txt file. The command for that is - `pip install -r requirements.txt`.
- configure the following environment variables. You can also set them from a `.env` file.
 A sample file is provided in the project named `.env.sample`.
  - `DB_NAME` - Name of the mysql database
  - `DB_HOST` - Host of mysql database (default localhost)
  - `DB_PORT` - Port of mysql database (default 3306)
  - `DB_USER` - Username of the user for mysql server
  - `DB_PASSWORD` - Password of the user for mysql server
  - `API_KEY` - Google API key, used for scraping video data
  - `REDIS_URL` - URL of redis server, used for scheduler (default `redis://localhost:6379`)
- Run all django migrations by running the command `python manage.py migrate`
- The application requires the user to configure youtube channel information from a Django Admin page. 
So you need to create a admin user to access admin panel. To create admin user run the command - 
`python manage.py createsuperuser`.
- Start the application by running command `python manage.py runserver`.

### configuring channel
After running the application, go to the url `/admin/`. 
Use the admin credentials in this page to access admin panel.
Then go to url `/admin/scrapper/channel/add/`. A form page will appear. 
Enter channel id in channel id field and click save.
Now this channel is ready for scraping.

### running the scheduler
The actual scraping is done by a celery task. To run the scheduler, go to `youtube_scrapper`,
where the `celery.py` file is located. 
You need to run the following two commands to start the scheduler

`celery -A youtube_scrapper beat -l info --logfile=celery.beat.log`

`celery -A youtube_scrapper worker -l info --logfile=celery.log --pool=solo`

The scheduler will now scap channel videos every 20 minutes.

**Note:** The given commands will not run celery in daemon mode. To run scheduler in daemon mode,
you can run the command using `--daemon` flag. For more information, check out celery official documentation.

#Development
To run unit tests, run the command `python manage.py test`.