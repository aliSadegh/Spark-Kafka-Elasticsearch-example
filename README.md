# Spark-Kafka-example
A simple example of using spark and kafka and push to elasticsearch


## مقدمه
تصور کنید که با یک وب سرور nginx روبرو هستین که روزانه هزاران و یا حتی میلیونی کاربر دارد و شما میخواد 4 نیازمندی زیر را پوشش دهید:
1- اگر کاربری در هر 20 ثانیه بیشتر از 10 ریکوست زد، سیستم اطلاع رسانی کند
2- اگر تعداد نتیجه 4xx ریکوئست های هر هاست بیشتر از 15 بار در دقیقه بود، سیستم اطلاع رسانی کند.
3- به ازای هر کشور تعداد ریکوئست های موفق را محاسبه کند و به تاپیکی در کافکا انتقال دهد.
4- به ازای هر هاست میانگین زمان پاسخ دهی ریکوئست را محاسبه کند به تاپیکی در کافکا انتقال دهد
5- داده های خام را به الستیک سرچ انتقال دهد.

![diagram-min](https://github.com/aliSadegh/Spark-Kafka-example/assets/24531562/307d453b-cef1-400c-8617-c415cdf8b775)
