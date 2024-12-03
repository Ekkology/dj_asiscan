# from rest_framework import serializers
# from .models import RecognizedFace, UnknownFace

# class FacialAreaSerializer(serializers.Serializer):
#     x = serializers.IntegerField()
#     y = serializers.IntegerField()
#     w = serializers.IntegerField()
#     h = serializers.IntegerField()
#     left_eye = serializers.ListField(child=serializers.IntegerField())
#     right_eye = serializers.ListField(child=serializers.IntegerField())

# class FaceDataSerializer(serializers.Serializer):
#     index = serializers.IntegerField()
#     facial_area = FacialAreaSerializer()
#     confidence = FacialAreaSerializer()

# class FaceRecognitionResultSerializer(serializers.Serializer):
#     verified = serializers.ListField(child=FaceDataSerializer(), default=[])
#     pending = serializers.ListField(child=FaceDataSerializer(), default=[])
#     unknown = serializers.ListField(child=FaceDataSerializer(), default=[])
#     image = serializers.CharField()  # Para la imagen en base64
#     timestamp = serializers.DateTimeField(read_only=True)