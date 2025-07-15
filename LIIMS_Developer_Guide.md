
## The Longevity India LIMS: A Developer's Guide to Your Custom OpenSpecimen

### Part 1: How It All Works - The OpenSpecimen Ecosystem

To develop effectively, it's crucial to understand the different components and how they interact. Think of it as a complete system with specialized parts.

*   **The Application Server (`Apache Tomcat`):** This is the "engine" that runs your Java code. It's a container for your application, handling web requests, managing resources, and serving pages to users. We installed it at `/opt/tomcat9`.

*   **The Database (`MySQL in Docker`):** This is the system's long-term memory. It stores every piece of data: participant details, specimen information, user accounts, etc.
    *   **Why Docker?** We run MySQL in a Docker container to isolate it from the host operating system. This provides a perfectly configured, stable, and repeatable database environment, protecting us from the system-level package and configuration issues we encountered.

*   **The Application Code (`openspecimen.war`):** This is the core product—the "brains" of the operation. It's a single file that contains:
    *   **The Backend (Java):** All the server-side logic, business rules, and database interactions.
    *   **The Frontend (JavaScript/HTML/CSS):** Everything the user sees and interacts with in their browser.

*   **The Build System (`Gradle`):** This is your "factory." It takes all your source code (both Java and JavaScript), compiles it, packages it, and produces the final `openspecimen.war` file, ready for deployment. We always use the **Gradle Wrapper (`./gradlew`)** to ensure we use the exact version (7.5.1) the project requires.

### Part 2: Understanding the Configuration

Your entire system is controlled by a few key configuration files. Knowing their roles is critical for troubleshooting.

| File Name                    | Location                                | Purpose                                                                                                                        |
| :--------------------------- | :-------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **`build.properties`**       | `~/openspecimen/`                       | **Build-Time Config:** Tells Gradle where your Tomcat server is located. The `deploy` task uses this to know where to copy files. |
| **`openspecimen.xml`**       | `/opt/tomcat9/conf/Catalina/localhost/` | **Tomcat Config:** Defines the database connection pool (URL, username, password) and gives it a JNDI name (`jdbc/openspecimen`). |
| **`openspecimen.properties`**| `/opt/tomcat9/conf/`                    | **Application Config:** Tells the running OpenSpecimen application how to find its data directory and which JNDI name to use for the database. |
| **`.vscode/settings.json`**  | `~/openspecimen/`                       | **IDE Config:** Forces VS Code to use the correct Java version (17) and the Gradle Wrapper for this specific project.          |

### Part 3: The Core Development Workflow

This is the cycle you will repeat every time you make changes.

1.  **Make Your Code Changes:** Use VS Code to edit the Java, HTML, or other files in your `~/openspecimen` directory.

2.  **Build the Application:** Use the integrated terminal in VS Code for this step. This compiles your code and creates the `.war` file.
    ```bash
    # Make sure you are in the project's root directory: ~/openspecimen
    ./gradlew clean deploy
    ```
    Always wait for the **`BUILD SUCCESSFUL`** message. If it fails, the error message will tell you which file has a syntax error.

3.  **Deploy the Application:** The `deploy` task does *not* automatically copy the file. You must do it manually.
    ```bash
    # This copies the newly built file to your server's webapps directory
    sudo cp build/libs/openspecimen.war /opt/tomcat9/webapps/
    ```

4.  **Run the New Version:** Restart the Tomcat server to make it load your new code.
    ```bash
    sudo systemctl restart tomcat
    ```
    Wait about 30-60 seconds for the server to fully start.

5.  **Test in Your Browser:**
    *   Open `http://localhost:8082/openspecimen`.
    *   Perform a **Hard Refresh** (**Ctrl+Shift+R** or **Cmd+Shift+R**) to ensure you are seeing the latest changes.

### Part 4: Saving Your Work - The Git Workflow

Your code lives in Git. Following this process ensures your work is safe, tracked, and shareable.

1.  **Check the Status:** See which files you have changed.
    ```bash
    git status
    ```

