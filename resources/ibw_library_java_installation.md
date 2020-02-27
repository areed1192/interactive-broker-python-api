# Installing OpenJDK with the MSI Installer

To install OpenJDK 8 for Windows using the MSI-based installer:

1. Download the [MSI-based](https://developers.redhat.com/products/openjdk/download) installer of OpenJDK 8 for Windows for your architecture.
2. Run the installer and follow the on-screen instructions to install `OpenJDK 8` for Windows and the desired extra components.

The `%JAVA_HOME%` environment variable must also be set to use some developer tools.
Set the `%JAVA_HOME%` environment variable as follows:

1. Open Command Prompt as an administrator.
2. Set the value of the environment variable to your OpenJDK 8 for Windows installation path:

    ```console
    C:\> setx /m JAVA_HOME "C:\Progra~1\RedHat\java-1.8.0-openjdk-1.8.0.181-1"
    ```

    - If the path contains spaces, use the shortened path name.
3. Restart Command Prompt to reload the environment variables.
