from ibc.session import InteractiveBrokersSession


class Data():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Data` client.

        ### Parameters
        ----
        ib_client : object
            The `InteractiveBrokersClient` Python Client.

        ib_session : InteractiveBrokersSession
            The IB session handler.
        """

        from ibc.client import InteractiveBrokersClient

        self.client: InteractiveBrokersClient = ib_client
        self.session: InteractiveBrokersSession = ib_session

    def portfolio_news(self) -> dict:
        """Returns a news summary for your portfolio.

        ### Returns
        ----
        list:
            A collection of `NewsArticle` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.portfolio_news()
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/news/portfolio'
        )

        return content

    def top_news(self) -> dict:
        """Returns the top news articles.

        ### Returns
        ----
        list:
            A collection of `NewsArticle` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.top_news()
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/news/top'
        )

        return content

    def news_sources(self) -> dict:
        """Returns news sources.

        ### Returns
        ----
        list:
            A collection of `Sources` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.news_sources()
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/news/top'
        )

        return content

    def news_briefings(self) -> dict:
        """Returns news briefings.

        ### Returns
        ----
        list:
            A collection of `Briefings` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.news_briefings()
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/news/briefing'
        )

        return content

    def summary(self, contract_id: str) -> dict:
        """Returns a summary of the contract ID, items include
        company description and more.

        ### Parameters
        ----
        contract_id : str
            The contract Id you want to query.

        ### Returns
        ----
        list:
            A collection of `Summary` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.summary(
                contract_id='265598'
            )
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/fundamentals/{contract_id}/summary'
        )

        return content
