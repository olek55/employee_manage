from rest_framework import status
from rest_framework.views import APIView
from partner_management.models import Partner, Entity
from country_management.models import Country, Currency
from rest_framework.response import Response
from django.forms.models import model_to_dict
from partner_management.serializers import EntitySerializer
from country_management.models import Address


class EntityView(APIView):
    def get(self, request, entity_id):
        if entity_id is None:
            return Response(
                {"error": "Entity ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            entity = Entity.objects.get(id=entity_id)
            serializer = EntitySerializer(entity)
            return Response(serializer.data)
        except Entity.DoesNotExist:
            return Response(
                {"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, entity_id):
        try:
            entity = Entity.objects.get(id=entity_id)
            entity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Entity.DoesNotExist:
            return Response(
                {"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND
            )


class EntityUpdateView(APIView):
    def post(self, request):
        partner_id = request.data.get("partner_id")
        if partner_id is None:
            return Response(
                {"error": "Partner ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            partner = Partner.objects.get(id=partner_id)
        except Partner.DoesNotExist:
            return Response(
                {"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND
            )
        company_name = request.data.get("company_name")
        beneficiary_country = request.data.get("beneficiary_country")
        beneficiary_currency = request.data.get("beneficiary_currency")
        beneficiary_name = request.data.get("beneficiary_name")
        account_number = request.data.get("account_number")
        iban_number = request.data.get("iban_number")
        swift_code = request.data.get("swift_code")
        address_line_1 = request.data.get("address_line_1")
        address_line_2 = request.data.get("address_line_2")
        city = request.data.get("city")
        state = request.data.get("state")
        zip_code = request.data.get("zip_code")
        country = request.data.get("country")
        try:
            country_obj = Country.objects.get(id=country)
        except Country.DoesNotExist:
            return Response(
                {"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            address = Address.objects.get(
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                country=country_obj,
                zip_code=zip_code,
            )
        except Address.DoesNotExist:
            address = Address.objects.create(
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                country=country_obj,
                zip_code=zip_code,
            )
        try:
            entity = Entity.objects.get(partner=partner, address__country=country_obj)
        except Entity.DoesNotExist:
            entity = Entity.objects.create(partner=partner)
        entity.partner = partner
        entity.address = address
        entity.company_name = company_name
        try:
            entity.payments_bank_country = Country.objects.get(id=beneficiary_country)
        except Country.DoesNotExist:
            return Response(
                {"error": "Beneficiary country not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            entity.payments_beneficiary_currency = Currency.objects.get(
                id=beneficiary_currency
            )
        except Currency.DoesNotExist:
            return Response(
                {"error": "Beneficiary currency not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        entity.payments_benificiary_name = beneficiary_name
        entity.payments_account_number = account_number
        entity.payments_iban_number = iban_number
        entity.payments_swift_code = swift_code
        entity.save()
        entity_serializer = EntitySerializer(entity)
        result_json = entity_serializer.data
        country_dict = model_to_dict(entity)
        result_json["address"]["country"] = country_dict
        return Response(result_json, status=status.HTTP_200_OK)
