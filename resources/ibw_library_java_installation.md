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

<https://www.sslsupportdesk.com/how-to-enable-or-disable-all-puposes-of-root-certificates-in-mmc/>
<https://support.sonatype.com/hc/en-us/articles/213465768-SSL-Certificate-Guide>
<https://blog.behrang.org/2018/12/04/connecting-to-self-signed-https-java.html>
<https://www.sslshopper.com/article-how-to-create-a-self-signed-certificate-using-java-keytool.html>
<C:\Program Files\RedHat\java-1.8.0-openjdk-1.8.0.232-3\jre\bin>

```console
keytool -delete -noprompt -alias selfsigned -keystore interactivebrokercert.jks -storepass mypassword
```

```console
keytool -genkey -keystore interactivebrokercert.jks -keypass mypassword -storepass mypassword -alias selfsigned -keyalg RSA -keysize 4096 -validity 5000 -dname "CN=localhost:5000, OU=Web, O=Sigma Coding, L=San Diego, ST=CA, C=US"
```

<!-- keytool -importkeystore -srckeystore interactivebrokercert.jks -destkeystore interactivebrokercert.jks -deststoretype pkcs12
keytool -importkeystore -srckeystore interactivebrokercertsigma.jks -destkeystore interactivebrokercertsigma.jks -deststoretype pkcs12
keytool -genkey -keyalg RSA -alias selfsigned -keystore interactivebrokercert.jks -storepass password -validity 360 -keysize 2048
keytool -genkey -keyalg RSA -alias selfsigned -keystore interactivebrokercertsigma.jks -storepass password -validity 360 -keysize 2048 -ext SAN=dns:localhost
keytool -genkeypair -keystore interactivebrokercert.jks -keypass mypassword -storepass mypassword -alias selfsigned -keyalg RSA -keysize 4096 -validity 5000 -dname "CN=localhost, OU=Web, O=Sigma Coding, L=San Diego, ST=CA, C=US"

Warning:
The JKS keystore uses a proprietary format. It is recommended to migrate to PKCS12 which is an industry standard format using "keytool -importkeystore -srckeystore interactivebrokercert.jks -destkeystore interactivebrokercert.jks -deststoretype pkcs12" -->
