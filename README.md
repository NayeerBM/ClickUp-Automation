# ClickUp-Automation

## Running the Program

**NOTE: ENSURE THAT GOOGLE CHROME AND PYTHON ARE INSTALLED**

1. Clone the project.
2. Fill up `config.json` with all the relevant information as below:

    ```python
    {
      "name": "Nayeer", #Must me same as name in ClickUp
      "email": "",
      "password": "", #as of now no encryption, becareful not to share password with anyone
      "location":"Office", #Office/Home/On Site
      "health level":5,
      "tasks": ["1. ISEM 10 Development", "2. ISEM X bug fixes"]
    }
    ```
 3. Open Command Prompt or any equivalent shell in the root project directory.
 4. Run the command **`python main.py checkin`** to check into Click Up or **`python main.py checkout`** to check out of Click Up.
 
## TODO

### Features to add to project:

- [ ] Create a script for encrypting password and storing into config.json
- [ ] Create a script for decrypting password from config.json
- [ ] Add command line arguments for executing script with tasks (e.g. `python main.py tasks 1.Completed task A`)
