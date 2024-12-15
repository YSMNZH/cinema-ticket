import os
import django

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_ticket.settings')

# Initialize Django
django.setup()

from main.models import News  # Import your model after setting up Django

news_data = [
    {
        "title": "'Smile 2' - A bigger, scarier, superior sequel",
        "text": "Lights, camera, bitch, smile / Even when you wanna die... The sequel to 2022's 'Smile' may have taken Taylor Swift's lyrics a little too literally. But for its faults, this follow-up works..",
        "image_url": "main\templates\main\images\1920x1080_cmsv2_6e490f97-6b8a-57e0-8284-916057bf3428-8797258.webp"
    },
    {
        "title": "Non merci! France issues rare ban for horror film 'Terrifier 3'",
        "text": "France’s classification body has slapped an -18 ban on ‘Terrifier 3’, which is out in cinemas today. It’s the first ruling of its kind for a horror film in nearly 20 years.",
        "image_url": "main\templates\main\images\1920x1080_cmsv2_60ff6e18-32fc-5f9b-a9a2-61b32e94caa0-8780190.webp"
    },
    {
        "title": "Celebrated British actress Maggie Smith dies aged 89",
        "text": "Legendary British actress Dame Maggie Smith, who won new fans in the 21st century as Professor Minerva McGonagall in the Harry Potter films and the dowager Countess of Grantham in the hit ITV series Downton Abbey, has died aged 89.",
        "image_url": "main\templates\main\images\828x466_cmsv2_70dbd718-facf-52c0-85b6-0fcbd454bf06-8758842.webp"
    },
    {
        "title": "Venice 2024: Lady Gaga, Joaquin Phoenix and Todd Phillips discuss 'Joker: Folie à Deux'",
        "text": "Premiering on the Lido this evening, 'Joker: Folie à Deux' is the highly anticipated sequel to 2019's controversial 'Joker'. Stars Lady Gaga and Joaquin Phoenix discuss making it - and why the latter suddenly quit Todd Haynes' gay romance film recently.",
        "image_url": "main\templates\main\images\1920x1080_cmsv2_b90b52a5-0bd2-5f05-a9ec-c9355abbadc2-8703176.webp"
    },
    {
        "title": "Turin National Cinema Museum displays iconic objects that make Hollywood movie magic",
        "text": "Turin National Cinema Museum displays iconic objects that make Hollywood movie magic",
        "image_url": "main\templates\main\images\1920x1080_cmsv2_d5bd6f1e-698c-5a2f-983b-7ca22029ca27-8537716.webp"
    },
    {
        "title": "Wicked: How cinema re-invented the witch and restored her powers",
        "text": "As 'Wicked' prepares to cast its spell over the box office, we look at how portrayals of witches on screen have evolved to become symbols of female empowerment and an embracement of otherness.",
        "image_url": "main\templates\main\images\1920x1080_cmsv2_fb6934a2-5677-5e79-96d1-8df2e56443d4-8858176.webp"
    }
]

# Bulk create the news items
news_objects = [News(**news) for news in news_data]
News.objects.bulk_create(news_objects)

print("News items successfully added to the database.")
