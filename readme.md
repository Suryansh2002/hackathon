# Virtual Personal Assistant Optimization

**This project was sent for Techfest Competition(Finals-27th Dec) [HackAI](https://techfest.org/competitions/hack-aI).**

## Project Details

**Your challenge is to create the Virtual Personal Assistant Optimization using [uAgent library](https://fetch.ai/docs), a tool that:**

Develop an agent that can manage and optimize personal schedules. The agent should intelligently handle appointments, set reminders, and suggest time management strategies based on user preferences and past behaviors.


## Our Approch to this Project

**You can add,remove and see your tasks via the virtual assistant but unlike the tradtional way to tasks in a simple scheduler , we have used the OPENAI to allow users to send simple engish messages and our code will extract the TASK-NAME , TASK-DESCRIPTION , TASK-TYPE(Appointment or Reminder) , START-TIME ,END-TIME(if provided) from the user's message.**

**This approach makes the assistant more easy for the user to use (Almost like a real assistant).
Communicate in easy english with the uagent**

## Setting up the Project

### Step 1. Prerequisites

- Make sure you have python installed in your system by running `python --version` on your terminal.

- Install poetry on your system by running
  ```
  pip install poetry
  ```

### Step 2. Cloning the Project

- Run the command on your terminal `git clone <repository_url>`

- Replace `<repository_url>` with the actual URL of the project's Git repository.

- Now navigate to the Project Directory by running `cd project_directory`

### Step 3. Creating a Virtual environment

- Inside the project directory, your should create a virtual environment using Poetry:

  ```
  poetry install
  ```

  This command reads the project's pyproject.toml file and sets up a virtual environment with the required dependencies.

- Now activate the poetry shell using the following command.

  ```
  poetry shell
  ```

### Step 4. Generating a MongoDb connection String to use in the .env file (Mentioned in the next point)

- Go to [MongoDb](https://www.mongodb.com/) and create a new account. Answer the basic questions and click on finish

- Choose M0 databse configuration.

- Make a username and password and click on create user

- Add a new IP Address `0.0.0.0/0` and click on create entry

- Click on create and close go the Overview.

- You will be taken to a overview page.

- Now click on Connect and click on drivers and select the driver "Python".

- Copy your connection string and Replace `<password>` with the password for the your account made in one of the above steps.


### Step 5. Setting up the .env file

- Create an account on [ChatGPT](https://platform.openai.com/docs/overview) and get an Api Key.

  **_How to get an API key from OPENAI-_**

  - Visit [ChatGPT](https://platform.openai.com/docs/overview) and create a new account or Sign-in to your account.

  - Select **API keys** and generate an API Key

  - Now copy the key.

  - For more queries visit [ChatGPT](https://platform.openai.com/docs/overview)

- Create a file in the project directory named `.env` and paste the following code in it.

  ```
  OPENAI_API_KEY="<your_api_key_here>"

  MONGODB_URL="<your_connection_string>"
  ```

- Replace `<your_api_key_here>` with your your api key

- Replace the `<your_connection_string>` with your mongodb connection string you generated in the last point

### Step 6. Run the main script

```
py src/main.py
```

Copy the agent address printed in the console.We are going to need it in step 7.

### Step 7.Set up the client script

Now that we have set up the integrations, we need to set up the client script to communicate with our assistant agent. 


### Step 8.Run the client script

```sh
py client.py
```
