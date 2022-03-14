# Mitchell Long
## Strava Data Analysis

---

### Basic Idea

This project is intended to observe some of your personal strava stats and allow for simple data analysis.

This project will walk you through setting up this interface to interact with this data.

---

### Instructions
1. Go to ```https://www.strava.com/settings/api``` and sign in.

2. Create a new application here and remember the credentials

    Within the project directory create a new file called *.env*. Within this file we will put your Api credentials.

    Put the following into the file:

    ```bash
    CLIENT_ID=[YOUR_CLIENT_ID]
    CLIENT_SECRET=[YOUR_CLIENT_SECRET]
    ```

    ****Note**: You will not need to add quotes around the variables

3. Go to the following url (albeit replace **[REPLACE_WITH_YOUR_CLIENT_ID]** with your client_id from the credentials in the second step)
    
    `http://www.strava.com/oauth/authorize?client_id=`**[REPLACE_WITH_YOUR_CLIENT_ID]**`&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all`

    On this page click *Authorize* to allow the Api to view and distribute your data.

    This will redirect you to another page with a url matching:

    `http://localhost/exchange_token?state=&code=`**[THIS_IS_THE_CODE_YOU_NEED_TO_COPY]**`&scope=read,activity:read_all,profile:read_all`

    Copy down the **[THIS_IS_THE_CODE_YOU_NEED_TO_COPY]** portion.

4. Open up a terminal or powershell, move into the project directory and run the following commands
```bash
python -m pip install -r requirements.txt
python initialSetup.py **[THIS_IS_THE_CODE_YOU_NEED_TO_COPY]**
python app.py
```

5. Open up your browser and visit localhost:8050

****Note**: This process can be repeated if the refresh_token doesn't work for whatever reason

---

### Credits

The requests for the strava api and all related logic was published [here](https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86) by [Benji Knights Johnson](https://medium.com/@benjikj).
