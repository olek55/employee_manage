from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework import status
from rest_framework.response import Response

from partner_management.models import Partner
from contract_management.models import Contract

from optionsets_management.models import PayrollStatus
from django.views.decorators.csrf import csrf_exempt
from chat_management.sockets import (
    sio,
    chat_id,
    send_contract_sign_confirmation_message,
)

from asgiref.sync import sync_to_async

# Create your views here.


@csrf_exempt
@api_view(["POST"])
@authentication_classes([])  # Disable authentication
@permission_classes([])
def check_contract(request):
    contract_status = request.data.get("status")
    data = request.data.get("data")
    # create eor contract webhook
    if (
        contract_status == "contract-signed"
        and data["contract"]["title"] == "Employer of Record Master Services Agreement"
    ):
        eor_contract_id = data["contract"]["id"]
        try:
            contract = Contract.objects.get(eor_contract_id=eor_contract_id)
            contract.onboarding_status = 8
            contract.eor_contract_file = data["contract"]["contract_pdf_url"]
            contract.payroll_status = PayrollStatus.objects.get(name="Onboarding")
            contract.save()
            send_contract_sign_confirmation_message(
                {
                    "employer_id": contract.employer.id,
                    "type": "employer_recode_master_services_agreement_signed",
                }
            )
            print("Sent!~")
            return Response("Ok! Webhook Received!", status=status.HTTP_200_OK)
        except Contract.DoesNotExist:
            return Response("Contract not found", status=status.HTTP_404_NOT_FOUND)

    elif (
        contract_status == "contract-signed"
        and data["contract"]["title"] == "Partner Service Agreement"
    ):
        try:
            partner = Partner.objects.get(psa_id=data["contract"]["id"])
            partner.psa_file = data["contract"]["contract_pdf_url"]
            partner.save()
            send_contract_sign_confirmation_message(
                {
                    "partner_id": partner.id,
                    "type": "partner_service_agreement_signed",
                }
            )
            # sio.emit(
            #     "contract_signed", "partner_service_agreement_signed", room=chat_id
            # )
            print("Sent!~")
            return Response("Ok! Webhook Received!", status=status.HTTP_200_OK)
        except Partner.DoesNotExist:
            return Response("Partner not found", status=status.HTTP_404_NOT_FOUND)

    elif (
        contract_status == "contract-signed"
        and data["contract"]["title"]
        == "Mutual Non Disclosure and Non Solicitation Agreement"
    ):
        try:
            partner = Partner.objects.get(nda_id=data["contract"]["id"])
            partner.nda_file = data["contract"]["contract_pdf_url"]
            partner.save()
            print("Sending message to client....")
            send_contract_sign_confirmation_message(
                {
                    "partner_id": partner.id,
                    "type": "partner_mutual_non_disclosure_agreement_signed",
                }
            )
            print("Sent!~")
            return Response("Ok! Webhook Received!", status=status.HTTP_200_OK)
        except Partner.DoesNotExist:
            return Response("Partner not found", status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(
            "contract-signed webhook not received", status=status.HTTP_200_OK
        )
