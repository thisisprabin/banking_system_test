import os
import decimal
import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utility.json_schema import JsonSchemaValidator
from utility.constant import (
    INPUT_VAL_ERR,
    USER_ADD_SUCCESS,
    SCHEMA_ADD_USER,
    DATA_FETCH_SUCCESS,
    DEPOSIT,
    WITHDRAW,
    DEPOSIT_SUCCESS,
    USER_NOT_EXISTS,
    ACCOUNT_NOT_EXISTS,
    INSUFFICIENT_WITHDRAW_AMOUNT,
    WITHDRAW_SUCCESS,
    ENQUIRY,
    SCHEMA_DEPOSIT_WITHDRAW,
    SCHEMA_ENQUIRY,
    EMAIL_ID_ALREADY_EXISTS,
    AMOUNT_WITHDRAW_MSG,
    AMOUNT_DEPOSIT_MSG,
    COMMON_SERVER_ERR,
    SCHEMA_DOWNLOAD_TRANS,
)
from bank.models import User, Account, Transaction
from bank.serializer import UserSerializer
from utility.utility import get_time, datetime_to_epoch
from django.conf import settings
from django.core.mail import send_mail


__all__ = ["UserAPI", "Deposit", "Withdraw", "Enquiry", "DownloadTransaction"]


class UserAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        response_data = {
            "success": None,
            "message": None,
            "error_details": [],
            "data": None,
        }

        try:

            data = User.objects.filter(is_active=True)
            se_data = UserSerializer(data, many=True)

            response_data.update(
                {"success": True, "message": DATA_FETCH_SUCCESS, "data": se_data.data}
            )
            response = Response(data=response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response_data.update({"success": False, "message": COMMON_SERVER_ERR})
            response = Response(
                data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response

    def post(self, request):

        response_data = {
            "success": None,
            "message": None,
            "error_details": [],
            "data": None,
        }

        try:

            data = request.data
            errors = JsonSchemaValidator.validate(instance=data, schema=SCHEMA_ADD_USER)

            if not errors:

                if not User.objects.filter(
                    email_id__iexact=data.get("email_id"), is_active=True
                ).exists():

                    user = User.objects.create(**data)
                    _ac_data = {
                        "account_number": datetime_to_epoch(date_time=get_time()),
                        "user": user,
                    }
                    Account.objects.create(**_ac_data)

                    response_data.update(
                        {
                            "success": True,
                            "message": USER_ADD_SUCCESS,
                        }
                    )
                    response = Response(
                        data=response_data, status=status.HTTP_201_CREATED
                    )
                else:
                    response_data.update(
                        {
                            "success": False,
                            "message": EMAIL_ID_ALREADY_EXISTS,
                        }
                    )
                    response = Response(
                        data=response_data, status=status.HTTP_409_CONFLICT
                    )
            else:
                error_details = [{"error": e} for e in errors]
                response_data.update(
                    {
                        "success": False,
                        "message": INPUT_VAL_ERR,
                        "error_details": error_details,
                    }
                )
                response = Response(
                    data=response_data, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            response_data.update({"success": False, "message": COMMON_SERVER_ERR})
            response = Response(
                data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class Deposit(APIView):
    def post(self, request):
        response_data = {
            "success": None,
            "message": None,
            "error_details": [],
            "data": None,
        }

        try:

            data = request.data
            errors = JsonSchemaValidator.validate(
                instance=data, schema=SCHEMA_DEPOSIT_WITHDRAW
            )

            if not errors:

                user = User.objects.filter(pk=data.get("user_id"), is_active=True)
                account = Account.objects.filter(
                    account_number=data.get("account_number"), is_active=True
                )

                if user.exists() and account.exists():
                    user = user[0]
                    account = account[0]

                    account.amount += decimal.Decimal(str(data.get("amount")))
                    account.save()

                    now = get_time()

                    t_data = {
                        "user": user,
                        "account": account,
                        "amount": data.get("amount"),
                        "operation": DEPOSIT,
                        "transaction_date": now,
                    }

                    Transaction.objects.create(**t_data)

                    msg = AMOUNT_DEPOSIT_MSG.format(
                        data.get("amount"),
                        account.account_number,
                        now.strftime("%d %B %Y, %H:%M:%S"),
                    )
                    subject = "Bank alert"
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [
                        user.email_id,
                    ]
                    send_mail(subject, msg, email_from, recipient_list)

                    response_data.update({"success": True, "message": DEPOSIT_SUCCESS})
                    response = Response(data=response_data, status=status.HTTP_200_OK)
                else:
                    if not user.exists():
                        response_data.update(
                            {"success": False, "message": USER_NOT_EXISTS}
                        )
                        response = Response(
                            data=response_data, status=status.HTTP_404_NOT_FOUND
                        )
                    else:
                        response_data.update(
                            {"success": False, "message": ACCOUNT_NOT_EXISTS}
                        )
                        response = Response(
                            data=response_data, status=status.HTTP_404_NOT_FOUND
                        )
            else:
                error_details = [{"error": e} for e in errors]
                response_data.update(
                    {
                        "success": False,
                        "message": INPUT_VAL_ERR,
                        "error_details": error_details,
                    }
                )
                response = Response(
                    data=response_data, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            response_data.update({"success": False, "message": COMMON_SERVER_ERR})
            response = Response(
                data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response


class Withdraw(APIView):
    def post(self, request):
        response_data = {
            "success": None,
            "message": None,
            "error_details": [],
            "data": None,
        }

        try:
            data = request.data
            errors = JsonSchemaValidator.validate(
                instance=data, schema=SCHEMA_DEPOSIT_WITHDRAW
            )

            if not errors:

                user = User.objects.filter(pk=data.get("user_id"), is_active=True)
                account = Account.objects.filter(
                    account_number=data.get("account_number"), is_active=True
                )

                if user.exists() and account.exists():
                    user = user[0]
                    account = account[0]

                    if account.amount >= data.get("amount"):
                        account.amount -= decimal.Decimal(str(data.get("amount")))
                        account.save()
                        now = get_time()
                        t_data = {
                            "user": user,
                            "account": account,
                            "amount": data.get("amount"),
                            "operation": WITHDRAW,
                            "transaction_date": now,
                        }

                        Transaction.objects.create(**t_data)

                        msg = AMOUNT_WITHDRAW_MSG.format(
                            data.get("amount"),
                            account.account_number,
                            now.strftime("%d %B %Y, %H:%M:%S"),
                        )
                        subject = "Bank alert"
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [
                            user.email_id,
                        ]
                        send_mail(subject, msg, email_from, recipient_list)

                        response_data.update(
                            {"success": True, "message": WITHDRAW_SUCCESS}
                        )
                        response = Response(
                            data=response_data, status=status.HTTP_200_OK
                        )
                    else:
                        response_data.update(
                            {"success": False, "message": INSUFFICIENT_WITHDRAW_AMOUNT}
                        )
                        response = Response(
                            data=response_data, status=status.HTTP_406_NOT_ACCEPTABLE
                        )
                else:
                    if not user.exists():
                        response_data.update(
                            {"success": False, "message": USER_NOT_EXISTS}
                        )
                        response = Response(
                            data=response_data, status=status.HTTP_404_NOT_FOUND
                        )
                    else:
                        response_data.update(
                            {"success": False, "message": ACCOUNT_NOT_EXISTS}
                        )
                        response = Response(
                            data=response_data, status=status.HTTP_404_NOT_FOUND
                        )
            else:
                error_details = [{"error": e} for e in errors]
                response_data.update(
                    {
                        "success": False,
                        "message": INPUT_VAL_ERR,
                        "error_details": error_details,
                    }
                )
                response = Response(
                    data=response_data, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            response_data.update({"success": False, "message": COMMON_SERVER_ERR})
            response = Response(
                data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class Enquiry(APIView):
    def post(self, request):
        response_data = {
            "success": None,
            "message": None,
            "error_details": [],
            "data": None,
        }

        try:

            data = request.data
            errors = JsonSchemaValidator.validate(instance=data, schema=SCHEMA_ENQUIRY)

            if not errors:

                user = User.objects.filter(pk=data.get("user_id"), is_active=True)
                account = Account.objects.filter(
                    account_number=data.get("account_number"), is_active=True
                )

                if user.exists() and account.exists():
                    user = user[0]
                    account = account[0]

                    _data = {"amount": account.amount}

                    t_data = {
                        "user": user,
                        "account": account,
                        "amount": account.amount,
                        "operation": ENQUIRY,
                        "transaction_date": get_time(),
                    }

                    Transaction.objects.create(**t_data)

                    response_data.update(
                        {"success": True, "message": DATA_FETCH_SUCCESS, "data": _data}
                    )
                    response = Response(data=response_data, status=status.HTTP_200_OK)
                else:
                    if not user.exists():
                        response_data.update(
                            {"success": False, "message": USER_NOT_EXISTS}
                        )
                        response = Response(
                            data=response_data, status=status.HTTP_404_NOT_FOUND
                        )
                    else:
                        response_data.update(
                            {"success": False, "message": ACCOUNT_NOT_EXISTS}
                        )
                        response = Response(
                            data=response_data, status=status.HTTP_404_NOT_FOUND
                        )
            else:
                error_details = [{"error": e} for e in errors]
                response_data.update(
                    {
                        "success": False,
                        "message": INPUT_VAL_ERR,
                        "error_details": error_details,
                    }
                )
                response = Response(
                    data=response_data, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            response_data.update({"success": False, "message": COMMON_SERVER_ERR})
            response = Response(
                data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class DownloadTransaction(APIView):
    def post(self, request):
        response_data = {
            "success": None,
            "message": None,
            "error_details": [],
            "data": None,
        }

        try:

            data = request.data
            errors = JsonSchemaValidator.validate(
                instance=data, schema=SCHEMA_DOWNLOAD_TRANS
            )

            trans_ops = {WITHDRAW: "Withdraw", DEPOSIT: "Deposit"}

            if not errors:
                account = Account.objects.filter(
                    account_number=data.get("account_number"), is_active=True
                )

                if account.exists():
                    account = account[0]
                    _info = []
                    for t in (
                        Transaction.objects.filter(
                            account=account,
                            is_active=True,
                            operation__in=[DEPOSIT, WITHDRAW],
                        )
                        .values("transaction_date", "amount", "operation")
                        .order_by("transaction_date")
                    ):
                        _info.append(
                            {
                                "Transaction Date": t.get("transaction_date").strftime(
                                    "%d/%m/%Y, %H:%M:%S"
                                ),
                                "Amount": str(t.get("amount")),
                                "Operation": trans_ops.get(t.get("operation")),
                            }
                        )

                    now = datetime_to_epoch(date_time=get_time())
                    file_name = "{}_{}.xlsx".format(account.account_number, now)
                    path = os.path.join(settings.TRANS_RECD_FILE_DIR_PATH, file_name)

                    df = pd.DataFrame(_info)
                    df.to_excel(path)

                    url = {
                        "url": "{}/{}".format(settings.TRANS_RECD_FILE_URL, file_name)
                    }

                    response_data.update(
                        {"success": True, "message": DATA_FETCH_SUCCESS, "data": url}
                    )
                    response = Response(data=response_data, status=status.HTTP_200_OK)
                else:
                    response_data.update(
                        {"success": False, "message": ACCOUNT_NOT_EXISTS}
                    )
                    response = Response(
                        data=response_data, status=status.HTTP_404_NOT_FOUND
                    )
            else:
                error_details = [{"error": e} for e in errors]
                response_data.update(
                    {
                        "success": False,
                        "message": INPUT_VAL_ERR,
                        "error_details": error_details,
                    }
                )
                response = Response(
                    data=response_data, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            response_data.update({"success": False, "message": COMMON_SERVER_ERR})
            response = Response(
                data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response
