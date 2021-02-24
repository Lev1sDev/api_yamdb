from rest_framework import serializers

from ..models import Reviews


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if Reviews.objects.filter(
                title=self.context['view'].kwargs.get('title_id'),
                author=self.context['request'].user
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'You can write only one review to this title.'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'score', 'author', 'pub_date',)
        model = Reviews
