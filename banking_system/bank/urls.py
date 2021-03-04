from django.urls import path
from .views import UserAPI, Deposit, Withdraw, Enquiry, DownloadTransaction

urlpatterns = [
    path("user/", UserAPI.as_view()),
    path("deposit/", Deposit.as_view()),
    path("withdraw/", Withdraw.as_view()),
    path("enquiry/", Enquiry.as_view()),
    path("download-transaction-record/", DownloadTransaction.as_view()),
]
