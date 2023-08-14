from rest_framework import serializers
from .models import Han, HanCom
from account.serializers import UserProfileSerializer


class HanComSerializer(serializers.ModelSerializer):
    hancom_user=UserProfileSerializer()
    class Meta:
        model = HanCom
        fields = ['hancom_id', 'hancom_user', 'mention', 'content']

class HanSerializer(serializers.ModelSerializer):
    han_user=UserProfileSerializer()
    do_like=serializers.BooleanField(default=False)
    like_num=serializers.IntegerField()
    HanCom = serializers.SerializerMethodField()
    is_my=serializers.BooleanField(default=False)
    class Meta:
        model = Han
        fields = ['han_id', 'content','do_like','like_num','is_my', 'han_user','HanCom']
    def get_HanCom(self, obj):
        hancoms = HanCom.objects.filter(hancom_han=obj).order_by('created_at').all()
        serializer = HanComSerializer(hancoms, many=True)
        return serializer.data

class NewHanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Han
        fields = ['han_id', 'content','han_user','han_post']

class NewHanComSerializer(serializers.ModelSerializer):
    class Meta:
        model = HanCom
        fields = ['hancom_id','hancom_han', 'hancom_user', 'mention', 'content']