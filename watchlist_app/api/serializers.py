from dataclasses import fields
from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        #fields = "__all__"
        exclude = ('watchlist',)
        
        
class WatchListSerializer(serializers.ModelSerializer): #It has it's own create and update methods
    
    class Meta:
        model  = WatchList
        fields = "__all__"
        #fields= ['id', 'name', 'description']
        #exclude = ['active']  #Used to exlude the field you do'nt want
    platform = serializers.CharField(source = 'platform.name')
    #reviews = ReviewSerializer(many=True,read_only=True)

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    #watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True, read_only=True,view_name='movie-details')
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"
    
    
     



# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too Short")
     
    
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self,instance, validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be different")
#         else:
#             return data
        
#     # def validate_name(self, value):
        
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too Short")
#     #     else:
#     #         return value
            