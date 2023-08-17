# Spark-Kafka-example
A simple example of using spark and kafka and push to elasticsearch


## مقدمه
تصور کنید که با یک وب سرور nginx روبرو هستین که روزانه هزاران و یا حتی میلیونی کاربر دارد و شما میخواد 4 نیازمندی زیر را پوشش دهید:

1- اگر کاربری در هر 20 ثانیه بیشتر از 10 ریکوست زد، سیستم اطلاع رسانی کند

2- اگر تعداد نتیجه 4xx ریکوئست های هر هاست بیشتر از 15 بار در دقیقه بود، سیستم اطلاع رسانی کند.

3- به ازای هر کشور تعداد ریکوئست های موفق را محاسبه کند.

4- به ازای هر هاست میانگین زمان پاسخ دهی ریکوئست را محاسبه کند.

5- داده های خام را به صورت دائمی ذخیره کند

نمونه لاگ شبیه سازی شده وب سرور:

{'server': 's_v3', 'client_ip': '154.85.126.16', 'method': 'PUT', 'status': '201',
'request_time': '0.28', 'host': 'api_38.digikala.com', 'country': 'US', '@timestamp':
'1659509511.865323'}

## معماری
فکر کردن به مسئله و ارائه راهکار میتواند خیلی متنوع و وابسته به نیازمندی های هر سازمان و منابع آنها باشد.
اگر فقط نیازمندی های مطرح شده را درنظر بگیریم، راهکار پیشنهادی بهتر است شرایط زیر را داشته باشد:
- در هیچ شرایطی داده از دست نرود.
- سامانه قابل اعتماد باشد و تقریبا در هیچ شرایطی متوقف نشود و در دسترس باشد
- single point of failure نداشته باشد.
- داده ها باید به صورت آنی پردازش شوند (با توجه به نیازمندی 1 و 2)
- با توجه به حجم داده ورودی، ظرفیت مناست ذخیره سازی فرآهم شود

با فرض موارد بالا بدیهی است که به معماری توزیع شده و hight available نیاز داریم

معماری پیشنهادی میتواند شامل اجزاء زیر باشد:
** Buffering System **
سیستمی که داده های ورودی و خروجی را به صورت موقت نگهداری میکند.
مزایای این سیستم:
- اطمینان از اینکه داده دریافت شده و به صورت موقت موجود است.
- در صورت متوقف شدن دیگر اجزا داده های ورودی از دست نمی روند.
- اجزای مختلف برای استفاده از داده ها به هم وابسته نیستند
- این عدم وابستگی باعث میشود تغییر و توسعه اجزاء دیگر آسانتر باشد
- این سیستم میتواند درگاه اصلی و Interface کل معماری باشد. (حتی سامانه های بیرونی هم میتوانند از داده استفاده کنند)
- تحمل خطای کل معماری را به صورت چشمگیری افزایش میدهد.
شرایط الزامی:
- توزیع شده باشد (تحمل خطا، height available)
- replication داشته باشد (سرعت بالای خواندن و نوشتن، از دست نرفتن داده)
- اجزای دیگر به راحتی بتوانند با آن تعامل کنند

** Processing System **
سیستمی که وظیفه محاسبه داده ها را بر عهده دارد.
مزایا:
- جداسازی بخش پردازش باعث میشود که با تعریف نیازمندی های جدید آن را با دیگر ابزارهای پردازشی جایگزین کرد و یا به صورت همزمان استفاده کرد
شرایط الزامی:
- توزیع شده باشد (تحمل خطا، سرعت پردازش بالا، کاهش هزینه سخت افزار)
- فرمت های مختلف داده را پشتیبانی کند
- نگهداشت آن آسان باشد

** Reporting System
سیستمی که با توجه به نیازمندی های سازمان بتوان گزارشات تحلیلی روی داده ها تولید کند.
این قسمت نتیجه قابل لمس برای سازمان و افراد سازمان است چون کاربر نهایی با این سیستم روبرو خواهد شد.
مزایا:
- تولید گزارشات خواسته شده سازمان
- کمک به تصمیم گیری های سازمان در توسعه آن
شرایط الزامی:
- سرعت و عملکر مناسبی داشته باشد
- دارای رابط کاربری باشد
- برای کاربر نهایی ساده و قابل فهم باشد
- انواع نمودارها و گزارشات را پشتیبانی کند
- قابلیت خروجی گرفتن از گزارشات را داشته باشد

** Search System **
سیستمی که وظیفه جستجتو روی داده ها را برعهده دارد
سیستمی دیگر که کاربر نهایی از آن استفاده خواهد کرد.
مزایا:
- دسترسی به داده ها به صورت موردی و بررسی آن
شرایط الزامی:
- سرعت و عملکرد مناسبی داشته باشد
- دارای رابط کاربری باشد

** Monitoring System **
سیستمی که بتوان همه اجزاء سامانه را به صورت لحظه ای پایش کرد
مزایا:
- میتوان از صحت کارکرد اجزا اطمینان حاصل کرد
- میزان منابع مصرف شده و نرخ ورودی داده و فشار وارده به اجزا را میتوان پایش کرد
شرایط الزامی:
- به صورت برخط باشد
- دارای رابط کاربری باشد
- دارای سیستم اطلاع رسانی باشد

** Store System **
سیستمی که وظیفه ذخیره سازی داده ها را برعهده دارد
مزایا:
- بستری جهت فرآهم سازی داده برای دیگر اجزا
شرایط الزامی:
- توزیع شده باشد (تحمل خطا، hight available، مقرون بصرفه)
- replication داشته باشد (افزایش سرعت خواندن و نوشتن، جلوگیری از ازدست دادن داده)


## راهکار
![diagram-min](https://github.com/aliSadegh/Spark-Kafka-example/assets/24531562/307d453b-cef1-400c-8617-c415cdf8b775)

معماری و راهکار پیشنهادی استفاده از ابزارهای زیر است:
- Kafka: