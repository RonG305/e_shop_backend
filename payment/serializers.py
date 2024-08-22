from rest_framework import serializers
from payment.models import MpesaPaymentTransaction


class MpesaPaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPaymentTransaction
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)   
        rep['user'] = str(instance.user)
        return  rep