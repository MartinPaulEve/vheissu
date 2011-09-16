"""
    Copyright 2011 Martin Paul EVe

    This file is part of Vheissu.

    Vheissu is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    Vheissu is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with Vheissu. If not, see http://www.gnu.org/licenses/.
"""

from django.http import HttpResponse
import datetime
import re
from BeautifulSoup import BeautifulSoup
import models


"""
This function is designed to import the source from http://www.vheissu.net/biblio/alles.php into a relational format.
The document referenced in the "with open" block contains the source from this page.
"""
def run_import(request):
    
    article_regex = '\s*(.+?)\.\s*"\s*<strong>\s*(.+?)\s*</strong>\s*\."\s*<i>\s*(.+?)\s*</i>\s*(.+?)\s*\((\d+?)\):\s*(.+?)\.\s*<i>\s*(.+?)\s*</i>'
    bookchapter_regex = '\s*(.+?)\.\s+ \"<strong>(.+?)</strong>\."\s+<i>(.+?)</i>\s*\.\s*(.+?),\s*(.+?)\((\d+)\)\:\s*(.+?)\.\s*<i>(.+?)</i>'
    news_regex = "\s*(.+?)\.\s+ \"\s*<strong>\s*(.+)\s*</strong>\s*\.\"\s*<i>\s*(.+?)\s*</i>\s*\((.+?)\):\s*(.+?)\.\s*<i>\s*(.+?)\s*</i>"

    html = ''
    
    matched_count = 0
    
    with open('/home/martin/Documents/Programming/Pynchon_Biblio/new.txt' ,'r') as f:
    #with open('/home/martin/Documents/Programming/Pynchon_Biblio/test2.xml' ,'r') as f:
        soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
    
        slist = soup.findAll(['p'])

        for line in slist:
            cont = True
            
            # match for articles            
            article_result = re.match(article_regex, line.renderContents())
            
            if article_result:
                
                matched_count = matched_count + 1
            
                venue, created = models.venue.objects.get_or_create(venue_name=article_result.group(3).strip())
                    
                article, created = models.document.objects.get_or_create(doc_document_name=article_result.group(2), doc_venue=venue, doc_pages=article_result.group(6).strip(), doc_issue=article_result.group(4).strip(), doc_notes=article_result.group(7).strip())
                
                authors = article_result.group(1).split(' and ')
                for author in authors:
                    if ',' in author:
                        author_split = author.split(',')
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[1].strip(), last_name=author_split[0].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=article)
                    else:
                        author_split = author.rsplit(' ', 1)
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[0].strip(), last_name=author_split[1].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=article)
                
                publication_date, created = models.pdate.objects.get_or_create(date=datetime.datetime.strptime(article_result.group(5).strip(), '%Y'))
                doc_publication_date, created = models.document_date.objects.get_or_create(date=publication_date, document=article)
                
                publication_type, created = models.ptype.objects.get_or_create(type='Article')
                doc_document_type, created = models.document_type.objects.get_or_create(dtype=publication_type, document=article)
        
                line.extract()
                cont = False

            # match for book chapters
            bookchapter_result = re.match(bookchapter_regex, line.renderContents())
    
            if bookchapter_result and cont:
                
                matched_count = matched_count + 1
                
                venue, created = models.venue.objects.get_or_create(venue_name=bookchapter_result.group(3).strip())
                
                book_chapter, created = models.document.objects.get_or_create(doc_document_name=bookchapter_result.group(2), doc_venue=venue, doc_pages=bookchapter_result.group(7).strip())
                
                authors = bookchapter_result.group(1).split(' and ')
                for author in authors:
                    if ',' in author:
                        author_split = author.split(',')
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[1].strip(), last_name=author_split[0].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=book_chapter)
                    else:
                        author_split = author.rsplit(' ', 1)
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[0].strip(), last_name=author_split[1].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=book_chapter)
                
                publisher, created = models.publisher.objects.get_or_create(publisher_name=bookchapter_result.group(4).strip())
                doc_publisher, created = models.document_publisher.objects.get_or_create(publisher=publisher, document=book_chapter)
                
                publication_place, created = models.publication_place.objects.get_or_create(place=bookchapter_result.group(5).strip())
                doc_publication_place, created = models.document_publication_place.objects.get_or_create(publication_place=publication_place, document=book_chapter)
                
                publication_date, created = models.pdate.objects.get_or_create(date=datetime.datetime.strptime(bookchapter_result.group(6).strip(), '%Y'))
                doc_publication_date, created = models.document_date.objects.get_or_create(date=publication_date, document=book_chapter)
                
                publication_type, created = models.ptype.objects.get_or_create(type='Book chapter')
                doc_document_type, created = models.document_type.objects.get_or_create(dtype=publication_type, document=book_chapter)
                
                line.extract()
                cont = False
                
            # match for newspaper articles
            news_result = re.match(news_regex, line.renderContents())
            
            if news_result and cont:
                
                matched_count = matched_count + 1
            
                venue, created = models.venue.objects.get_or_create(venue_name=news_result.group(3).strip())
                    
                news, created = models.document.objects.get_or_create(doc_document_name=news_result.group(2), doc_venue=venue, doc_pages=news_result.group(5).strip(), doc_notes=news_result.group(6).strip())
                
                authors = news_result.group(1).split(' and ')
                for author in authors:
                    if ',' in author:
                        author_split = author.split(',')
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[1].strip(), last_name=author_split[0].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=news)
                    else:
                        author_split = author.rsplit(' ', 1)
                        the_author, created = models.author.objects.get_or_create(first_name=author_split[0].strip(), last_name=author_split[1].strip())
                        doc_author, created = models.document_author.objects.get_or_create(author=the_author, document=news)
                
                date_to_parse = news_result.group(4).strip()
                date_string = '%B %Y'
                add_date=True
                
                if(re.match('\d+\s*.+?\s*\d+', date_to_parse)):
                    date_string = '%d %B %Y'
                    
                # deal with a date range by adding each day in the range
                # 31 May - 6 June 2002
                daterange = re.match('(\d+)\s*(.+?)\s*-\s*(\d+)\s*(.+?)\s*(\d+)', date_to_parse) 
                if(daterange):
                    add_date = False
                    
                    start_string = daterange.group(1).strip() + ' ' + daterange.group(2).strip() + ' ' + daterange.group(5).strip()
                    end_string = daterange.group(3).strip() + ' ' + daterange.group(4).strip() + ' ' + daterange.group(5).strip()
                
                    start = datetime.datetime.strptime(start_string, '%d %B %Y')
                    end = datetime.datetime.strptime(end_string, '%d %B %Y')
                    dateList = date_range(start, end)
                    
                    for date in dateList:
                        publication_date, created = models.pdate.objects.get_or_create(date=date)
                        doc_publication_date, created = models.document_date.objects.get_or_create(date=publication_date, document=news)
                
                # TODO: need to be able to handle dates such as "Fall 1997"
                
                if(add_date):
                    publication_date, created = models.pdate.objects.get_or_create(date=datetime.datetime.strptime(date_to_parse, date_string))
                    doc_publication_date, created = models.document_date.objects.get_or_create(date=publication_date, document=news)
                
                publication_type, created = models.ptype.objects.get_or_create(type='Article')
                doc_document_type, created = models.document_type.objects.get_or_create(dtype=publication_type, document=news)
        
                line.extract()
                cont = False

    html = soup.prettify()
    #html = matched_count
    
    return HttpResponse(html)


def date_range(start, end):
    r = (end+datetime.timedelta(days=1)-start).days
    return [start+datetime.timedelta(days=i) for i in range(r)]