2.  **Stage Your Changes:** Tell Git which changes you want to include in your next save point.
    ```bash
    # To add a specific file
    git add path/to/your/file.java
    
    # To add all changed files (use with caution, but common)
    git add .
    ```

3.  **Commit Your Changes:** Save your staged changes with a descriptive message. This creates a permanent save point in your local history.
    ```bash
    git commit -m "feat: Add custom field for BHARAT Study baseline"
    # Or "fix: Corrected the title on the participant page"
    ```

4.  **Push Your Changes to GitHub:** Upload your new commits from your local machine to your GitHub fork (`origin`). This is your backup and how you share your work.
    ```bash
    # This pushes your 'longevity-india-dev' branch to your fork
    git push origin longevity-india-dev
    ```

### Part 5: System Administration & Troubleshooting

#### How to Start Everything After a System Reboot

Our setup is designed to be resilient. Here's what happens on a reboot and how to manage it:

1.  **Docker Service Starts:** The main Docker service starts automatically.
2.  **MySQL Container Starts:** Because we created the `openspecimen-mysql` container with the `--restart unless-stopped` policy, the Docker service will automatically start it.
3.  **Tomcat Service Starts:** Because we enabled the `tomcat.service` with `systemd`, it will also start automatically after the network and Docker are ready.

**Manual Control:**
*   **To check the status:** `docker ps` and `sudo systemctl status tomcat`
*   **To start/stop the database:** `docker stop openspecimen-mysql` and `docker start openspecimen-mysql`
*   **To start/stop the application:** `sudo systemctl stop tomcat` and `sudo systemctl start tomcat`

---

#### The Troubleshooting Bible

This covers every major error we encountered and how to solve it.

| Symptom / Error Message                                          | Diagnosis                                                                                                  | Solution                                                                                                           |
| :--------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| **`BUILD FAILED` ... `Unable to find local grunt`**                | Front-end JavaScript libraries are not installed locally.                                                  | `cd www`, run `npm install` and `bower install`, then `cd ..` and retry the build.                                 |
| **`BUILD FAILED`** with a Java syntax error                        | You have a typo or error in your custom Java code.                                                         | Read the error message to find the exact file and line number. Correct the code in your IDE and rebuild.         |
| **Application is inaccessible (404)** after a successful build.  | The `.war` file was built but not copied to the Tomcat `webapps` directory.                                  | Manually copy the file: `sudo cp build/libs/openspecimen.war /opt/tomcat9/webapps/`                                |
| **`SEVERE` ... `Address already in use`** on port **8005**         | A previous Tomcat process did not shut down correctly and is still running in the background.                | Find and stop the zombie process. The most direct way is `sudo killall -9 java`, then restart Tomcat.           |
| **`ERROR` ... `Could not resolve placeholder 'plugin.dir'`**       | The `plugin.dir` property is missing from `openspecimen.properties`.                                       | Edit `/opt/tomcat9/conf/openspecimen.properties` and add the line `plugin.dir=/opt/tomcat9/os-data/plugins`. |
| **`LOGIN FAILED` ... `AUTH_INVALID_CREDENTIALS`** on first login | The default `admin` user was not created correctly or is inactive in the database.                         | Log into the MySQL container and run the `INSERT ... ON DUPLICATE KEY UPDATE` command to reset the user and password. |
| **VS Code shows errors** or uses the wrong Java/Gradle version     | The IDE's internal cache is stale or its configuration is wrong.                                           | 1. Ensure `.vscode/settings.json` is forcing Java 17 and the Gradle Wrapper. 2. Run `> Java: Clean Workspace`. |
| **`./gradlew` command fails** for any reason                       | The Gradle cache might be corrupted by a different Java version.                                           | Close VS Code. Run `rm -rf ~/.gradle/caches` and `rm -rf .gradle`. Retry the command.                             |

This guide should serve as your primary reference for developing, deploying, and maintaining your custom LIMS solution for the Longevity India Initiative.