from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from HallowWriteup.models import Tag, Website, Report


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'slug',
                  'report_count')
        extra_kwargs = {
            'name': {'validators': []},
            'slug': {'validators': []}
        }


class WebsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Website
        fields = ('id',
                  'name',
                  'slug',
                  'url')


class ReportSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    website = WebsiteSerializer(read_only=True)
    task_type = serializers.ChoiceField(choices=Report.TASK_TYPES)
    task_platform = serializers.ChoiceField(choices=Report.TASK_PLATFORMS)
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    task_platform_display = serializers.CharField(source='get_task_platform_display', read_only=True)

    class Meta:
        model = Report
        fields = ('id',
                  'name',
                  'slug',
                  'tags',
                  'website',
                  'website_id',
                  'task_type',
                  'task_platform',
                  'task_type_display',
                  'task_platform_display',
                  'task_url',
                  'content',
                  'create_date',
                  'write_date',
                  'active')

        extra_kwargs = {
            'website_id': {'source': 'website', 'write_only': True}
        }

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        report = Report.objects.create(**validated_data)

        # Tags
        for tag_data in tags_data:
            try:
                tag = Tag.objects.get(slug=tag_data['slug'])
            except ObjectDoesNotExist:
                tag = Tag.objects.create(**tag_data)
            report.tags.add(tag)

        return report

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.content = validated_data.get('content', instance.content)

        # Tags
        if 'tags' in validated_data:
            updated_tags = validated_data.get('tags')
            deleted_tags = instance.tags.exclude(slug__in=[x['slug'] for x in updated_tags])
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
