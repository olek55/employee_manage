from django.shortcuts import render


# Create your views here.
def partner_adds_service(partner_id, user_id):
    url = "https://hook.eu2.make.com/84o8ypdukl3dsc4jus9anb546o3bt0rb"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
