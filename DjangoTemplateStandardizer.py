import argparse
from re import findall,subn,finditer
from os import listdir

# ایجاد یک شیء از کلاس ArgumentParser
parser = argparse.ArgumentParser(description='A script for handling custom flags and values')
# تعریف پارامترهای مورد نیاز
parser.add_argument('-s', type=str, help='The address of the folder where all static file folders are located (such as images,styles,scripts,fonts,...)')
parser.add_argument('-t', type=str, help='The address of the template file')
# پارس کردن آرگومان‌ها از خط فرمان
args = parser.parse_args()
# به دست آوردن لیست نام فایل های استاتیک در آدرس مشخص
if args.s:list_static_files=listdir(args.s)
# مشخص کردن فایل تمپلیت مورد نظر
if args.t:template_name=args.t
# لیست کلیه خط های فایل تمپلیت(خط اول مقدار اولیه است)
new_line_list=['{% load static %}',]
# باز کردن فایل برای خواندن خط به خط محتوای
with open(template_name,'r') as file:lines_list=file.readlines()
# برسی خط به خط فایل تمپلیت
for item_list in lines_list:
    # برسی هر پوشه (نوع) فایل های استاتیک
    for static_file in list_static_files:
        # پیدا کردن لینک فایل های استاتیک در خط های فایل تمپلیت
        link_range=finditer(f'([\"\']{static_file}/[a-z|A-Z|\|/|.|:|0-9|_|\-|<|>]*[\"\'])',item_list)
        # اگر در هر خطی وجود داشته باشد شرط درست است
        if link_range:
            # برای دسترسی به آدرس و ایندکس شروع و پایان آن
            for find in link_range:
                # استاندارد سازی آدرس فایل استاتیک پیدا شده
                item_updated=item_list[0:find.start()] + '{%' + f' static {find.group()} ' + '%}' + item_list[find.end():]
                # پیدا کردن شماره ایندکس خط استاندارد سازی شده
                index=lines_list.index(item_list)
                # جایگزینی خط استاندارد شده با خط قبلی
                lines_list[index]=item_updated
# باز کردن فایل برای نوشتن محتوای جدید
with open(template_name, 'w') as file:file.writelines(lines_list)