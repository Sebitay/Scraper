How to run code:
python scraper.py --d <date_number> --h <hours>

date_number: is the date number for example 17 of april would be 17 since its only 1 week in advance
hours: list of hours in order of importance ex 09:00 10:00 08:00

the following command would search for hours in the 17th and try to reserve at 09:00, 10:00, 08:00 in order

python scraper.py --d 17 --h 09:00 10:00 08:00 
