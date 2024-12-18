from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from HallowSoup.models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'count')
        extra_kwargs = {'name': {'validators': []}, 'slug': {'validators': []}}


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'name',
            'slug',
            'content',
            'tags',
            'bookmarked',
            'create_date',
            'write_date',
            'active',
        )

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        article = Article.objects.create(**validated_data)

        # Tags
        for tag_data in tags_data:
            try:
                tag = Tag.objects.get(slug=tag_data['slug'])
            except ObjectDoesNotExist:
                tag = Tag.objects.create(**tag_data)
            article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.content = validated_data.get('content', instance.content)
        instance.bookmarked = validated_data.get('bookmarked', instance.bookmarked)

        # Tags
        if 'tags' in validated_data:
            updated_tags = validated_data.get('tags')
            deleted_tags = instance.tags.exclude(
                slug__in=[x['slug'] for x in updated_tags]
            )
            instance.tags.remove(*deleted_tags)

            for tag_data in updated_tags:
                try:
                    tag = Tag.objects.get(slug=tag_data['slug'])
                except ObjectDoesNotExist:
                    tag = Tag.objects.create(**tag_data)
                try:
                    instance.tags.get(slug=tag.slug)
                except ObjectDoesNotExist:
                    instance.tags.add(tag)

        instance.save()
        return instance
