from rest_framework import serializers
from .models import Title

class TitleSerializer(serializers.ModelSerializer):
    """Serializer for the Title model with all fields"""
    
    class Meta:
        model = Title
        fields = '__all__'
        
    def validate_release_year(self, value):
        """Check that release year is reasonable (between 1900 and current year + 5)"""
        
        import datetime
        current_year = datetime.datetime.now().year
        if value < 1900 or value > current_year + 5:
            raise serializers.ValidationError(
                f"Release year must be between 1900 and {current_year + 5}"
            )
        return value

class TitleListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing titles (only essential fields)"""
    
    class Meta:
        model = Title
        fields = ['id', 'show_id', 'type', 'title', 'release_year', 'rating', 'duration', 'listed_in']

class TitleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new titles with validation"""
    
    class Meta:
        model = Title
        fields = '__all__'
        
    def validate_show_id(self, value):
        """Check that show_id is unique"""
        
        if Title.objects.filter(show_id=value).exists():
            raise serializers.ValidationError("A title with this show_id already exists.")
        return value
        
    def validate_type(self, value):
        """Check that type is either 'Movie' or 'TV Show'"""
        
        if value not in ['Movie', 'TV Show']:
            raise serializers.ValidationError("Type must be either 'Movie' or 'TV Show'")
        return value
        
    def validate_release_year(self, value):
        """Check that release year is reasonable (between 1900 and current year + 5)"""
        import datetime
        current_year = datetime.datetime.now().year
        if value < 1900 or value > current_year + 5:
            raise serializers.ValidationError(
                f"Release year must be between 1900 and {current_year + 5}"
            )
        return value

class TitleDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with additional computed fields"""
    
    cast_count = serializers.SerializerMethodField()
    genres_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Title
        fields = '__all__'
        
    def get_cast_count(self, obj):
        """Count the number of cast members"""
        
        if obj.cast:
            return len([name.strip() for name in obj.cast.split(',') if name.strip()])
        return 0
        
    def get_genres_list(self, obj):
        """ Return genres as a list instead of comma-separated string"""
        
        if obj.listed_in:
            return [genre.strip() for genre in obj.listed_in.split(',') if genre.strip()]
        return []
