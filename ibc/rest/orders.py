from typing import Union
from ibc.session import InteractiveBrokersSession


class Orders():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Orders` client.

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

    def orders(self) -> dict:
        """The end-point is meant to be used in polling mode, e.g. requesting 
        every x seconds.

        ### Overview
        ----
        The response will contain two objects, one is notification,
        the other is orders. Orders is the list of orders (cancelled,
        filled, submitted) with activity in the current day. Notifications
        contains information about execute orders as they happen, see
        status field.

        ### Returns
        ----
        dict: 
            A collection of `Order` resources.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.orders()
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/account/orders'
        )

        return content

    def place_order(self, account_id: str, order: dict) -> dict:
        """Places an order.

        ### Overview
        ----
        Please note here, sometimes this end-point alone can’t make sure
        you submit the order successfully, you could receive some questions
        in the response, you have to to answer them in order to submit the order
        successfully. You can use `/iserver/reply/{replyid}` end-point to answer
        questions.

        ### Parameters
        ----
        account_id : str
            The account you want the order placed on.

        order : dict
            The order payload.

        ### Returns
        ----
        dict: 
            A `Reply` resource or a `Order` resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.place_order(
                account_id=ibc_client.account_number,
                order={
                    "conid": 251962528,
                    "secType": "362673777:STK",
                    "cOID": "limit-buy-order-1",
                    "orderType": "LMT",
                    "price": 5.00,
                    "side": "BUY",
                    "quantity": 1,
                    "tif": "DAY"
                }
            )
        """

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/iserver/account/{account_id}/order',
            json_payload=order
        )

        return content

    def place_bracket_order(self, account_id: str, orders: dict) -> dict:
        """Places multiple orders at once.

        ### Parameters
        ----
        account_id : str
            The account you want the orders placed on.

        orders : dict
            The orders payload.

        ### Returns
        ----
        dict: 
            A `Reply` resource or a `Order` resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.place_bracket_order(
                account_id=ibc_client.account_number,
                order={
                    "orders": [
                        {
                            "conid": 251962528,
                            "secType": "362673777:FUT",
                            "cOID": "buy-1",
                            "orderType": "LMT",
                            "side": "BUY",
                            "price": 9.00,
                            "quantity": 1,
                            "tif": "DAY"
                        },
                        {
                            "conid": 251962528,
                            "secType": "362673777:STK",
                            # This MUST match the `cOID` of the first order.
                            "parentId": "buy-1",
                            "orderType": "LMT",
                            "side": "BUY",
                            "price": 7.00,
                            "quantity": 2,
                            "tif": "DAY"
                        }
                    ]
                }
            )
        """

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/iserver/account/{account_id}/orders',
            json_payload=orders
        )

        return content

    def modify_order(self, account_id: str, order_id: str, order: dict) -> dict:
        """Modifies an open order.

        ### Overview
        ----
        The `/iserver/accounts` endpoint must first be called.

        ### Parameters
        ----
        account_id : str
            The account which has the order you want to be
            modified.

        order_id : str
            The id of the order you want to be modified.

        order : dict
            The new order payload.

        ### Returns
        ----
        dict: 
            A `Reply` resource or a `Order` resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.modify_order(
                account_id=ibc_client.account_number,
                order_id='1915650539',
                order={
                    "conid": 251962528,
                    "secType": "362673777:STK",
                    "cOID": "limit-buy-order-1",
                    "orderType": "LMT",
                    "price": 5.00,
                    "side": "BUY",
                    "quantity": 1,
                    "tif": "DAY"
                }
            )
        """

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/iserver/account/{account_id}/order',
            json_payload=order
        )

        return content

    def delete_order(self, account_id: str, order_id: str) -> Union[list, dict]:
        """Deletes an order.

        ### Parameters
        ----
        account_id : str
            The account that contains the order you want to
            delete.

        order_id : str
            The id of the order you want to delete.

        ### Returns
        ----
        Union[list, dict]: 
            A `OrderResponse` resource or a collection of them.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.delete_order(
                account_id=ibc_client.account_number,
                order_id=
            )
        """

        content = self.session.make_request(
            method='delete',
            endpoint=f'/api/iserver/account/{account_id}/order/{order_id}'
        )

        return content

    def place_whatif_order(self, account_id: str, order: dict) -> dict:
        """This end-point allows you to preview order without actually
        submitting the order and you can get commission information in
        the response.

        ### Parameters
        ----
        account_id : str
            The account you want the order placed on.

        order : dict
            The order payload.

        ### Returns
        ----
        dict: 
            A `OrderCommission` resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.place_whatif_order(
                account_id=ibc_client.account_number,
                order={
                    "conid": 251962528,
                    "secType": "362673777:STK",
                    "cOID": "limit-buy-order-1",
                    "orderType": "LMT",
                    "price": 5.00,
                    "side": "BUY",
                    "quantity": 1,
                    "tif": "DAY"
                }
            )
        """

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/iserver/account/{account_id}/order/whatif',
            json_payload=order
        )

        return content

    def reply(self, reply_id: str, message: dict) -> Union[list, dict]:
        """Reply to questions when placing orders and submit orders.

        ### Parameters
        ----
        reply_id : str
            The `ID` from the response of `Place Order` end-point

        message : dict
            The answer to question.

        ### Returns
        ----
        Union[list, dict]: 
            A list when the order is submitted, a dictionary
            with an error message if not confirmed.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.reply(
                reply_id='5050c104-1276-4483-8be8-ca598e698766',
                message={
                    "confirmed": True
                }
            )
        """

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/iserver/reply/{reply_id}',
            json_payload=message
        )

        return content
