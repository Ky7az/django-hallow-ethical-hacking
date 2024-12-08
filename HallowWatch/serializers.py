from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from HallowWatch.models import Content, Feed, Source, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'count')
        extra_kwargs = {'name': {'validators': []}, 'slug': {'validators': []}}


class SourceSerializer(serializers.ModelSerializer):
    source_type = serializers.ChoiceField(choices=Source.SOURCE_TYPES)
    source_type_display = serializers.CharField(
        source='get_source_type_display', read_only=True
    )

    class Meta:
        model = Source
        fields = ('id', 'name', 'slug', 'source_type', 'source_type_display', 'url')


class FeedSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Feed
        fields = (
            'id',
            'source',
            'source_id',
            'tags',
            'create_date',
            'write_date',
            'active',
            'tag_names',
            'count',
        )
        extra_kwargs = {'source_id': {'source': 'source', 'write_only': True}}

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        feed = Feed.objects.create(**validated_data)

        # Tags
        for tag_data in tags_data:
            try:
                tag = Tag.objects.get(slug=tag_data['slug'])
            except ObjectDoesNotExist:
                tag = Tag.objects.create(**tag_data)
            feed.tags.add(tag)

        return feed


class ContentSerializer(serializers.ModelSerializer):
    feed = FeedSerializer(read_only=True)
    source = SourceSerializer(read_only=True)
    tag = TagSerializer(read_only=True)

    class Meta:
        model = Content
        fields = (
            'id',
            'feed',
            'feed_id',
            'source',
            'source_id',
            'tag',
            'tag_id',
            'title',
            'url',
            'viewed',
            'bookmarked',
            'create_date',
        )
        extra_kwargs = {
            'feed_id': {'source': 'feed', 'write_only': True},
            'source_id': {'source': 'source', 'write_only': True},
            'tag_id': {'source': 'tag', 'write_only': True},
        }
