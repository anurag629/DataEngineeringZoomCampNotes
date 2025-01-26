---

### **Introduction to Kestra**

**Kestra Overview**:
- **Kestra**: An event-driven data orchestration platform designed for simplicity and flexibility.
- Suitable for all types of workflows and pipelines.
- Key features:
  - **Intuitive Interface**.
  - **Extensive Plugin Support**.
  - **Workflow Customization** through YAML-based definitions.

---

### **Setup and Installation**

1. **Run Kestra Using Docker**:
   - Use the following command to start Kestra quickly:
     ```bash
     docker run --pull=always --rm -it -p 8080:8080 --user=root -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp kestra/kestra:latest server local
     ```
   - Navigate to `http://localhost:8080` to access the Kestra web interface.

2. **Kestra Workflow Structure**:
   - **Flows**: YAML-based workflows with three main components:
     - **ID**: Unique identifier for the workflow.
     - **Namespace**: Logical grouping or environment (e.g., dev, prod).
     - **Tasks**: Define individual steps in the workflow.

   Example:
   ```yaml
   id: getting-started
   namespace: example
   tasks:
     - id: log-task
       type: io.kestra.core.tasks.debugs.Log
       message: "Hello Kestra!"
   ```

---

### **Core Concepts**

1. **Inputs**:
   - Define constants or parameters for reuse across tasks.
   - Example:
     ```yaml
     inputs:
       - id: github_repo
         type: STRING
         default: "kestra-io/kestra"
     ```

2. **Outputs**:
   - Tasks can generate outputs for use in subsequent tasks.
   - Example:
     ```python
     import kestra
     kestra.outputs({"result": 123})
     ```

3. **Triggers**:
   - Automate workflow execution based on conditions (e.g., schedules or webhooks).
   - Example:
     ```yaml
     triggers:
       - id: hourly-trigger
         type: io.kestra.core.triggers.schedules.Schedule
         cron: "0 * * * *"
     ```

---

### **Building Your First Workflow**

**Objective**:
- Fetch GitHub repository stars every hour and send the count to a Discord channel.

1. **Create the Python Script**:
   - Write a Python script to fetch GitHub stars using the requests library:
     ```python
     import requests
     response = requests.get("https://api.github.com/repos/kestra-io/kestra")
     gh_stars = response.json()["stargazers_count"]
     print(gh_stars)
     ```

2. **Integrate the Script into Kestra**:
   - Define a task to execute the Python script:
     ```yaml
     tasks:
       - id: python-task
         type: io.kestra.core.tasks.scripts.Bash
         beforeCommands:
           - python3 -m venv .venv
           - source .venv/bin/activate
           - pip install -r requirements.txt
         commands:
           - python /path/to/api_example.py
     ```

3. **Enhance the Python Script for Outputs**:
   - Install and use the Kestra library for returning results:
     ```python
     import kestra
     import requests

     response = requests.get("https://api.github.com/repos/kestra-io/kestra")
     gh_stars = response.json()["stargazers_count"]
     kestra.outputs({"github_stars": gh_stars})
     ```

   - Reference the output in Kestra:
     ```yaml
     tasks:
       - id: log-stars
         type: io.kestra.core.tasks.debugs.Log
         message: "GitHub stars: {{ outputs.python-task.github_stars }}"
     ```

4. **Send Discord Notifications**:
   - Add a Discord task to notify the number of stars:
     ```yaml
     tasks:
       - id: discord-notification
         type: io.kestra.plugin.notifications.discord
         webhookUrl: "YOUR_DISCORD_WEBHOOK_URL"
         content: "GitHub stars: {{ outputs.python-task.github_stars }}"
     ```

---

### **Advanced Configuration**

1. **Using Inputs for Reusability**:
   - Define inputs for dynamic values:
     ```yaml
     inputs:
       - id: discord_webhook_url
         type: STRING
         default: "YOUR_DISCORD_WEBHOOK_URL"
     ```

   - Reference inputs:
     ```yaml
     webhookUrl: "{{ inputs.discord_webhook_url }}"
     ```

2. **Adding a Trigger**:
   - Schedule the workflow to run hourly:
     ```yaml
     triggers:
       - id: hourly-trigger
         type: io.kestra.core.triggers.schedules.Schedule
         cron: "0 * * * *"
     ```

---

### **Execution and Testing**

1. **Testing the Workflow**:
   - Use the **Execute** button in the top-right corner of the Kestra interface to test manually.
   - Check the logs for task execution details and outputs.

2. **Viewing Logs**:
   - Inspect logs for:
     - Installation of dependencies.
     - Execution results (e.g., number of GitHub stars).

3. **Verifying Discord Notification**:
   - Confirm that the Discord channel receives the notification with the star count.

4. **Automated Triggers**:
   - Once saved, triggers become active automatically.
   - To disable, add:
     ```yaml
     triggers:
       - id: hourly-trigger
         type: io.kestra.core.triggers.schedules.Schedule
         cron: "0 * * * *"
         disabled: true
     ```

---

### **Best Practices**

1. **Namespace Separation**:
   - Use namespaces to differentiate between environments (e.g., dev, staging, prod).

2. **Use Inputs and Outputs**:
   - Define reusable parameters with inputs.
   - Use outputs to pass data between tasks.

3. **Debugging**:
   - Use log tasks to inspect intermediate results.

4. **Triggers**:
   - Automate workflows using schedules or event-based triggers.

---

### **Conclusion**

With Kestra:
- You can orchestrate workflows efficiently with YAML-based definitions.
- It supports various use cases through its plugins, including scripting, notifications, and integrations.
- Automating repetitive tasks becomes seamless, enhancing productivity and reliability.