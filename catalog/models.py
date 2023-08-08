from django.db import models
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page, Orderable, ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from modelcluster.fields import ParentalKey
from wagtail_multi_upload.edit_handlers import MultipleImagesPanel
from wagtail.admin.panels.group import TabbedInterface, ObjectList



class Catalog(Page):
    pass
    
BUILDING_TYPE_CHOICES = [
        ('Сруб', 'Сруб'),
        ('Кирпичные дома', 'Кирпичные дома'),
        ('Каркасные дома', 'Каркасные дома'),
    ]

class House(Page):
    name = models.CharField('Название дома', max_length=100)
    area = models.FloatField('Площадь дома', blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, blank=True, null=True)
    project = models.CharField('Проект', blank=True, null=True, max_length=100)    
    floor = models.IntegerField('Количество этажей', blank=True, null=True)
    building_type = models.CharField('Тип постройки', choices=BUILDING_TYPE_CHOICES, max_length=100, blank=True, null=True)
    floors = models.IntegerField('Этажи', blank=True, null=True)
    rooms = models.IntegerField('Количество комнат', blank=True, null=True)
    bathrooms = models.IntegerField('Санузлы', blank=True, null=True)
    style = models.CharField('Стиль', max_length=100, blank=True, null=True)
    description = RichTextField('Описание', blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [        
        FieldPanel('name', classname='full'),
        FieldRowPanel(
            [
                FieldPanel('area'),
                FieldPanel('price'),
                ],),
        FieldRowPanel(
            [
                FieldPanel('floor'),
                FieldPanel('project'),
                ],),        
                ],
                heading='Данные дома',
            ),

        MultiFieldPanel(
            [   FieldRowPanel(
            [
                FieldPanel('rooms'),
                FieldPanel('bathrooms'),
                ],
                heading='Данные дома',
            ),
        FieldRowPanel(
            [
                FieldPanel('building_type'),
                FieldPanel('style'),
                ],
                heading='Данные дома',
            ),      
                
                FieldPanel('description'),
            ],
            heading='Данные дома',
            classname='collapsible collapsed'
        ),
        
        
    ]
    first_content_panels = [
        InlinePanel('floor_plan', heading='Floor plans', label='Floor plan'),
    ]

    second_content_panels = [
        InlinePanel('content', heading='Content', label='Content'),
    ]

    third_content_panels = [
        MultipleImagesPanel('images', heading='Media content', label="Изображения дома", image_field_name="image"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Данные дома'),
        ObjectList(first_content_panels, heading='Данные этажей'),
        ObjectList(second_content_panels, heading='Дополнительный контент'),
        ObjectList(third_content_panels, heading='Медиа контент'),
        ObjectList(Page.promote_panels, heading='Promote'),
    ])

    @classmethod
    def can_create_at(cls, parent):
        return parent.specific_class == Catalog
    

class FloorPlan(Orderable, ClusterableModel):
    page = ParentalKey(House, on_delete=models.CASCADE, related_name="floor_plan")
    name = models.CharField('Наименование', max_length=100)
    schema = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='img', blank=True, null=True
    )
    floor_content = RichTextField("Контент блока этажи", blank=True, null=True)  

    panels = [
        FieldPanel('name'),
        FieldPanel('schema'),
        FieldPanel('floor_content'),
    ]


class HouseImage(Orderable):
    house = ParentalKey(House, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        FieldPanel('image'),
    ]    

class Content(Orderable):
    house = ParentalKey(House, on_delete=models.CASCADE, related_name='content')
    content = RichTextField("Контент", blank=True, null=True)    

    panels = [
        FieldPanel('content'),
    ]    