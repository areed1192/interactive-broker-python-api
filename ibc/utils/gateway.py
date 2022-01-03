import io
import pathlib
import zipfile
import requests
import textwrap


class ClientPortalGateway():

    def __init__(self) -> None:
        """Initializes the client portal object. """

        self._resources_folder = pathlib.Path(__file__).parents[1].joinpath(
            'resources'
        ).resolve()

    def _make_resources_directory(self) -> bool:
        """Makes the resource folder if it doesn't exist.

        ### Returns
        ----
        bool:
            `True` if additional steps need to be executed.
            `False` otherwise.
        """

        if not self._resources_folder.exists():
            print("Gateway folder does not exists, downloading files...")
            self._resources_folder.mkdir(parents=True)
            return True
        else:
            return False

    def _download_client_portal(self) -> requests.Response:
        """Downloads the Client Portal from Interactive Brokers.

        ### Returns
        ----
        requests.Response:
            A response object with clientportal content.
        """

        # Request the Client Portal
        response = requests.get(
            url='https://download2.interactivebrokers.com/portal/clientportal.beta.gw.zip'
        )

        return response

    def _create_zip_file(self, response_content: requests.Response) -> zipfile.ZipFile:
        """Creates a zip file to house the client portal content.

        ### Parameters
        ----
        response_content: requests.Response
            The response object with the client portal content.

        ### Returns
        ----
        zipfile.ZipFile:
            A zip file object with the Client Portal.
        """

        # Download the Zip File.
        zip_file_content = zipfile.ZipFile(
            io.BytesIO(response_content.content)
        )

        return zip_file_content

    def _extract_zip_file(self, zip_file: zipfile.ZipFile) -> None:
        """Extracts the Zip File.

        ### Parameters
        ----
        zip_file: zipfile.ZipFile:
            The client portal zip file to be extracted.
        """

        # Extract the Content to the new folder.
        zip_file.extractall(path="ibc/resources/clientportal.beta.gw")

    def setup(self) -> None:
        """Downloads and extracts the client portal object."""

        # Make the resource directory if needed.
        if self._make_resources_directory() == False:
            return

        # Download it.
        client_portal_response = self._download_client_portal()

        # Create a zip file.
        client_portal_zip = self._create_zip_file(
            response_content=client_portal_response
        )
        print("Zip folder created...")

        # Extract it.
        self._extract_zip_file(zip_file=client_portal_zip)
        print(textwrap.dedent(f"""Files extracted...
        New Folder is: {self._resources_folder}
        """))
